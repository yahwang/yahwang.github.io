---
layout: post
title: CSV 데이터 검증하기(Validation)
date: 2019-04-04 01:00:00 am
permalink: posts/64
description: CSV 데이터의 accuracy와 quality를 보장하기 위해 검증하는 방법을 알아본다.
categories: [Data, ETL]
tags: [Validation, Python, Vladiate]
---

> CSV 데이터의 accuracy와 quality를 보장하기 위해 검증하는 방법을 알아본다.

CSV 파일을 처리(분석)할 때 accuracy와 quality를 보장하기 위해 타입, NULL value 유무, 중복 유무, 이상치 등을 확인해야 한다.

간단한 용도로서 python에서 **vladiate**라는 라이브러리를 활용할 수 있다. 

### vladiate 기본 소개

로컬, S3, StringIO에서 데이터를 읽을 수 있는 함수를 기본으로 제공한다.

다양한 용도로 활용할 수 있는 Validator가 존재한다.

|Validator       |   용도           |
|----------------|------------------|
|UniqueValidator| 중복되는 데이터 확인  |
|SetValidator| Set에 속해있는 지 확인 |
|RangeValidator| 범위에 속해있는 지 확인 |
|NotEmptyValidator| Null Value가 있는 지 확인 |
|IntValidator| Int 타입인 지 확인 |
|RegexValidator| 정규식으로 확인 |
|  ... | ... |

Reference에 있는 github에서 모든 정보를 확인할 수 있다.

### CLI를 활용하는 법

Kaggle의 titanic 데이터의 일부를 활용하여 작성해보았다. 이 데이터는 Null value 등 오류데이터를 포함하고 있다.

먼저, Validator 클래스를 포함한 .py파일을 만들어 놓으면 된다. (default 파일명은 vladfile.py)

``` python
# default
from vladiate import Vlad
from vladiate.validators import UniqueValidator, SetValidator,
     NotEmptyValidator, IntValidator, Ignore
from vladiate.inputs import LocalFile

class TitanicValidator(Vlad): # 클래스명은 상관없음
    #Load Data
    source = LocalFile('titanic_train.csv')

    # validators는 모든 컬럼에 대해 값이 있어야 한다.
    # 한 컬럼에 여러 개의 validator를 동시에 적용할 수 있다.
    validators = {
        'PassengerId': [
            NotEmptyValidator(), UniqueValidator()
        ],
        'Survived': [
            NotEmptyValidator(), SetValidator(['0', '1'])
        ],
        'Name':[Ignore()], # Ignore은 이 컬럼은 무시한다는 뜻
        'Sex':[
            NotEmptyValidator(), SetValidator(['male', 'female'])
        ],
        'Age':[
            NotEmptyValidator(), IntValidator()
        ]    
    }
    # delimiter=',' : default 값 / 다른 문자로 변경 가능
```

CLI에서 실행한 결과는 다음과 같다.

``` python
$ vladiate -l

Available vlads: # 내가 작성한 클래스명 확인 가능
    TitanicValidator 

$ vladiate 
# vladiate -f vladfile.py : 특정 파일명 지정

Validating TitanicValidator(source=LocalFile('titanic_train.csv'))
Failed :(
  NotEmptyValidator failed 177 time(s) (19.9%) on field: 'Age'
  IntValidator failed 202 time(s) (22.7%) on field: 'Age'
    Invalid fields: ['', '34.5', '40.5', '36.5', '20.5', ... ]
```

### 직접 함수로 실행하는 방법

``` python
from vladiate import Vlad
from vladiate.validators import UniqueValidator, SetValidator
from vladiate.inputs import LocalFile

source = LocalFile('test.csv')
validators = {
        'Column A': [
            UniqueValidator()
        ],
        'Column B': [
            UniqueValidator(), SetValidator(['A', 'B'])
        ]
}

# Vlad는 클래스이다.
Vlad(source=source, validators=validators).validate()
```

`References` : 

* [vladiate Github](https://github.com/di/vladiate){:target="_blank"}