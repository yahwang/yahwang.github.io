---
layout: post
title: Airflow에서 ExternalTaskSensor 활용 사례
date: 2025-06-22 11:00:00 pm
permalink: posts/126
description: Airflow에서 ExternalTaskSensor를 활용했던 사례를 간단하게 정리한다.
categories: [DataOps]
tags: [airflow, sensor]
---

> Airflow에서 ExternalTaskSensor를 활용했던 사례를 간단하게 정리한다.   

airflow 2.10.5 버전을 기준으로 작성되었다.

## 개요

RAW 데이터를 기준이 되는 Iceberg 테이블에 적재하고, 서비스에 필요한 데이터로 집계하는 파이프라인이 있다.

Iceberg 테이블은 UPSERT가 가능하기 때문에 늦게 들어온 데이터도 시간 파티션에 맞게 적재할 수 있다.

하지만, 기존 DAG는 시간 파티션을 기준으로 실행하기 때문에 늦게 들어온 데이터는 집계 처리가 되지 않았다.

RAW 데이터는 외부에서 들어오는 데이터라 길게는 며칠 전 데이터가 들어오기도 하는 경우가 종종 있다.

집계까지 하나의 DAG로 생성해 사용하고 있었고, backfill을 통해 처리하려고 하니 특정 Task부터 시작하는 것은 불가능했다.

Task 1부터 다시 시작하는 것은 시간이 오래 걸리고 비효율적이어서, 다른 방법을 찾다가 Sensor를 활용한 방법을 찾았다.

![airflow_sensor_use_1]({{site.baseurl}}/assets/img/dataops/airflow_sensor_use_1.png)

집계 처리를 별도의 DAG로 분리하고, Sensor를 활용하여 Iceberg 테이블 DAG의 종료를 기다린다.

과거 데이터 집계를 위한 Backfill을 실행할 경우, Sensor Task를 Skip한 후 집계 처리를 실행한다.

참고: BASE_DAG가 스케줄대로 기존부터 잘 실행되고 있었다면 Sensor가 정상 동작하여 Branch가 굳이 필요 없을 수 있다.

## Sensor 간단 설명

### ExternalTaskSensor

`external_dag_id & external_task_id` : 감지할 DAG와 Task

external_task_id가 None인 경우, external_dag_id의 DAG 전체가 성공할 때까지 기다린다.

`execution_date_fn` : 감지할 DAG의 스케줄과의 시간 차이

스케줄이 동일하다면 사용할 필요는 없지만, 아래 예시와 같은 경우 BASE_DAG는 매시 4분에 실행되고 AGG_DAG는 매시 5분에 실행된다.

**execution_date_fn = lambda execution_date: execution_date.subtract(minutes=1)**

pendulum 객체를 받아 시간 계산을 할 수 있으며, 여기서는 1분 전으로 설정했다. execution_delta를 대신 사용할 수도 있다.

`mode` : sensor 실행 모드

poke는 Sensor Task가 실행되는 동안 계속 실행되고, reschedule은 주기적으로 Sensor Task를 실행한다.

`poke_interval` : task 상태를 감지하는 주기

### BranchPythonOperator

함수를 통해 다음에 실행될 Task의 ID를 반환한다.

여기서는 DAG_RUN의 run_type을 확인하여 backfill이면 agg_task를 실행하고, 아니면 wait_for_iceberg_table을 실행한다.

[BranchPythonOperator - astronomer](https://registry.astronomer.io/providers/apache-airflow/versions/2.10.5/modules/BranchPythonOperator){:target="_blank"}

## 코드 예시

주의할 점은 agg_task에는 trigger_rule을 **TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS** 

또는 **TriggerRule.ONE_SUCCESS**로 설정해야 한다.

ONE_SUCCESS는 다른 upstream Task의 실패 여부와 무관하게 하나의 upstream Task가 성공하기만 하면 된다.

NONE_FAILED_MIN_ONE_SUCCESS는 다른 upstream Task의 실패를 확인한다. 자세한 건 아래 Reference를 참고한다.

DAG 흐름을 보면, agg_task의 upstream Task는 wait_for_iceberg_table과 sensor_branch 2개이지만, 둘 중 하나만 실행되기 때문이다.

![airflow_sensor_use_3]({{site.baseurl}}/assets/img/dataops/airflow_sensor_use_3.png)

`BASE_DAG`

```python
with DAG(
    'BASE_DAG',
    start_date=pendulum.datetime(2025, 6, 1, tz='Asia/Seoul'),
    schedule_interval='4 * * * *',
) as dag:

...
```

`AGG_DAG`

```python
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.state import DagRunState
from airflow import TriggerRule

...

def choose_branch(**context):
    '''
    run_type이 backfill이면 agg_task를 반환하고, 아니면 wait_for_iceberg_table을 반환한다.
    '''
    run_type = context['dag_run'].run_type
    if run_type == 'backfill':
        return 'agg_task'
    else:
        return 'wait_for_iceberg_table'

##############
# DAG 정의
##############

with DAG(
    'AGG_DAG',
    start_date=pendulum.datetime(2025, 6, 1, tz='Asia/Seoul'),
    schedule_interval='5 * * * *',
    catchup=False,
) as dag:

    sensor_branch = BranchPythonOperator(
        task_id='sensor_branch',
        python_callable=choose_branch,
        provide_context=True,
    )

    wait_for_iceberg_table = ExternalTaskSensor(
        task_id='wait_for_iceberg_table',
        external_dag_id='BASE_DAG',
        external_task_id=None,  # DAG 전체 성공을 기다림
        allowed_states=[DagRunState.SUCCESS], # 성공으로 감지할 Task 상태
        failed_states=[DagRunState.FAILED],   # 실패로 감지할 Task 상태
        mode='reschedule',
        poke_interval=30,
        timeout= 60 * 5,   # 이 시간이 지나면 FAILED로 처리
        execution_date_fn=lambda execution_date: execution_date.subtract(minutes=1),
    )

    agg_task = PythonOperator(
        task_id='agg_task',
        python_callable=agg_task,
        provide_context=True,
        trigger_rule=TriggerRule.ONE_SUCCESS,   # 간단한 DAG이므로 ONE_SUCCESS로 설정하였다.
    )

    #############
    # DAG 흐름 정의
    #############
    sensor_branch >> [wait_for_iceberg_table, agg_task]
    (
        wait_for_iceberg_table
        >> agg_task
    )

```

Backfill로 실행할 경우, wait_for_iceberg_table Task가 skip된 것을 확인할 수 있다.

![airflow_sensor_use_2]({{site.baseurl}}/assets/img/dataops/airflow_sensor_use_2.png)


`References` : 

* [ExternalTaskSensor - astronomer](https://registry.astronomer.io/providers/apache-airflow/versions/2.10.5/modules/ExternalTaskSensor){:target="_blank"}

* [[Airflow] branch opeartor랑 trigger_rule로 복잡한 DAG 의존성 설정하기](https://velog.io/@leesh970930/Airflow-branch-opeartor%EB%9E%91-triggerrule%EB%A1%9C-%EB%B3%B5%EC%9E%A1%ED%95%9C-DAG-%EC%9D%98%EC%A1%B4%EC%84%B1-%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0){:target="_blank"}

* [TriggerRule - airflow](https://airflow.apache.org/docs/apache-airflow/2.10.5/core-concepts/dags.html#trigger-rules){:target="_blank"}