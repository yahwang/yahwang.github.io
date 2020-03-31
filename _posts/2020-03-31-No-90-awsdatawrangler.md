---
layout: post
title: AWS Data Wrangler(Pandas on AWS) 활용하기
date: 2020-03-31 09:00:00 pm
permalink: posts/90
description: AWS 서비스의 데이터를 Pandas로 활용하는 AWS Data Wrangler에 대해 알아본다.
categories: [Data, DataOps]
tags: [AWS, Pandas, Lambda]
---

> AWS 서비스의 데이터를 Pandas로 활용하는 AWS Data Wrangler에 대해 알아본다.

<img src="https://aws-data-wrangler.readthedocs.io/en/latest/_images/logo_transparent.png" width="150px">
<div style="text-align:center;font-size:x-large;">AWS Data Wrangler</div>
<div style="text-align:center;font-size:x-large;">( Pandas on AWS )</div>


<div><i class="fa fa-github fa-lg" aria-hidden="true"></i> &nbsp;<a href="https://github.com/awslabs/aws-data-wrangler" target="_blank" style="font-size:1.3em">awslabs/aws-data-wrangler</a></div>

참고 : 글 작성 기준으로 0.3.2 버전이지만 1.0 버전에 많은 변화가 생긴다고 한다.

    IMPORTANT NOTE: Version 1.0.0 coming soon with several breaking changes.

## 사용 가능한 방법

자세한 내용은 github와 공식문서를 통해 확인가능하다.

| FROM                     | TO              |
|--------------------------|-----------------|
| Pandas        | S3       | 
| S3                | Pandas |
| Athena            | Pandas | 
| Pandas         | Amazon Redshift | 
| Redshift          | Pandas | 
| Pandas        | Aurora   |
| Aurora            | Pandas |  
| CloudWatch Logs Insights | Pandas |
| Glue Catalog             | Pandas | 

### Pandas - S3 활용 예시

boto3와 함께 사용하면 쉽게 사용할 수 있다.

``` python
import boto3
import awswrangler as wr

boto_sess = boto3.Session(profile_name="yahwang")

wr_sess = wr.Session(boto3_session=boto_sess)

df = wr_sess.pandas.read_csv("s3://.../csvs/tips.csv")

# CSV로 저장
## 파일명을 따로 지정해야 하나의 파일로 저장된다.
wr_sess.pandas.to_csv(df,'s3://yahwang-test/csvs',filename='XXX.csv', header=True, preserve_index=False)

# parquet로 변환해서 S3에 저장 가능 
## 한 폴더에 multi-file 형태로 저장된다.
wr_sess.pandas.to_parquet(df, "s3://.../parquets/tips_parquet", preserve_index=False)
```

메모리 제한으로 모든 데이터를 한 번에 읽을 수 없는 경우, pandas에서는 chunksize 옵션을 통해 row 개수로 제한하지만 

AWS Data Wrangler에서는 max_result_size 옵션을 통해 사이즈로 제한할 수 있다.

![wr_size_limit]({{site.baseurl}}/assets/img/dataops/wr_size.png)

## Lambda layer 제공

github releases에서 Lambda layer를 제공한다. layer 안에는 numpy, pandas, pyarrow 등이 들어있다.

<i class="fa fa-github fa-sm" aria-hidden="true"> [aws-data-wrangler - Releases](https://github.com/awslabs/aws-data-wrangler/releases){:target="_blank"} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  [Setting Up Lambda Layer](https://aws-data-wrangler.readthedocs.io/en/latest/install.html#setting-up-lambda-layer){:target="_blank"}


![wr_diagram]({{site.baseurl}}/assets/img/dataops/wr_lambda.png)

### Lambda Layer로 활용 예시

토이 프로젝트를 진행하면서 따릉이 데이터 실시간 API가 대여소 정보를 누락시키거나 새롭게 추가되는 경우가 있었다.

Kinesis Data Analytics에서 S3의 데이터를 reference 테이블 형태로 활용하는 것을 참고해서

데이터 Validation을 Data Wrangler를 활용해서 구현해보았다.

![wr_diagram]({{site.baseurl}}/assets/img/dataops/wr_diagram.png)

    코드의 일부

``` python
# rent_api : API로 받은 데이터를 의미
rent_df = pd.DataFrame(rent_api)
st_df = wr.pandas.read_csv('s3://yahwang-test/csvs/st_info.csv')
# indicator 파라미터를 활용한다.
broken = pd.merge(st_df, rent_df, how='outer', left_on='st_id',right_on='stationId', indicator=True) \
         .loc[:,['st_id','stationId','_merge']]
```

|    | st_id   | stationId   | _merge     |
|---|--------|------------|-----------|
|  0 | ST-1    | nan         | **left_only**  |
|  1 | ST-2    | nan         | **left_only**  |
|  2 | ST-4    | ST-4        | both       |
|  3 | ST-5    | ST-5        | both       |
|  4 | ST-6    | ST-6        | both       |
|  5 | ST-7    | ST-7        | both       |
|  6 | nan     | ST-8        | **right_only** |

데이터를 보면 left_only는 API에서 특정 대여소 정보를 받아오지 못했다는 의미이고,

right_only는 대여소 table의 정보가 없는 새로운 대여소의 데이터를 가져왔다는 것을 확인할 수 있다.

`References` : 

* [aws-data-wrangler.readthedocs.io](https://aws-data-wrangler.readthedocs.io/){:target="_blank"}



