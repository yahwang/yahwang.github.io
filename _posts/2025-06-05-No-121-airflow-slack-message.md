---
layout: post
title: Airflow에서 Slack으로 DAG 실패 메시지 보내기 (2025)
date: 2025-06-06 00:00:00 am
permalink: posts/121
description: Airflow에서 Slack으로 DAG 실패 메시지를 보내는 방법을 간단하게 정리한다.
categories: [DataOps]
tags: [airflow, slack]
---

> Airflow에서 Slack으로 DAG 실패 메시지를 보내는 방법을 간단하게 정리한다.

airflow 2.10.5 버전을 기준으로 작성되었다.

## Incoming Webhook 등록

메시지를 보내는 데는 Incoming Webhook으로도 충분하다.

[https://slack.com/marketplace/A0F7XDUAZ](https://slack.com/marketplace/A0F7XDUAZ){:target="_blank"} 링크를 통해 쉽게 URL을 발급받을 수 있다.

![airflow_slack_message_1]({{site.baseurl}}/assets/img/dataops/airflow_slack_message_1.png)

airflow UI에서 connection에서 다음처럼 등록하면 된다.

![airflow_slack_message_2]({{site.baseurl}}/assets/img/dataops/airflow_slack_message_2.png)

## SlackWebhookOperator 활용

**trigger_rule**을 보면 TriggerRule.ONE_FAILED로 설정하였다.

모든 task >> notify_slack task로 각각 연결해야 어떤 task가 실패하든 notify_slack task가 실행된다.

( A >> B >> C >> notify_slack일 경우, A 또는 B가 실패할 경우, notify_slack task가 실행되지 않는다. ) 

```python
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

...

task_fail = BashOperator(
    task_id='task_fail',
    bash_command="echo 'Task Fail' && exit 1",
)

notify_slack = SlackWebhookOperator(
    task_id='notify_slack',
    slack_webhook_conn_id='slack_webhook',
    channel='#airflow-alert',
    icon_emoji=':warning:',
    message=textwrap.dedent(
        """
        *Task*: { { task.task_id } }
        *DAG*: { { dag.dag_id } }
        *URL*: { { task_instance.log_url } }
        """),
    trigger_rule=TriggerRule.ONE_FAILED,
)

task_fail >> notify_slack
```

![airflow_slack_message_4]({{site.baseurl}}/assets/img/dataops/airflow_slack_message_4.png)

`문제점`

1 - 실패한 task의 정보를 알기 어렵다.

context를 통해 현재 notify_slack task에 대해서만 알 수 있다. LOG_URL을 알 수 있지만 도메인과 TASK에 대한 수정이 필요하다.

2 - slack 메시지를 보내는 일이 성공으로 끝나기 때문에 UI에서 DAG RUN이 성공한 것처럼 보일 수 있다.

의도적으로 DAG RUN이 실패 상태로 남도록 실패하는 task를 추가하면, 실패한 DAG RUN을 명확히 확인할 수 있다.

```python

task_after_notify_slack = BashOperator(
    task_id='task_after_notify_slack',
    bash_command="exit 1",
)

notify_slack >> task_after_notify_slack
```

![airflow_slack_message_3]({{site.baseurl}}/assets/img/dataops/airflow_slack_message_3.png)

## on_failure_callback + SlackWebhookHook 활용

on_failure_callback은 TASK 레벨과 DAG 레벨 두 가지를 선택해서 구현할 수 있다.

default_args에 **on_failure_callback**를 설정하면 모든 task에 적용한다.

[Source code for airflow.models.baseoperator](https://airflow.apache.org/docs/apache-airflow/1.10.6/_modules/airflow/models/baseoperator.html){:target="_blank"}

```
:param on_failure_callback: a function to be called when a task instance
    of this task fails. a context dictionary is passed as a single
    parameter to this function. Context contains references to related
    objects to the task instance and is documented under the macros
    section of the API.

```

DAG( ... ) 안에 정의할 경우, DAG가 실패하는 상황에 적용된다. 

[Source code for airflow.models.dag](https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/models/dag.html){:target="_blank"}

```
:param on_failure_callback: A function or list of functions to be called when a DagRun of this dag fails.
    A context dictionary is passed as a single parameter to this function.
```

일반적인 상황에서는 DAG( ... ) 안에 정의하는 것으로 해결될 것으로 보인다.

context를 통해 실패한 task의 정보를 가져올 수 있다. 여기서는 failed_task_instance 변수로 실패한 task의 정보를 가져왔다.

callback 함수로 사용할 때는 **context가 아닌 context로 정의한다. 

retry_handlers는 옵션이지만 on_failure_callback 용도로는 필요할 거 같아서 찾아보았다.

[retry_handler - slack.dev](https://tools.slack.dev/python-slack-sdk/webhook/index.html#retryhandler){:target="_blank"} 정보는 여기서 대략 알 수 있다.

![airflow_slack_message_5]({{site.baseurl}}/assets/img/dataops/airflow_slack_message_5.png)


```python
...
from slack_sdk.http_retry.builtin_handlers import (
    RateLimitErrorRetryHandler,
    ConnectionErrorRetryHandler
)

def send_slack_message(context):

    rate_limit_handler = RateLimitErrorRetryHandler(max_retry_count=3)
    connection_error_handler = ConnectionErrorRetryHandler(max_retry_count=3)

    slack_web_hook = SlackWebhookHook(
        slack_webhook_conn_id='slack_webhook',
        retry_handlers=[rate_limit_handler, connection_error_handler]
    )

    failed_task_instance = context['dag_run'].get_task_instances(state='failed')[0]

    text = textwrap.dedent(f"""
    *Task*: {failed_task_instance.task_id}
    *Dag*: {context['dag'].dag_id}
    *Execution Time*: {context['execution_date'].in_timezone('Asia/Seoul')}
    *URL*: <{context['params']['base_url']}/dags/{failed_task_instance.log_url.split('dags/',1)[1]}|Open in Airflow>
    """)

    data = {
        "text": text,
        "channel": context['params']['channel'],
    }

    if context['params']['icon_emoji']:
        data["icon_emoji"] = context['params']['icon_emoji']
    
    slack_web_hook.send_dict(
        body=data,
        headers={'Content-Type': 'application/json'}
    )

#######
# 기본 설정 정의
#######

default_args = {
    'owner': 'yahwang', 
    'retries': 0,
    'retry_delay': pendulum.duration(seconds=10),
}

params = {
    'base_url': 'https://.....',
    'channel': '#airflow-alert',
    'icon_emoji': ':warning:',
}

#######
# DAG 정의
#######

with DAG(
    dag_id='slack_webhook_test',
    default_args=default_args,
    params=params,
    start_date=pendulum.datetime(2025, 6, 1, tz='Asia/Seoul'),
    schedule_interval="*/1 * * * *",
    catchup=False,
    on_failure_callback=send_slack_message,
    tags=['test']
) as dag:

    task_success = BashOperator(
        task_id='task_success',
        bash_command="echo 'Success on purpose'",
    )

    task_fail = BashOperator(
        task_id='task_fail',
        bash_command="echo 'Failing on purpose' && exit 1",
    )
    
    task_success >> task_fail
```

### callback

[Callbacks - Airflow](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/callbacks.html){:target="_blank"}

callback 함수에서 로그를 출력할 수 있는데 이 로그는 UI에서는 확인할 수 없고 

$AIRFLOW_HOME/logs/scheduler/latest/DAG_FILE.py.log에 직접 접근하면 확인할 수 있다.

`References` : 

* [SlackWebhookOperator Source code - in Airflow](https://airflow.apache.org/docs/apache-airflow-providers-slack/stable/_modules/airflow/providers/slack/operators/slack_webhook.html#SlackWebhookOperator){:target="_blank"}

* [SlackWebhookHook Source code - in Airflow](https://airflow.apache.org/docs/apache-airflow-providers-slack/stable/_modules/airflow/providers/slack/hooks/slack_webhook.html#SlackWebhookHook){:target="_blank"}

* [[Airflow] Airflow DAGs 이상감지, 알림받기, 결과전송 (EmailOperator, Slack)](https://spidyweb.tistory.com/509){:target="_blank"}