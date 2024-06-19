---
layout: post
title: aws-sdk-pandas Lambda로 활용하기
date: 2024-06-20 01:00:00 am
permalink: posts/112
description: Lambda에서 활용가능한 aws-sdk-pandas에 대해 간단히 정리한다.
categories: [Dev, ETL]
tags: [Lambda]
---

> Lambda에서 활용가능한 aws-sdk-pandas에 대해 간단히 알아본다.

github 주소 : [aws-sdk-pandas (pandas on AWS)](https://github.com/aws/aws-sdk-pandas){:target="_blank"}

몇 년 전에 AWS Data Wrangler라는 이름으로 활용해본 적이 있고 [블로그 글](https://yahwang.github.io/posts/90){:target="_blank"}을 남긴 적도 있다.

pandas on AWS 라는 슬로건(?)을 제시하며, AWS 내 다양한 자원의 데이터를 pandas와 연동하여 사용할 수 있게 도와준다.

잘 사용하지는 않고 있다가 pandas layer를 업그레이드 하는 중 오류가 있었고 우연히 다시 접하게 되었다. 

살펴보니 다수의 라이브러리들이 포함되어 있고 용량이 최적화되어 있었다.

## Lambda에서 활용하기

releases 페이지에서 zip파일을 다운받아서 Lambda Layer로 등록해서 사용할 수 있다.

[aws-sdk-pandas/releases](https://github.com/aws/aws-sdk-pandas/releases){:target="_blank"}

![lambda_aws_sdk_pandas_2]({{site.baseurl}}/assets/img/etl/lambda_aws_sdk_pandas_2.png)

zip 파일을 다운받아 확인해보니 pandas, numpy, pyarrow, pymysql, requests 등이 있다.

pandas와 함께 자주 사용될 수 있는 라이브러리들이 포함되어 있다.

![lambda_aws_sdk_pandas_1]({{site.baseurl}}/assets/img/etl/lambda_aws_sdk_pandas_1.png)

아래 링크에서는 ARN을 제공해주기도 한다.

[aws-sdk-pandas - AWS Lambda Managed Layers](https://aws-sdk-pandas.readthedocs.io/en/stable/layers.html){:target="_blank"}

참고로 [Klayers](https://github.com/keithrozario/Klayers){:target="_blank"}의 ARN을 활용하는 사람들도 있는 거 같지만 aws-sdk-pandas가 더 유용해 보인다.

## 참고: 직접 Layer 생성 시 문제

Lambda layer 사용 시 5개의 레이어, 압축푼 용량 250MB 등의 제한이 있다.

[AWS Lambda Layer(계층) 사용법 정리 (for Python) - yahwang](https://yahwang.github.io/posts/105){:target="_blank"}

위 링크에서 정리했던 방식으로 pandas와 pyarrow를 하나의 레이어로 만들려고 했다. (parquet 활용 목적)

두 개를 설치하면 압축 전에 300MB를 넘어서 Layer로 활용할 수가 없다. 

사이즈를 줄여 레이어를 만드는 시도에 대한 과거 여러 글들도 있었다.

aws-sdk-pandas의 경우, 150MB 정도 용량을 차지한다.

`References` : 

* [AWS 람다(Lambda) 튜토리얼(3): 계층(Layer) 추가 및 판다스(Pandas) 사용 방법](https://yoonminlee.com/aws-lambda-layer-pandas#41-layers-arn){:target="_blank"}

* [AWS Lambda Quota](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html#function-configuration-deployment-and-execution){:target="_blank"}