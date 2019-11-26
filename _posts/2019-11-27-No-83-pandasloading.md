---
layout: post
title: Pandas에서 CSV 데이터를 빠르게 읽기 (with. Apache Arrow, Parquet)
date: 2019-11-27 01:00:00 am
permalink: posts/83
description: Pandas에서 CSV 데이터를 빠르게 읽는 법을 알아본다.
categories: [Data, ETL]
tags: [Python, Pandas, Arrow, Parquet]
---

> Pandas에서 CSV 데이터를 빠르게 읽는 법을 알아본다.

pandas는 기본적으로 single core를 사용한다. 데이터 크기가 커질수록 데이터 처리 속도도 문제지만 데이터를 읽거나 쓸 때 매우 느리다.

## Apache Arrow ( Pyarrow )

Apache Arrow is a cross-language development platform for in-memory data.

![apache arrow]({{site.baseurl}}/assets/img/tech/arrow.png)

출처 : https://arrow.apache.org

Apache Arrow의 핵심은 Coulmnar In-Memory 포맷과 pandas, spark 등 여러 시스템에서 같은 메모리 포맷을 공유한다는 점이다.

Arrow는 특히 **Parquet** 파일을 활용하는 것이 효과적이다.

Parquet 파일 설명 : [Big Data File Formats](https://blog.clairvoyantsoft.com/big-data-file-formats-3fb659903271){:target="_blank"}

pandas에서도 Arrow의 메모리 포맷을 활용하면 데이터를 읽고 쓰는 데 도움을 받을 수 있다.

    참고

Pandas를 원활히 사용하기 위해서는 데이터 크기의 약 3배의 메모리가 필요하다는 의견이 있다. 

Apache Arrow는 메모리 절약은 해결해주지는 못한다. 이 부분은 Spark와 같은 분산 처리를 고려해야 한다.

## 사용법

### Apache Arrow 설치

Python에서는 pyarrow라는 이름으로 간단히 설치할 수 있다.

```
pip install pyarrow
```

### CSV 데이터 읽기

기본적으로 **Table**이란 이름의 데이터타입을 사용한다. 타입은 null, int64, float64, timestamp[s], string, binary로 추론한다.

데이터 읽기가 빠른 이유 중 하나는 multi thread를 사용하기 때문이다.

``` python
from pyarrow import csv
pyarrow_table = csv.read_csv('data.csv')

pyarrow_table.schema
#    Year: int64
#    Month: int64
#    ...

pyarrow_table.shape
#   (21604865, 29)
```

Arrow의 Table을 Pandas 데이터프레임으로 변환해서 사용한다.

``` python
df = pyarrow_table.to_pandas()
# 또는 (한 번에)
df_from_pyarrow = csv.read_csv('data.csv').to_pandas()
```

### Parquet 데이터 타입으로 읽고 쓰기

csv 데이터는 읽는 것보다 쓰는 데 매우 시간이 많이 걸린다. 

arrow에서는 csv 포맷 쓰기를 지원하지는 않기 때문에 parquet 타입 파일을 활용해야 한다.

#### CSV를 바로 Parquet 파일로 저장

``` python
import pyarrow.parquet as pq
from pyarrow import csv

pq.write_table(csv.read_csv('data.csv'), 'data.parquet')
```

#### 데이터 프레임을 Parquet 파일로 저장

데이터프레임을 먼저 Table로 변환 후 Parquet로 저장한다.

``` python
### 속도는 비슷

# 1. pandas 함수
import pandas as pd
df.to_parquet('data3.parquet',engine='pyarrow', index=False)

# 2. 
import pyarrow as pa
import pyarrow.parquet as pq

## index 컬럼을 제거할 경우, preserve_index=False를 활용한다.
table_from_pandas = pa.Table.from_pandas(df, preserve_index=False)
pq.write_table(table_from_pandas, 'data.parquet')
```

참고 : Pandas는 nanosecond를 지원하지만 Spark 같은 경우는 nanosecond를 지원하지 않기 때문에 관련 옵션이 있다.

#### Parquet 파일을 데이터프레임으로 읽기

읽는 속도가 더 빨라지기 때문에 유용하다.

``` python
### 속도는 비슷

# 1. pandas 함수
import pandas as pd
df = pd.read_parquet('data.parquet',engine='pyarrow')

# 2.
import pyarrow.parquet as pq
df = pq.read_pandas('data.parquet').to_pandas()
```

### 참고 : 속도 테스트

    테스트 환경(노트북)
    
RAM : 16G &nbsp;&nbsp; PYTHON : 3.7.5 &nbsp;&nbsp; DATA : 2.1 GB

CPU : Intel® Core™ i5-8250U CPU @ 1.60GHz × 8


| 비교 | Pandas | Arrow |
|-----|-------|--------|
|**CSV 읽기**|67.30 sec|17.32 sec|
|**Parquet 읽기**|-|3.58 sec|
|**CSV 저장 VS Parquet 저장**|406.45 sec|15.84 sec|


`References` : 

* [A gentle introduction to Apache Arrow with Apache Spark and Pandas](https://towardsdatascience.com/a-gentle-introduction-to-apache-arrow-with-apache-spark-and-pandas-bb19ffe0ddae){:target="_blank"}

* [Apache Arrow - Reading CSV files](https://arrow.apache.org/docs/python/csv.html){:target="_blank"}