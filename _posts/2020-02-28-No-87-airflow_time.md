---
layout: post
title: Airflow의 시간정보에 대한 정리
date: 2020-02-28 01:00:00 am
permalink: posts/87
description: Airflow의 시간정보에 대한 정리해본다.
categories: [Data, DataOps]
tags: [Airflow, TIMEZONE]
---

> Airflow의 시간정보에 대한 정리해본다.

### Airflow는 UTC TIMEZONE으로 처리

Airflow는 **aware** datetime objects를 사용하고 **UTC** TIMEZONE을 기반으로 처리한다.

*단, 사용자는 DAG의 start_date나 end_date를 설정할 때는 자신의 TIMEZONE에 맞게 시간을 설정할 수 있다.*

Airflow가 TIMEZONE에 맞게 내부적으로 UTC로 다시 변환하여 처리한다. 

`주의할 점`

    웹 UI나 LOG는 모두 UTC 시간으로만 확인 가능하다.

참고 : Asia/Seoul은 UTC+09, 우리나라 시간 대비 9시간 전으로 표현된다.

### naive vs aware datetime

TIMEZONE이 없는 object를 naive object, TIMEZONE(tzinfo)이 포함된 object를 aware object라고 표현한다.

airflow에서는 TIMEZONE 변환을 위해 **pendulum** 패키지를 사용한다. aware object 여부는 utcoffset()이라는 함수를 사용한다.

![airflow_time_2]({{site.baseurl}}/assets/img/dataops/airflow_time_2.png)

참고 : naive object를 aware object로 변환하는 경우, 다른 시간이 되기 때문에 주의가 필요하다.

### 사용자용 TIMEZONE 변경

환경변수 AIRFLOW__CORE__DEFAULT_TIMEZONE을 설정하거나 airflow.cfg의 default_timezone 정보를 변경한 후 

airflow upgradedb를 실행하면 된다. (+ 재시작)

    airflow.cfg

``` python
[core]
...
...
# default_timezone = utc
default_timezone = Asia/Seoul
## Pendulum 라이브러리에서 지원하는 timezone 형태
```

![airflow_time_1]({{site.baseurl}}/assets/img/dataops/airflow_time_1.png)

TIMEZONE 설정을 해두면 코드에서 naive datetime object를 사용하더라도 aware object로 변경해준다.

다만, 아주 드물게 오류가 발생할 수 있기 때문에 항상 aware object로 사용하는 것을 권장한다.

### DAG에서 datetime object 활용

#### 1. TIMEZONE을 DAG에 표현

``` python
import pendulum
from datetime import datetime

local_tz = pendulum.timezone("Asia/Seoul")

default_args=dict(
    start_date = datetime(2020, 2, 28, 2, tzinfo=local_tz)
...
```

#### 2. TIMEZONE 설정을 활용

airflow에서 제공하는 timezone의 **datetime** 또는 **make_aware** 함수를 사용할 수 있다.

``` python
from airflow.utils.timezone import datetime

default_args=dict(
    start_date = datetime(2020, 2, 28, 2)
...
```

``` python
from airflow.utils.timezone import make_aware
from datetime import datetime

default_args=dict(
    start_date = make_aware( datetime(2020, 2, 28, 2) )
...
```

`References` : 

* [Airflow - Time Zone](https://airflow.apache.org/docs/stable/configurations-ref.html#default-timezone){:target="_blank"}

* [Github - timezone.py](https://github.com/apache/airflow/blob/master/airflow/utils/timezone.py){:target="_blank"}

* [Working with Datetime Objects and Timezones in Python](https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python#enter-timezones){:target="_blank"}





