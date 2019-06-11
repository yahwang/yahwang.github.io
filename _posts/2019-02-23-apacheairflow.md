---
layout: post
title: Airflow 기본 정보 (상시 업데이트)
date: 2019-02-23 10:00:00 pm
update: 2019-06-06 03:00:00 am
permalink: posts/airflow
description: Airflow에 대해 정리한 자료
categories: [Dev, DevOps]
tags: [Airflow]
---

- [DAG란](#DAG란)
- [옵션 설정](#옵션설정)
- [airflow 내부 DB](#airflow_db)
- [시간정보](#시간정보)
- [Scheduling](#scheduling)
- [Variables](#variables)
- [JINJA 템플릿](#jinja템플릿)
- [기타](#기타)
- [주의할점](#주의할점)

### DAG란

참고 : [airflow concept - Apply Data Science](https://www.applydatascience.com/airflow/airflow-concept){:target="_blank"}

DAG는 Directed Acyclic Graph의 줄임말이다.

Graph : edge와 node로 이루어진 자료구조

Undirected VS **Directed** : edge가 한 방향으로만 가리킨다.

**Acyclic** VS Cyclic : 한 번 통과한 노드로 다시 돌아오지 않는 Graph

![dag_img]({{site.baseurl}}/assets/img/tech/dag_img.jpg)

### 옵션설정

참고 : [how to set config](https://airflow.readthedocs.io/en/stable/howto/set-config.html){:target="_blank"}

- 설정 우선순위
1. 환경변수
2. airflow.cfg 파일 내 설정
3. command in airflow.cfg
4. Airflow’s built in defaults

Docker로 설치할 경우, bash에서 printenv를 통해 환경변수 확인가능

- Executor의 종류
    - SequentialExector: 기본 설정, 한 서버에서 task를 순차처리할 수 있음 / task마다 python interpreter가 실행되어 process를 생성한다.
    - LocalExecutor : 한 서버에서 task들을 병렬처리할 수 있음
    - CeleryExecutor : task를 여러 서버(worker)에 할당하여 처리할 수 있음


- [Securing Connections](https://airflow.apache.org/howto/secure-connections.html){:target="_blank"}

airflow는 접속한 비밀번호를 메타데이터에서 그대로 저장하는데 보안을 위해 cryptography 라이브러리의 FERNET 방식을 사용자가 적용해야 한다. 

참고 : FERNET 방식은 encode와 decode가 같은 대칭키이다.

### airflow_DB

참고 : [
Initializing a Database Backend](https://airflow.readthedocs.io/en/stable/howto/initialize-database.html){:target="_blank"}

기본 DB는 SQLite3로 설정되어 있다. 

SQLite3는 동시 접근이 제한되어 DAG가 병렬처리되지 않고 순차처리(SequentialExecutor)가 되는 문제가 있다. 

airflow 자체에서도 MySQL이나 PostgresSQL로 사용할 것을 권장한다.

SequentialExecutor => Local(Celery)Executor로 변경하여 사용해야 한다.

Docker로 설치할 경우, docker-compose를 통해 PostgreSQL을 새로 구축해 연동하여 서비스를 생성한다.

### 시간정보

참고 : [Time Zone](https://airflow.apache.org/timezone.html){:target="_blank"}

airflow에서는 **UTC** 시간을 사용한다. time zone에 관계없이 실제 내부에서는 UTC로 다시 변환하여 처리한다. 

현재 UI에서는 UTC만 보이도록 설정되어 있다(?)...

    default 타임존 설정방법 ( airflow.cfg 수정 )

``` python
# airflow.cfg
...
# default_timezone = utc
default_timezone = Asia/Seoul
## Pendulum 라이브러리에서 지원하는 timezone 형태
...
```

timezone.datetime을 활용하여 바로 확인 가능하다.

![airflow_var]({{site.baseurl}}/assets/img/tech/airflow_timezone.jpg)

    타임존을 DAG에서 명시하기 위해 **pendulum** 라이브러리를 활용할 수 있다. 

``` python
import pendulum
from datetime import datetime

local_tz = pendulum.timezone("Asia/Seoul")
default_args=dict(
    start_date=datetime(2019, 1, 1, tzinfo=local_tz)
...
```

참고 : tzinfo없이 datetime 라이브러리를 사용하더라도 default_timezone을 기반으로 내부적으로 처리된다고 한다.

### Scheduling

참고 : https://airflow.apache.org/scheduler.html

DAG 생성 시에 사용하는 schedule_interval 변수에 넣는 value를 통해 스케줄링을 수행

가능한 Value : cron preset / cron expression / datetime.timedelta

참고 : 
cron expression : * * * * * (분, 시간, 일, 월, 요일)

timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

|preset |expression |timedelta |
|-------|-----------|---------------|
|None |||
|@Once|||
|@hourly|'0 * * * *'|tmedelta(hours=1)|
|@daily|'0 0 * * *'|tmedelta(days=1)|
|@weekly|'0 0 * * 0'|tmedelta(weeks=1)|
|@monthly|'0 0 1 * *'||
|@yearly|'0 0 1 1 *'||

### Variables

참고 : [airflow variables - Apply Data Science](https://www.applydatascience.com/airflow/airflow-variables/){:target="_blank"}

변수를 미리 사용자가 지정하여 DAG를 생성할 때 사용 가능하다.

![airflow_var]({{site.baseurl}}/assets/img/tech/airflow_var.jpg)


Variable은 메타DB에 저장되고 .get 함수를 사용할 때마다 매번 접속을 시도한다. 따라서, 변수를 따로따로 만드는 것은 비효율적이다.

JSON 파일에 수많은 변수들을 저장한 뒤에 사용하는 것이 효율적이다.

``` python
from airflow.models import Variable

test = Variable.get("test")
# JSON 파일에서 변수 사용하기
config = Variable.get("config파일명", deserialize_json=True)
var1 = config["var1"]
var2 = config["var2"]
```
### JINJA템플릿

[Default Variables](https://airflow.apache.org/macros.html){:target="_blank"}

[템플릿 사용 예시](https://diogoalexandrefranco.github.io/about-airflow-date-macros-ds-and-execution-date/){:target="_blank"}

### 기타

- SLA : Service Level Agreements로 제한 시간 내에 task를 수행하는 지에 대한 확인을 하는 용도, default_args에서 설정 가능

참고 : https://airflow.apache.org/concepts.html#slas


### 주의할점

1. upstream의 task가 제대로 수행되었는 지에 대해 reliable하지 않다. (오류는 downstream에서 발견되는 경우가 많음) 따라서, 데이터를 check하는 task가 필요할 수 있다.

2. sensor는 일을 하지 않아도 계속 시스템 자원을 차지한다. 많은 sensor가 사용될 경우, 시스템 자원이 낭비되어 다른 스케줄링에 차질이 생길 수 있다.

