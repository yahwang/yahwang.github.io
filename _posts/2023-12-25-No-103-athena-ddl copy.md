---
layout: post
title: Athena 테이블 DDL 간단 정리
date: 2023-12-25 01:00:00 am
permalink: posts/103
description: Athena 테이블 DDL에 대해 간단히 정리해본다.
categories: [Data, SQL]
tags: [AWS, Athena]
---

> Athena 테이블 DDL에 대해 간단히 정리해본다.

### 데이터 타입

데이터 타입은 아래 링크에서 확인할 수 있다.

[Data types in Amazon Athena - in AWS](https://docs.aws.amazon.com/athena/latest/ug/data-types.html){:target="_blank"}

#### ARRAY & STRUCT 타입

특별한 경우로는 ARRAY와 STRUCT 타입이 있다.

```
[1,2,3] => array<int>

{"a": 100, "b": "HELLO"} => struct<a:int,b:string>

{"a": 3.54, "b":["a","b"]} => struct<a:float,b:array<string>>

[{"a": 15341, "b": "2.121}, {"a": 2341, "b": 3.232}] => array<struct<a:bigint,b:double>>
```

참고로, SELECT 문에서 직접 사용하려면 다음처럼 사용한다. ( UNLOAD를 통해 데이터 타입을 변환해서 저장할 때 유용하다. )

STRUCT는 ROW라는 함수를 사용하고 CAST를 통해 STRUCT의 타입을 정의해주어야 한다. ( string 대신 varchar를 사용 )

```sql
SELECT ARRAY[1,2,3]

SELECT CAST(ROW('HELLO', 100) AS ROW(name varchar, age int))
```

#### ARRAY 타입 사용 시 주의할 점

Athena에서는 보통 Parquet 타입을 많이 사용한다. Parquet 타입은 empty array를 허용하지 않는다.

UNLOAD 아테나 쿼리를 사용해 parquet로 압축하기 위해서는 배열의 길이 확인 후 empty array를 NULL로 변환해야 한다.

`cardinality`: 배열 길이 함수

```sql
-- 배열 길이 확인
SELECT cardinality(ARRAY[1,2,3]) 
=> 3

SELECT CASE WHEN cardinality(col) = 0 THEN NULL ELSE col END AS col

```

### CSV 데이터

`skip.header.line.count` : CSV의 header를 무시한다는 의미이다.

`FIELDS TERMINATED BY` : CSV의 구분자를 의미한다.

```sql
CREATE EXTERNAL TABLE [ DB ].[ 테이블 ](
  `A` int, 
  `B` string,
  `C` float,
)

ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY ',' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://[ 버킷 ]/[ PREFIX ]'

TBLPROPERTIES (
  'skip.header.line.count'='1'
)
```

### JSON 데이터

`ignore.malformed.json` : 오류 데이터는 무시한다는 의미

```sql
CREATE EXTERNAL TABLE [ DB ].[ 테이블 ](
  ...
  )
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
WITH SERDEPROPERTIES ( 
  'ignore.malformed.json'='true') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'

LOCATION
    's3://[ 버킷 ]/[ PREFIX ]'
```

### PARQUET 데이터

```sql
CREATE EXTERNAL TABLE [ DB ].[ 테이블 ](
  ...
  )

ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'

LOCATION
    's3://[ 버킷 ]/[ PREFIX ]'
```

### 파티션 관리

#### 파티션된 테이블 정의

PARTITIONED BY 라는 부분을 작성해주면 된다.

```sql
CREATE EXTERNAL TABLE [ DB ].[ 테이블 ](
  ...
  )

PARTITIONED BY ( 
  `[ 파티션 ]` string,
)

ROW FORMAT SERDE 
    ...
```

#### 테이블에 파티션 추가

```sql
ALTER TABLE [ DB ].[ 테이블 ] ADD IF NOT EXISTS 
PARTITION ([파티션] = '[ 값 ]') LOCATION 's3://[ 버킷 ]/[ PREFIX ]/[ 파티션 ]=[ 값 ]'
```

### Projection Partitioning

파티션을 자동으로 추가하는 방법으로 파티션이 연속적인 숫자나 날짜일 때 사용한다. 

아래는 파티션이 날짜인 경우 파티션명을 dt로 설정하고 적용한 예시이다.

```sql
CREATE EXTERNAL TABLE [ DB ].[ 테이블 ](
    ...
)

...

PARTITIONED BY ( 
  `dt` string
)

...

LOCATION
  's3://[ 버킷 ]/[ PREFIX ]'
TBLPROPERTIES (
  'projection.dt.format'='yyyy-MM-dd', 
  'projection.dt.interval'='1', 
  'projection.dt.interval.unit'='DAYS', 
  'projection.dt.range'='2023-01-01,NOW', 
  'projection.dt.type'='date',
  'storage.location.template'='s3://[ 버킷 ]/[ PREFIX ]/dt=${dt}'
)

```

`References` : 

* [Amazon Athena JSON 쿼리 - in AWS](https://docs.aws.amazon.com/ko_kr/athena/latest/ug/querying-JSON.html){:target="_blank"}

* [Partition projection with Amazon Athena - in AWS](https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html){:target="_blank"}


