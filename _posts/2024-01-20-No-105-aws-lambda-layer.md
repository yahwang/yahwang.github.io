---
layout: post
title: AWS Lambda Layer(계층) 사용법 정리 (for Python)
date: 2024-01-20 01:00:00 am
update: 2025-02-05 01:00:00 am
permalink: posts/105
description: AWS Lambda Layer 사용법에 대해 간단히 정리해본다.
categories: [Data, ETL]
tags: [AWS, Lambda]
---

> AWS Lambda Layer 사용법에 대해 간단히 정리해본다.


## Layer(계층) 만들기

### 이전

패키지 저장 명령어는 다음과 같다.

```python
pip install \
    --platform manylinux2014_aarch64 \
    --target=python \
    --implementation cp \
    --python-version 3.11 \
    --only-binary=:all: --upgrade \
    <package_name>
```

`platform`: OS 정보

Lambda에서 x86_64 또는 arm64 아키텍처를 선택할 수 있다. 

arm64 Lambda에서 패키지가 실행되지 않는 경우만 x86_64만 사용하기를 권장한다. 

성능도 나아지고 무엇보다 비용을 20%나 절감할 수 있기 때문이다.

Amazon Linux 2 기준 (CentOS 기반)

|아키텍처|platform|
|-|-|
|arm64|manylinux2014_aarch64|
|x86_64|manylinux2014_x86_64|

OS 정보는 [pypa/manylinux](https://github.com/pypa/manylinux){:target="_blank"}에서 확인할 수 있다.

### 최신 (2025~)

manylinux2014는 2024년 6월 30일부터 EOL 상태이다. AWS 공식 문서에서는 변화가 없는데 layer 실행에 문제가 생기는 경우가 있었다.

제일 안정적으로 layer를 생성하는 방법은 Lambda 이미지를 활용해서 생성하는 법이다.

docker container에서 layer를 다운받고 로컬로 복사해서 zip 파일을 만드는 방식이다.

사용할 이미지는 [Amazon ECR Public Gallery - python](https://gallery.ecr.aws/lambda/python){:target="_blank"}에서 확인할 수 있다.

```python
docker run --name lambda-layer -it --entrypoint /bin/bash public.ecr.aws/lambda/python:3.12-arm64

pip install -t python [패키지]

docker cp lambda-layer:/var/task/python ~/opt/
```

![aws_lambda_layer_3]({{site.baseurl}}/assets/img/aws/aws_lambda_layer_3.png)

`target`: 저장할 폴더 위치

Lambda에서 패키지를 바로 읽을 수 있도록 하려면 python 폴더를 생성 후 저장해야 한다.

자세한 정보는 [종속 항목을 위한 Python 계층 생성 - in AWS](https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/python-package.html#python-package-dependencies-layers){:target="_blank"}에서 알 수 있다.

`python-version` : 파이썬 버전

패키지 저장 후 zip 파일을 생성하면 된다.

```cli
zip -r lambda-layer-duckdb-python-arm64.zip python
```

**참고**

Python 3.11까지는 Lambda OS가 Amazon Linux 2이고 3.12 부터는 Amazon Linux 2023가 사용된다.

자세한 정보는 [Lambda 런타임 - in AWS](https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/lambda-runtimes.html){:target="_blank"}에서 확인할 수 있다.

## Layer(계층) 등록하기

![aws_lambda_layer_2]({{site.baseurl}}/assets/img/aws/aws_lambda_layer_2.jpg)

`S3 링크 URL`

보통 바로 업로드할 수 있지만 zip 파일이 10MB가 넘는 경우 S3에 먼저 업로드한 후 링크 URL을 입력하라고 권장한다. ( 어느 정도는 무시하고 가능한 듯 보임 )

링크 URL은 업로드된 S3 객체를 클릭해보면 객체 URL 정보로 확인할 수 있다.

![aws_lambda_layer_1]({{site.baseurl}}/assets/img/aws/aws_lambda_layer_1.jpg)

## Layer(계층) 적용하기

콘솔에서 Lambda 선택 후 제일 아래에서 추가할 수 있다. 

등록한 계층은 사용자 지정 계층에서 확인할 수 있고 런타임 설정에 맞는 계층만 선택가능하다.

참고로, 최대 추가 가능한 계층은 5개이다.

![aws_lambda_layer_3]({{site.baseurl}}/assets/img/aws/aws_lambda_layer_3.jpg)

`References` : 

* [빌드된 배포판 작업(휠) -in AWS](https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/python-package.html#python-package-wheels){:target="_blank"}


