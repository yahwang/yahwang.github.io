---
layout: post
title: Athena Partition Projection 활용 시 주의할 사항
date: 2023-12-11 01:00:00 am
permalink: posts/101
description: Athena Partition Projection 활용 시 겪었던 주의할 사항에 대해 알아본다.
categories: [Data, ETL]
tags: [Athena, S3]
---

> Athena Partition Projection 활용 시 겪었던 주의할 사항에 대해 알아본다.

## 빅쿼리와 비교

빅쿼리는 테이블 정의 시 설정한 컬럼에 따라 파티션을 생성하고 관리해주는 기능이 있어서 INSERT만 해주면 된다.

테이블에 존재하는 데이터는 빅쿼리가 자체적으로 데이터를 압축해서 성능도 최적화해준다.

그리고 파티션을 설정한 테이블에 대해서는 WHERE 절에 파티션을 명시해야 쿼리가 가능한 기능도 있는 게 나름 장점이다.

( ATHENA에서는 파티션없이 쿼리 시 비용 문제가 생길 수도 있다... ) 

![bigquery_create_table]({{site.baseurl}}/assets/img/etl/bigquery_create_table.jpg)

반면, 아테나는 사용자가 직접 데이터 압축을 수행하고 파티션 관리를 해주어야 하는 불편함이 있다.

## ATHENA 활용

기본적인 방법으로는 Glue Data Catalog에 파티션을 등록해야 아테나에서 파티션을 읽고 데이터를 처리할 수 있다.

**Partition Projection**은 매번 Catalog에 등록하지 않고 아테나에서 스스로 파티션을 인식하는 기능이다.

실행방법에 대해서는 다른 블로그에 가이드가 많이 있으니 참고하면 된다.

빅쿼리는 일별과 시간별 중 파티션을 선택해야 하는데 비용과 성능을 고려했을 때

일별과 시간별 파티션을 둘 다 처리하고 싶어 아테나로는 다음처럼 구성했다.

( 일별로 파티션 처리할 경우, 매 시간 배치 처리 시 불필요한 시간의 데이터까지 스캔되기 때문이다. )

```sql
CREATE EXTERNAL TABLE my_table (
 ...
)
...
PARTITIONED BY (
 dt STRING
 dth STRING
)
LOCATION "s3://DOC-EXAMPLE-BUCKET/prefix/"
TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.dt.format'='yyyy-MM-dd', 
  'projection.dt.interval'='1', 
  'projection.dt.interval.unit'='DAYS', 
  'projection.dt.range'='2023-01-01,NOW', 
  'projection.dt.type'='date', 
  'projection.dth.format'='yyyy-MM-dd-HH', 
  'projection.dth.interval'='1', 
  'projection.dth.interval.unit'='HOURS', 
  'projection.dth.range'='2023-01-01-00,NOW', 
  'projection.dth.type'='date', 
  'projection.enabled'='true', 
  'storage.location.template" = "s3://DOC-EXAMPLE-BUCKET/prefix/dt=${dt}/dth=${dth}'
)
```

이렇게 하면 테이블에 파티션 추가를 위해 **ALTER TABLE ADD PARTITION** 실행을 안 해주어도 된다.

아테나 테이블이 생길 때마다 파티션을 관리해주어야 하는 요소를 줄일 수 있다.

( 참고로, 미리 미래에 생길 파티션을 추가할 수도 있지만 매일 +1일 파티션을 추가하는 파이프라인을 사용하고 있다. )

## NESTED 파티션 문제점

아테나는 S3 데이터를 읽는다. S3를 읽는 것은 비용으로 연결되기에 주의가 필요하다.

S3 Gateway endpoint를 설정해놓았다면 AWS 내부에서 S3 데이터 전송 비용은 청구되지 않는다. 

그러나 S3에는 GET, POST 등의 요청 및 데이터 검색 비용은 항상 청구된다. 아테나를 잘못 사용할 경우, 이 비용이 문제가 될 수 있다.

핵심은 아테나에서 파티션을 검색할 때 **LIST 요청**을 수행한다.

다음은 CloudTrail을 통해 수집한 S3 요청 로그 예시이다. 파티션 검색을 위해 List 요청을 수행한다.

|eventtime|eventsource|eventname|awsregion|sourceipaddress|useragent|requestparameters|
|	- |s3.amazonaws.com|ListObjects|ap-northeast-2|athena.amazonaws.com|athena.amazonaws.com| prefix/dt=.../dth=...|

NESTED 파티션을 구현했기 때문에 다음과 같이 다양한 WHERE 문 처리가 가능하다.

```sql
1. WHERE dt = '2023-12-05' AND dth = '2023-12-05-03'

2. WHERE dth = '2023-12-05-03'

3. WHERE dth BETWEEN '2023-12-04-15' AND '2023-12-05-03'

4. WHERE dt BETWEEN '2023-12-04' AND '2023-12-05' AND dth BETWEEN '2023-12-04-15' AND '2023-12-05-03'
```

Glue Data Catalog에 파티션을 추가하면 검색을 위한 List 요청을 최소화하여 수행한다.

반면, Partition Projection을 적용한 테이블은 정확한 파티션을 지정하지 않으면 모든 파티션을 서치하는 동작을 수행할 수 있다.

2번 dth='2023-12-05-03'만 지정할 경우, 모든 상위 파티션인 dt와 dth 파티션들을 모두 스캔하려고 시도한다. 

최악의 경우, 모든 파티션 dt의 개수 * dth 개수 ( 일수 * 24 * 파일의 개수) List 요청을 시도한다.

## 결론

S3 비용은 요청과 여러 저장 종류의 합으로 청구된다. 요청 비용은 관심가지지 않으면 무시하기 쉬운 비용이다.

S3 저장 비용보다 상대적으로 적어 문제를 모를 수도 있고 오히려 더 큰 금액이 발생할 수도 있다.

뿐만 아니라 서비스에도 문제가 생길 수도 있다. S3에는 기본적으로 요청 제한이 있다.

과도한 List 요청이 S3 서비스 Throttling을 발생시켜서 다른 서비스까지 문제가 될 수 있다.

또한, EMR, Redshift 등에서 아테나 테이블 데이터를 읽으려면 Glue Data Catalog에 파티션이 등록되어 있어야 한다.

온전히 아테나로 테이블을 조회하는 경우에만 Partition Projection을 사용해야 한다.

현재 파이프라인 중에서 dt와 dth 파티션을 정확히 사용하는 테이블에 대해서만 Partition Projection을 사용하고

그 외의 테이블엔 모두 ALTER TABLE ADD PARTITION 명령어로 파티션을 추가하고 있다.

`References` : 

* [Partition projection with Amazon Athena](https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html){:target="_blank"}

* [ALTER TABLE ADD PARTITION](https://docs.aws.amazon.com/ko_kr/athena/latest/ug/alter-table-add-partition.html){:target="_blank"}