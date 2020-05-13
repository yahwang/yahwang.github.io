---
layout: post
title: AWS Lambda, API Gateway와 연동하기 (with Python)
date: 2019-08-28 07:00:00 pm
permalink: posts/78
description: AWS Lambda와 API Gateway를 연동하는 법을 알아본다.
categories: [Dev, DevOps]
tags: [AWS, Lambda, API Gateway, Python]
---

> AWS Lambda와 API Gateway를 연동하는 법을 알아본다.

Lambda 화면에서 Add trigger를 통해 간편하게 설정할 수 있다.

![lambda_api_1]({{site.baseurl}}/assets/img/devops/lambda_api_1.png)

여기서는 보안목적으로 API KEY를 요청하도록 설정하였다.

![lambda_api_2]({{site.baseurl}}/assets/img/devops/lambda_api_2.png)

### API 확인

생성한 API는 기본적으로 **ANY** 즉, GET, POST, ... 등 모든 METHOD를 처리할 수 있도록 설정되어 있다.

Method Request를 확인해보면 API KEY를 요구하는 것을 알 수 있고,

Integration Request를 확인해보면 **LAMBDA_PROXY**를 거쳐서 LAMDA 함수로 전달되는 것을 확인할 수 있다.


![lambda_api_3]({{site.baseurl}}/assets/img/devops/lambda_api_3.png)

![lambda_api_4]({{site.baseurl}}/assets/img/devops/lambda_api_4.png)

### Lambda Proxy를 활용한 데이터 처리

Lambda Proxy로 인해 lambda_handler 함수의 event, context parameter를 통해 데이터를 받을 수 있다.

    event 파라미터 확인

event JSON에서 유용한 정보는 httpMethod, queryStringParameters, body 등이 있다.

``` python
{
    "resource": "/first_lambda_python",
    "path": "/first_lambda_python",
*** "httpMethod": "GET",
    "headers": {
        "Accept": "*/*",
        "accept-encoding": "gzip, deflate",
       
       ...

    },

*** "queryStringParameters": {
        "param1": "hello",
        "param2": "world!"
    },
    "multiValueQueryStringParameters": {
        "param1": [
            "hello"
        ],
        "param2": [
            "world!"
        ]
    },
    "pathParameters": null,
    "stageVariables": null,
    "requestContext": {
        "resourceId": "3nzg5x",
        "resourcePath": "/first_lambda_python",
        "httpMethod": "GET",

        ...

        "accessKey": null,
        "cognitoAuthenticationProvider": null,
        "user": null
        },
    },
*** "body": "{\"msg\": \"hello! postman\"}", # 임의로 넣음
    "isBase64Encoded": false
}
```

자세한 정보는 [API Gateway에서 Lambda 프록시 통합 설정](https://docs.aws.amazon.com/ko_kr/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format){:target="_blank"}에서 확인할 수 있다.


    lambda_function.py

event 변수는 dict 타입으로 바로 활용가능하다.

여기서는 httpMethod를 활용하여 API METHOD를 구분하고 다른 처리를 구현했다.

주의할 점은 POST로 보낸 데이터는 body에서 **\ 가 포함된 JSON 문자열**로 확인할 수 있다. (위에서 확인)

따라서, json.loads를 활용하여 dict 타입으로 변환해야 한다.

``` python
import json

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        return {
            'statusCode': 200,
            'body': json.dumps(event['queryStringParameters'])
        }
    if event['httpMethod'] == 'POST':
        req_data = json.loads(event['body']) # JSON 문자열 처리
        return {
            'statusCode': 200,
            'body': json.dumps(req_data)
        }
```

### API 확인

#### POST

api key는 header에 x-api-key를 추가하는 형식으로 보낸다.

``` python
$ curl -X POST https://XXX.execute-api.XX.amazonaws.com/test/first_lambda_python 
-H "ContentType:application/json" -H "x-api-key:wFCiBeC1i58ZK9k..." -d '{"msg": "hello! lambda"}'

=> {"msg": "hello! postman"}
```

#### GET

``` python
$ curl -X GET https://XXX.execute-api.XX.amazonaws.com/test/first_lambda_python?param1=hello&
param2=world! -H "x-api-key:wFCiBeC1i58ZK9k..."

=> {"param1": "Hello", "param2": "world!"}
```

GET의 경우, API KEY 없이 처리하기 위해서는 API gateway에서 GET method를 새로 생성하면 된다.

ANY에는 API KEY가 설정되어 있지만, 새로 method를 생성하면 기본적으로 Not required로 설정되어 있다.

마지막 deploy까지 처리해야 API가 새로 정의된다.

![lambda_api_5]({{site.baseurl}}/assets/img/devops/lambda_api_5.png)

``` python
# api-key 없이 GET
$ curl -X GET https://XXX.execute-api.XX.amazonaws.com/test/first_lambda_python?param1=hello&
param2=world!

=> {"param1": "Hello", "param2": "world!"}
```

`References` : 

* [API Gateway와 Lambda를 이용한 RestFul API 생성](https://galid1.tistory.com/398){:target="_blank"}

* [Getting json body in aws Lambda via API gateway - stackoverflow](https://stackoverflow.com/questions/41648467/getting-json-body-in-aws-lambda-via-api-gateway){:target="_blank"}
