---
layout: post
title: PyIceberg 기본 사용법 간단 정리
date: 2025-08-13 01:00:00 am
permalink: posts/131
description: PyIceberg 기본 사용법을 간단히 정리한다.
categories: [DataOps]
tags: [iceberg]
---

> PyIceberg 기본 사용법을 간단히 정리한다. (지속적으로 업데이트 예정)

소규모의 데이터 같은 경우는 Spark를 사용하는 것보다 PyIceberg를 사용하는 것이 더 효율적일 수 있다.

## Glue Catalog

Iceberg는 메타데이터와 데이터를 분리하여 저장할 수 있기 때문에 Catalog 정보와 데이터 접근 정보를 따로 입력해주어야 한다.

아래는 client로 통합해서 간단하게 둘 다 접근할 수 있는 방법을 알려준다.

catalog는 glue.  데이터는 s3. 형태로 분리해서 입력할 수도 있다.

[Unified AWS Credentials - PyIceberg](https://py.iceberg.apache.org/configuration/#unified-aws-credentials){:target="_blank"}

[Glue Catalog Configuration - PyIceberg](https://py.iceberg.apache.org/configuration/#glue-catalog){:target="_blank"}

[S3 Configuration - PyIceberg](https://py.iceberg.apache.org/configuration/#s3){:target="_blank"}

```python
# !pip install pyiceberg[s3fs,glue]
from pyiceberg.catalog import load_catalog
import boto3

session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()

glue_catalog = load_catalog(
    'AwsDataCatalog',
    **{
        'client.access-key-id': credentials.access_key,
        'client.secret-access-key': credentials.secret_key,
        'client.session-token': credentials.token,
        'client.region': 'ap-northeast-2',
    },
    type='glue'
)

# 데이터베이스.테이블명
iceberg_test_table = glue_catalog.load_table("default.iceberg_test")

# 데이터 접근 오류 시 AWS Error ACCESS_DENIED during HeadObject operation: No response body 오류가 발생한다.
```

참고: 

AWS 프로필을 사용할 수 있는 glue.profile-name 옵션이 있는데 s3.profile-name은 사용할 수 없다.

데이터 접근은 pyarrow의 S3FileSystem 사용하는데 profile을 통한 접근을 지원하지 않기 때문이다.


### Pandas

```python
import pandas as pd
import pyarrow as pa

df = pd.DataFrame()

arrow_table = pa.Table.from_pandas(df)

iceberg_test_table.append(arrow_table)

##################
# 테이블 데이터 전체 읽기
##################

df = iceberg_test_table.scan().to_pandas()
```

### DuckDB

```python
arrow_table = duck_conn.sql(
    """
    SELECT *
    FROM df
    """
).to_arrow_table()

iceberg_test_table.append(arrow_table)

##################
# 테이블 데이터 전체 읽기
##################

df_conn = table.scan().to_duckdb(table_name="df")
df_conn.sql("SELECT * FROM df")
```

`References`: 

* [Getting started with PyIceberg](https://py.iceberg.apache.org/){:target="_blank"}

* [pyiceberg와 Glue Catalog를 이용한 Apache Iceberg 사용](https://devpongi.tistory.com/131){:target="_blank"}
