---
layout: test_post
title: AWS Lambda, Docker로 테스트하기 (with Python)
date: 2019-08-27 01:00:00 am
permalink: posts/77
description: AWS Lambda를 사용하기 전 Docker로 테스트하는 법을 알아본다.
categories: [Data, DataOps]
tags: [AWS, Lambda, Layer, Python]
---

> AWS Lambda를 사용하기 전 Docker로 테스트하는 법을 알아본다.


#### [docker-lambda](https://hub.docker.com/r/lambci/lambda){:target="_blank"}라는 유용한 도커 이미지가 존재한다.

![lambda_docker_0]({{site.baseurl}}/assets/img/dataops/lambdadocker_0.png)

docker-lambda에서 빌드형과 실행형, 두 가지 컨테이너를 활용할 수 있다.

## 1. 빌드형 컨테이너

lambci/lambda:build-XXXX 형식으로 언어별로 image를 제공한다.

복잡한 코드를 작성하는 경우, 직접 라이브러리를 설치하고 코드 실행을 확인하는 용도로 적합하다.

``` python
docker run --name test-lambda -it lambci/lambda:build-python3.6 bash
```

    컨테이너 정보

![lambda_docker_1]({{site.baseurl}}/assets/img/dataops/lambdadocker_1.png)

    python에 대한 정보

![lambda_docker_2]({{site.baseurl}}/assets/img/dataops/lambdadocker_2.png)

## 2. 실행형 컨테이너

lambci/lambda:XXXX 형식으로 언어별로 image를 제공한다.

### 폴더 구성

실행할 py파일과 Layer로 사용될 폴더를 구성해준다.

Python의 경우, Layer에 포함될 추가 라이브러리들은 **/opt/python**에 위치해야 한다.

AWS 상에서 Layer를 생성할 때는 zip파일을 사용하지만, docker에서는 설치된 그대로를 활용한다.

``` python
# lambda 실행을 위한 폴더 내에서
mkdir -p opt/python
# 필요한 패키지 설치
pip install 패키지 -t opt/python # ubuntu 환경
```

참고 : 사용중인 OS환경에 따라서 라이브러리가 Lambda에서 실행되지 않을 수 있으므로

빌드형 컨테이너에서 한 폴더에 모두 저장한 후 그 폴더를 활용하는 것이 안전하다.

    폴더 확인

![lambda_docker_3]({{site.baseurl}}/assets/img/dataops/lambdadocker_3.png)

    lambda_func.py 코드

``` python
import json
import requests
def lambda_handler(event, context):
    return {'statusCode':200, 'body':json.dumps(event['body'])}
```

    실행 결과

``` python
# docker run --rm -v 폴더:/var/task -v 폴더/opt:/opt 이미지 py파일.함수 테스트JSON
docker run --rm -v ~/lambda_layer:/var/task -v ~/lambda_layer/opt:/opt 
    lambci/lambda:python3.6 lambda_func.lambda_handler '{"body":"Trigger Event"}'
```

* /var/task는 함수 코드 py 파일이 담긴 폴더와 연결한다.
* 테스트 데이터는 '{ JSON }' 형식으로 args로 전달한다. 양 끝에 ' '를 반드시 포함

![lambda_docker_4]({{site.baseurl}}/assets/img/dataops/lambdadocker_4.png)

이 python 폴더를 zip파일로 압축해서 Layer로 생성할 수 있다.

``` python
~/lambda_layer/opt
➜ zip -r lambda-layer-1.zip python
```

`References` : 

* [Going Serverless with AWS Lambda Functions — 2](https://medium.com/@info.ankitp/going-serverless-with-aws-lambda-functions-2-51a1bd786547){:target="_blank"}

* [AWS 람다(Lambda)로 Python 서버 API 구현하기](https://ndb796.tistory.com/279){:target="_blank"}