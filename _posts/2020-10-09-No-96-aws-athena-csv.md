---
layout: post
title: Athena로 대용량 CSV 데이터를 Parquet로 변환하기
date: 2020-10-09 10:00:00 pm
permalink: posts/96
description: AWS Glue 테스트 환경을 간단하게 생성하고 활용하는 방법을 알아본다.
categories: [Data, ETL]
tags: [Athena, S3, Parquet, CTAS]
---

> Athena로 대용량 CSV 데이터를 Parquet로 변환하는 방법을 알아본다.

## 도입

로그 데이터 분석을 하려고 하니 다음과 같은 문제에 부딪혔다.

1. 하루치 CSV 데이터 크기가 약 7GB이다.

2. 온전한 하루치 데이터를 구하기 위해서는 2-3일치 데이터를 전처리해야 한다.

3. 로컬에 데이터를 유지하려고 하니 노트북 SSD 용량이 부족하다.

4. 노트북(16GB RAM)에서 pandas로 하루치 데이터도 읽지 못한다. (컬럼을 몇 개 안 써도)

Parquet 타입으로 데이터를 변환하는 것이 필요하다고 느꼈다. EMR이나 Glue를 사용해보려고 하다가 

Athena로도 가능하다는 글을 발견하고 시도해봤다. 먼저, S3에 원본 CSV 파일을 업로드한다. 

( 기가 인터넷이 아닌 일반 인터넷이라면 XX GB 데이터를 올리기만 해도 시간이 많이 걸리기는 했다. )

## CSV 테이블 정의

이 방식은 default인 LazySimpleSerDe 방식이다. 만약, 데이터가 "1", "string", .. 이런 식으로 되어 있다면 

