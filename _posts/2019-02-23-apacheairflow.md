---
layout: post
title: Airflow 기본 정보 (상시 업데이트)
date: 2019-02-23 10:00:00 pm
update: 2020-12-13 03:00:00 pm
permalink: posts/airflow
description: Airflow에 대해 정리한 자료
categories: [Data, DataOps]
tags: [Airflow]
---

> 주요 용어

![](https://image.slidesharecdn.com/airflow-191017192342/95/airflow-for-beginners-4-1024.jpg)
*출처 : https://www.slideshare.net/varyakarpenko5/airflow-for-beginners/4*

## DAG

참고 : [airflow concept - Apply Data Science](https://www.applydatascience.com/airflow/airflow-concept){:target="_blank"}

DAG는 Directed Acyclic Graph의 줄임말이다.

Graph : edge와 node로 이루어진 자료구조

Undirected VS **Directed** : edge가 한 방향으로만 가리킨다.

**Acyclic** VS Cyclic : 한 번 통과한 노드로 다시 돌아오지 않는 Graph

![dag_img]({{site.baseurl}}/assets/img/dataops/dag_img.jpg)

### DagRun & TaskInstance

DagRun과 TaskInstance는 실행중인 DAG의 상태정보를 가지고 있다. 

JINJA 템플릿을 통해 상태정보를 활용할 수도 있고 task 간 데이터를 주고 받을 수도 있다.(xcom)

    DagRun

a DagRun is simply a DAG with **execution_date**.

Dag스케줄러(or Trigger)가 DAG의 execution_date(실행시간)를 정의하고 DagRun이 시간에 맞게 생성된다. 

    TaskInstance

TaskInstance is a task that has been instantiated and has an **execution_date** context. 

하나의 DagRun과 연관된 tasks 즉, 스케줄이 정의된 task를 TaskInstance라고 한다.

![dag_run]({{site.baseurl}}/assets/img/dataops/dag_run.png)

    JINJA 템플릿

[Default Variables](https://airflow.apache.org/macros.html){:target="_blank"}

[템플릿 사용 예시](https://diogoalexandrefranco.github.io/about-airflow-date-macros-ds-and-execution-date/){:target="_blank"}

`실행 구조`

![](https://miro.medium.com/proxy/1*CEojZqU4FWcbOwOTgwttDw.jpeg)
*출처 : https://towardsdatascience.com/why-apache-airflow-is-a-great-choice-for-managing-data-pipelines-48effcce3e41*

Scheduler는 Meta database에 저장된 task에 대한 정보(스케줄, 상태 등)를 관리하고 스케줄에 맞게 task를 Executor에 전달한다.

Executor는 task 수행에 필요한 worker process를 실행한다.

## Executor (worker)
    
    SequentialExector (default)

task 순차 처리 / SQLite3를 backend로 설정 / TEST로 사용 권장

    LocalExecutor
    
task 병렬 처리 가능 / MySQL이나 PostgreSQL을 backend로 설정 / task마다 subprocess를 생성
    
    CeleryExecutor

task를 여러 서버(node)에 분산 처리 가능 (cluster) / Celery backend (RabbitMQ, Redis, …) 설정이 필요

    DaskExecutor

Celery와 같은 역할이지만 Dask로 처리

    KubernetesExecutor

Kubernetes로 cluster 자원을 효율적으로 관리 가능 / 1.10 버전부터 지원

## Backend ( META DB )

참고 : [
Initializing a Database Backend](https://airflow.readthedocs.io/en/stable/howto/initialize-database.html){:target="_blank"}

기본 DB는 SequentialExecutor에 따라 SQLite3로 설정되어 있다.

SQLite3는 동시 접근이 제한되어 DAG가 병렬처리되지 않고 순차처리(SequentialExecutor)가 되는 문제가 있다. 

airflow에서도 MySQL이나 PostgreSQL로 사용할 것을 권장한다. (LocalExecutor부터)

## 옵션설정

참고 : [how to set config](https://airflow.readthedocs.io/en/stable/howto/set-config.html){:target="_blank"}

- 설정 우선순위
1. 환경변수
2. airflow.cfg 파일 내 설정
3. command in airflow.cfg
4. Airflow’s built in defaults

- SLA : Service Level Agreements로 제한 시간 내에 task를 수행하는 지에 대한 확인을 하는 용도, default_args에서 설정 가능

참고 : https://airflow.apache.org/concepts.html#slas

### 보안 관련

[Securing Connections - Airflow document](https://airflow.apache.org/howto/secure-connections.html){:target="_blank"}

airflow는 접속한 비밀번호를 메타데이터에서 그대로 저장하는데 보안을 위해 cryptography 라이브러리의 FERNET 방식을 사용자가 적용해야 한다. 

[Airflow 보안 설정하기 (with RBAC) - by yahwang]({{site.baseurl}}/posts/86){:target="_blank"}

## 시간정보

airflow에서는 **UTC** 시간을 사용한다. TIME ZONE을 설정할 수는 있지만 실제 내부에서는 UTC로 다시 변환하여 처리한다. 

웹 UI나 로그에서도 UTC 시간으로만 확인 가능하다.

[Airflow의 시간정보에 대한 정리 - by yahwang]({{site.baseurl}}/posts/87){:target="_blank"}

## Scheduling

### Scheduler

Scheduler는 interval을 두고 실행할 DAG를 Monitoring한다. ( Airflow는 Streaming 솔루션이 아니다. )

![airflow_heartbeat]({{site.baseurl}}/assets/img/dataops/airflow_heartbeat.png)

Production 환경에서는 **scheduler_heartbeat_sec**를 60초 이상으로 설정하는 것을 추천한다고 한다.

자세한 정보는 아래 references에서 Airflow Schedule Interval 101을 보는 것을 추천한다.

###  스케줄 설정

`schedule_interval` 설정을 통해 스케줄링을 수행  **cron preset / cron expression / datetime.timedelta**

```
cron expression : * * * * * (분, 시간, 일, 월, 요일)

timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
```

[crontab.guru - cron schedule expressions](https://crontab.guru/)

|preset |expression |timedelta |
|-------|-----------|---------------|
|None |||
|@Once|||
|@hourly|'0 * * * *'|tmedelta(hours=1)|
|@daily|'0 0 * * *'|tmedelta(days=1)|
|@weekly|'0 0 * * 0'|tmedelta(weeks=1)|
|@monthly|'0 0 1 * *'||
|@yearly|'0 0 1 1 *'||

참고 : [https://airflow.apache.org/scheduler.html](https://airflow.apache.org/scheduler.html){:target="_blank"}

airflow 스케줄과 execution_date


### execution_date와 start_date

execution_date는 스케줄링 된 실행시간을 의미하고 start_date는 실제 dagrun이 실행된 시간을 의미한다.

일반적으로, hourly 스케줄이 적용된 DAG 중 11시에 스케줄링 된 task는 실제로는 12시에 실행된다. **( + 1 interval )**

추가적인 gap이 존재하는 이유는 scheduler의 interval 설정, 코드 실행 및 META DB 업데이트하는 데 시간이 필요하기 때문이다.

( 아래 이미지는 스케줄링이 적용되지 않았고 interval이 5초로 default 값이 되어 있을 경우이다. )

![airflow_ui_task]({{site.baseurl}}/assets/img/dataops/airflow_execution.png)

### Delay_Between_Tasks

Airflow는 여러 task로 구성된 DAG에서 task 별로 모니터링할 수 있다.

airflow는 DAG 실행 스케줄은 정확하게 따르지만 세부 task 사이에는 **delay**가 존재한다.

default 설치 후 Sample DAG를 실행할 경우에는 task 간 20초 이상의 delay가 생겼다.

옵션 변경을 통해 최적화를 해도 몇 초의 delay는 생길 수 밖에 없다. (airflow의 설계와 관련??)

오래 걸리는 task에서 몇 초는 큰 의미가 없기 때문에 이런 task들을 활용할 때 유용한 도구이다. 

따라서, task 설계도 주의해야 한다. 아래 참고 외에도 여러 방법이 존재하는 듯하다. (webserver, ...)

참고 : [How to reduce airflow dag scheduling latency in production?](https://airflow.apache.org/faq.html#how-to-reduce-airflow-dag-scheduling-latency-in-production){:target="_blank"}

## Variables

참고 : [airflow variables - Apply Data Science](https://www.applydatascience.com/airflow/airflow-variables/){:target="_blank"}

변수를 미리 사용자가 지정하여 DAG를 생성할 때 사용 가능하다.

![airflow_var]({{site.baseurl}}/assets/img/dataops/airflow_var.jpg)


Variable은 메타 DB에 저장되고 .get 함수를 사용할 때마다 매번 접속을 시도한다. 따라서, 변수를 따로따로 만드는 것은 비효율적이다.

JSON 파일에 수많은 변수들을 저장한 뒤에 사용하는 것이 효율적이다.

``` python
from airflow.models import Variable

test = Variable.get("test")
# JSON 파일에서 변수 사용하기
config = Variable.get("config파일명", deserialize_json=True)
var1 = config["var1"]
var2 = config["var2"]
```

## 주의할점

1. upstream의 task가 제대로 수행되었는 지에 대해 reliable하지 않다. (오류는 downstream에서 발견되는 경우가 많음) 따라서, 데이터를 check하는 task가 필요할 수 있다.

2. sensor는 일을 하지 않아도 계속 시스템 자원을 차지한다. 많은 sensor가 사용될 경우, 시스템 자원이 낭비되어 다른 스케줄링에 차질이 생길 수 있다.

## Airflow 버전 업데이트 관리

다음 링크에서 버전 업데이트 시 이전 버전과 호환되지 않는 점들에 대해 알 수 있다. 
- [Updating Aiflow.md](https://github.com/apache/airflow/blob/master/UPDATING.md#updating-airflow){:target="_blank"}

GCP의 Cloud Composer는 Open source 배포 버전보다 하위 버전으로 제공된다.

- [GCP의 Cloud Composer Release Notes](https://cloud.google.com/composer/docs/release-notes){:target="_blank"}

`References` : 

* [Apache Airflow with Kubernetes Executor and MiniKube](https://marclamberti.com/blog/airflow-kubernetes-executor/#Apache_Airflow_with_Kubernetes_Executor_Practice){:target="_blank"}

* [Airflow Executors: Explained](https://www.astronomer.io/guides/airflow-executors-explained/){:target="_blank"} - by Astronomer

* [Understanding Apache Airflow’s key concepts](https://medium.com/@dustinstansbury/understanding-apache-airflows-key-concepts-a96efed52b1a){:target="_blank"}

* [Airflow Schedule Interval 101](https://towardsdatascience.com/airflow-schedule-interval-101-bbdda31cc463){:target="_blank"}


