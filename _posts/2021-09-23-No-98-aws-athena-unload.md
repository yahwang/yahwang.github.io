---
layout: post
title: Athena 2의 UNLOAD를 활용하여 데이터 가공하기 (with Lambda)
date: 2021-09-23 01:00:00 am
permalink: posts/98
description: CTAS를 대체하는 UNLOAD를 Lambda와 활용하는 법을 알아본다.
categories: [Data, ETL]
tags: [Athena, UNLOAD, Lambda, S3, Parquet]
---

> CTAS를 대체하는 UNLOAD를 Lambda와 활용하는 법을 알아본다.

Athena 2에서 기존 CTAS보다 간편하게 사용할 수 있는 UNLOAD 기능이 생겼다. 

CTAS의 단점이라면 Athena에 임시 테이블(사용되지 않음)이 생성된다는 것이다. 

데이터 엔지니어링 용도로 활용하려면 항상 마지막에 DROP TABLE을 실행해야 한다.

참고 : [Athena로 대용량 CSV 데이터를 Parquet로 변환하기]({{ site.url }}/posts/96)

# UNLOAD 소개

``` sql
UNLOAD (
    SELECT *
    FROM [TABLE]
)
TO 's3:// bucket / prefix /'
WITH (format='parquet', compression='snappy')

-- 참고 : CTAS 사용 시에는 parquet_compression이라는 argument를 사용했으나 UNLOAD에서는 간단하게 사용
```

임시 테이블을 생성하지 않고도 데이터를 가공해서 저장할 수 있다. 단, CTAS와 UNLOAD 공통적으로 주의해야 할 사항이 있다. 

`저장 위치에 이미 파일이 존재한다면 에러가 발생한다는 것이다.`

# Lambda와 함께 사용

멱등성(다시 실행해도 항상 같은 결과를 유지)을 고려하여 항상 파일 존재 유무를 체크하고 실행한다.

이미 실행되었다면 기존 파일을 삭제 후 다시 UNLOAD를 실행한다.

``` python
import boto3
import time

sess = boto3.Session(region_name='ap-northeast-2')
athena = sess.client('athena')
s3 = sess.client('s3')
bucket = 'BUCKET'
prefix = 'PREFIX'

def lambda_handler(event, context):

    # 버킷의 prefix 안에 파일이 존재한다면 모두 삭제한다.
    objects = s3.list_objects_v2(Bucket=bucket, Prefix=f'{prefix}/')
    if objects.get('Contents', False):
        delete_keys = {'Objects' : []}
        delete_keys['Objects'] = [{'Key' : k} for k in [obj['Key'] for obj in objects['Contents']]]
        s3.delete_objects(Bucket=bucket, Delete=delete_keys)

    # UNLOAD 쿼리 실행
    unload_sql = f"""
        UNLOAD (
            SELECT *
            FROM [TABLE]
        )
        TO 's3://{bucket}/{prefix}/'
        WITH (format='parquet', compression='snappy')
    """
    
    log_output_loc = f"s3://{bucket}/logs/athena/"
    start_query_response = athena.start_query_execution(
        QueryString=unload_sql,
        ResultConfiguration={'OutputLocation': log_output_loc}
    )
    query_id = start_query_response['QueryExecutionId']

    # Athena의 response를 주기적으로 SUCESS/FAIL 확인
    while True:
        time.sleep(5)
        get_query_response = athena.get_query_execution(
            QueryExecutionId = query_id
        )
        status = get_query_response['QueryExecution']['Status']['State']
        if status == 'SUCCEEDED':
            break
        elif status == 'FAILED' or status == 'CANCELLED':
            raise Exception

    return None
```

`References` : 

* [How can I store an Athena query output in a format other than CSV, such as a compressed format?](https://docs.aws.amazon.com/athena/latest/ug/unload.html){:target="_blank"}

* [Amazon Athena UNLOADコマンドによるCSV、Parquet、Avro、ORC、JSON出力をサポートしました！](https://dev.classmethod.jp/articles/20210807-amazon-athena-unload/){:target="_blank"}