OpenCSVSerDE 방식을 사용해야 한다. 참고 : [OpenCSVSerDe for Processing CSV](https://docs.aws.amazon.com/athena/latest/ug/csv-serde.html){:target="_blank"}

대부분의 CSV 테이블 DDL 쿼리는 포맷이 같고 추가 설정만 잘 해주면 된다.

`데이터 타입 확인` 

[Athena data-types - AWS](https://docs.aws.amazon.com/athena/latest/ug/data-types.html){:target="_blank"}

`TBLPROPERTIES`

'skip.header.line.count'='1' : header row를 제외한다는 의미

'serialization.null.format'='' : 공백 문자는 Null(None)로 처리한다는 의미

`LOCATION`

LOCATION은 하나의 파일이 아니라 prefix(폴더) 전체를 의미한다. 마지막에 반드시 /를 붙여줘야 한다.

(폴더 안에 메타정보가 같은 CSV 파일이 여러 개 있다면, 하나의 테이블로 구성할 수 있다.)


``` sql
# 간단하게 DB 생성
CREATE DATABASE clickstreams; 

CREATE EXTERNAL TABLE IF NOT EXISTS my_db.my_table (
         `uuid_seq` bigint,
         `col_1` string,
         `col_2` double,
         `col_4` int,
         `registered_at` timestamp 
)

ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' ESCAPED BY '\\' LINES TERMINATED BY '\n' 
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3:// bucket / prefix (folder) /' 
TBLPROPERTIES ( 'skip.header.line.count'='1', 'serialization.null.format'='' );
```

쿼리의 문제가 없다면 바로 실행된다. 

    결과 확인

``` sql
# 컬럼 확인
SELECT *
FROM   information_schema.columns
WHERE  table_schema = 'my_db' and table_name = 'my_table';

# 데이터 확인
SELECT * FROM my_db.my_table LIMIT 5;
SELECT COUNT(*) FROM my_db.my_table;
```

BigQuery는 COUNT(*)에 비용이 들지 않지만 Athena는 전체 데이터 크기가 비용으로 측정되니 주의해야 한다.


## CTAS를 활용해 Parquet로 변환

Athena는 쿼리 결과를 CSV 타입으로만 저장할 수 있다. CTAS를 사용하면 변환한 데이터를 다양한 타입(ORC, Parquet 등)

으로 변환해서 S3에 저장할 수 있다. 또한, Partitioning과 Bucketing도 지원한다. 

자세한 정보는 References의 첫번째 링크에서 확인할 수 있다.

``` sql
CREATE TABLE my_db.my_table_parquet
WITH ( format = 'PARQUET', parquet_compression = 'SNAPPY', 
    external_location = 's3:// bucket / prefix /' ) AS
SELECT `uuid_seq` bigint,
         `col_1` string,
         `col_2` double,
         `col_4` int,
         `registered_at` timestamp
FROM my_db.my_table
```

### Partitioning and Bucketing 추가

Partitioning을 하기 위해 year, month, day 컬럼을 생성했다. **partitioned_by = ARRAY[ col1, col2, ...]**

형태로 입력해주면 된다.

Bucketing을 사용한 이유는 Partition당 하나의 파일로 생성해서 로컬에 저장하고 싶었기 때문이다. (파일 개수 조절)

**bucketed_by=ARRAY[col1]**과 **bucket_count=1**을 설정하면 분산처리한 데이터를 하나의 파일로 모아준다.

    주의할 점

Partition될 컬럼은 SELECT 문 제일 마지막에 위치해야 한다. bucketing을 한다면 bucketing 컬럼 다음에 위치한다.

Partitioning과 Bucketing은 각각의 컬럼이 필요하다.

``` sql
CREATE TABLE my_db.my_table_parquet_partitioned
WITH ( format = 'PARQUET', partitioned_by = ARRAY['year', 'month', 'day'], 
    bucketed_by=ARRAY['day'], bucket_count=1, parquet_compression = 'SNAPPY', 
    external_location = 's3:// bucket / prefix(folder) /' ) AS
SELECT `uuid_seq` bigint,
         `col_1` string,
         `col_2` double,
         `col_4` int,
         `registered_at` timestamp, 
         date_format(register_at, '%d') AS "_day", -- for bucketing
         date_format(register_at, '%Y') AS year,
         date_format(register_at, '%m') AS month,
         date_format(register_at, '%d') AS day
FROM my_db.my_table
```

`bucket / prefix / year=2020 / month=10 / day=12 ` 안에 파일이 생성된다. 

## 추가 이슈 및 대응

&nbsp;&nbsp; 1. 쿼리 중간에 실패할 경우, 생성중인 데이터가 S3안에 존재할 수 있다. 다시 실행하면 오류가 발생한다.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; => Athena에서 위치를 알려주고 셀프로 삭제하라고 한다.

&nbsp;&nbsp; 2. Athena의 기본 쿼리 최대 실행시간은 30분이다. (Service Quotas에서 변경 가능) 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; => 쿼리마다 약 20GB의 데이터로 실행해야 거의 30분 직전에 완료되었다.

&nbsp;&nbsp; 3. 로컬로 다운받을 때 주의할 점은 파일명이 폴더마다 똑같기 때문에 구분해야 한다. (파일명 변경은 셀프로 해야하는 듯하다.)

## 참고사항

Parquet나 ORC 포맷으로 변환하면 비용을 매우 절약할 수 있다. 단, 성능이 향상되는 것은 아닌 듯 하다.

아래 링크에서 여러 쿼리를 테스트해 본 결과를 확인할 수 있다.

[Amazon Athena: Beyond The Basics – Part 2](https://www.northbaysolutions.com/amazon-athena-beyond-the-basics-part-2/){:target="_blank"}

`References` : 

* [How can I store an Athena query output in a format other than CSV, such as a compressed format?](https://aws.amazon.com/premiumsupport/knowledge-center/athena-query-output-different-format/?nc1=h_ls){:target="_blank"}

* [How can I set the number or size of files when I run a CTAS query in Athena?](https://aws.amazon.com/ko/premiumsupport/knowledge-center/set-file-number-size-ctas-athena/){:target="_blank"}

* [Using AWS Athena To Convert A CSV File To Parquet](https://www.cloudforecast.io/blog/Athena-to-transform-CSV-to-Parquet/){:target="_blank"}


