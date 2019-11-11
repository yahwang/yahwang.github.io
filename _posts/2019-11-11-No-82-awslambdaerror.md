---
layout: post
title: AWS Lambda에서 Slack으로 오류메시지 보내기
date: 2019-11-11 09:00:00 pm
permalink: posts/82
description: AWS Lambda에서 Slack으로 오류메시지를 보내는 법을 알아본다.
categories: [Data, DevOps]
tags: [AWS, Lambda, Python, Slack]
---

> AWS Lambda에서 Slack으로 오류메시지를 보내는 법을 알아본다.

AWS Lambda는 크게 두 유형으로 볼 수 있다.

- **RequestResponse 호출 유형 (동기식 실행)** e.g.) API Gateway

- **Event 호출 유형(즉, 비동기식 실행)** e.g.) Cloudwatch Event

RequestResponse 호출 유형의 경우, Client가 오류 메시지를 직접 받을 수 있다. 

그러나, Event 호출 유형의 경우, Lambda는 오류 결과를 Cloudwatch Log로만 남길 뿐 Client가 직접 오류를 확인하는 방법이 필요하다.

참고 : 이벤트 소스에 따라 ( e.g. kinesis )실패한 Lambda 함수를 다시 시도할 수 있다고 한다.

### 0. Slack에 메시지 보내는 법

requests를 활용하여 Slack의 webhook URL로 POST 요청을 보낸다. url 변수엔 각자의 webhook url값을 설정하면 된다.

여기서는 webhook url을 환경변수로 설정해서 사용했다. 또한, requests 패키지를 Lambda Layer에 추가하는 작업이 필요하다.

참고 : [AWS Lambda Layers로 Python 패키지 재사용하기](https://beomi.github.io/2018/11/30/using-aws-lambda-layers-on-python3/){:target="_blank"}

    msg_to_slack 기본 구조

<script src="https://gist.github.com/yahwang/ca54d4c2758f5c8115e88dbd26d293d0.js"></script>

### 1. Exception 클래스를 활용하는 법

Exception 클래스를 상속받아 Custom한 클래스를 사용한다.

이 방법을 잘 활용하려면 오류 예상 지점마다 오류 메시지를 직접 설정해야 한다.

    lambda_function.py

``` python
import requests
import json
import os

def msg_to_slack(msg):
    webhook_url = os.environ['webhook_url']
    data = {
        'text':'TASK FAILED! REASON : ' + msg,
        'username': 'FROM AWS LAMBDA',
        'channel': '채널명',
        'icon_emoji': ':robot_face:'
        }
    response = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

def lambda_handler(event, context):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    url = os.environ['webhook_url']
    my_handler = SlackHandler(url)
    logger.addHandler(my_handler)
    
    try:
        a = int('foo')
        
    except:
        raise LambdaError('Task Failed!. REASON : ???')

class LambdaError(Exception):
    
    def __init__(self, msg):
        super().__init__(msg)
        msg_to_slack(msg)
```

    slack 메시지 확인

![lambda_error_2]({{site.baseurl}}/assets/img/devops/lambda_error_2.png)

### 2. Logging 클래스를 활용하는 법

오류 결과 메시지를 확인할 수 있는 방법을 고민하다가 Stackoverflow에서 힌트를 얻어 간단히 구현해봤다.

[Github - Logging의 HTTPHandler](https://github.com/python/cpython/blob/3.8/Lib/logging/handlers.py){:target="_blank"}를 활용하였다.

    MyHandler.py

<script src="https://gist.github.com/yahwang/d9edf0fea26399f3d28fe8aeb48d3bd3.js"></script>

    lambda_function.py

``` python
import json
import logging
import requests
import os 
from MyHandler import SlackHandler 

def lambda_handler(event, context):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    url = os.environ['webhook_url']
    my_handler = SlackHandler(url)
    logger.addHandler(my_handler)
    
    try:
        a = int('foo')
        
    except Exception as e:
        logger.error(e)
       # logger.error(f"User Error Msg : \n {e}") # 유저 메시지를 넣는 방법
       # 유저 메시지를 넣으면 에러 타입을 확인할 수 없다.
```

    lambda 구조 및 slack 메시지 확인

![lambda_error_3]({{site.baseurl}}/assets/img/devops/lambda_error_3.png)

![lambda_error_1]({{site.baseurl}}/assets/img/devops/lambda_error_1.png)

Traceback과 같은 자세한 오류메시지는 Cloudwatch Logs에서 확인할 수 있다.

`References` : 

* [AWS 가이드 - AWS Lambda 함수 오류(Python)](https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/python-exceptions.html){:target="_blank"}