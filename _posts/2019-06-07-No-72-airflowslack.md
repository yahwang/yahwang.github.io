---
layout: post
title: Airflow에서 slack으로 DAG 실패 메세지 보내기
date: 2019-06-07 08:00:00 pm
permalink: posts/72
description: Airflow에서 slack으로 DAG 실패 메세지 보내는 법을 알아본다.
categories: [Data, DataOps]
tags: [Airflow, Slack] # add tag
redirect_to: /posts/121
---

> Airflow에서 slack으로 DAG 실패 메세지 보내는 법을 알아본다.

테스트 버전 : 1.10.3

Slack에는 Web Hook을 활용하여 데이터를 보낼 수 있는 기능이 존재한다. 이를 Airflow와 연결하여 메세지를 보낼 수 있다.

### Slack에 Incoming WebHooks App 설치

Incoming WebHooks를 설치하면 Webhook URL을 확인할 수 있다.

여기서 설정한 channel은 나중에 airflow에서 변경할 수 있기 때문에 아무거나 선택해도 상관없는 듯하다.

![airflow_slack_2]({{site.baseurl}}/assets/img/devops/airflow_slack_2.png)

### Airflow Connection 설정

Incoming WebHooks에서 제공하는 Webhook URL을 바탕으로 새로운 Connection을 생성한다.

    Host : https://hooks.slack.com/services # 고정된 값

    Extra : { "webhook_token" : "/..... " } # 나머지 부분

![airflow_slack_1]({{site.baseurl}}/assets/img/devops/airflow_slack_1.png)

### Airflow에서 활용하기 위한 코드

Airflow에서 제공하는 Hook과 Operator를 활용하기 위해서 코드를 일부 수정해서 새로 생성했다.

만든 파일들은 임시로 dags/utils 폴더에 넣어두고 활용했다.

#### slack_webhook_hook_fixed.py

현재 1.10.3 버전으로 설치되는 slack webhook에서 github에서는 이미 수정된 것이 반영되지 못하고 있다.

connection에 설정한 정보를 가져오는 부분에서 문제가 생기는데 이 부분만 수정하면 된다. 

여기서는, 필요한 부분만 수정해서 활용하기 위해 새로운 Hook을 상속받아 만들고 HttpHook.__init__ ... 으로 수정하였다.

![airflow_slack_4]({{site.baseurl}}/assets/img/devops/airflow_slack_4.png)

<script src="https://gist.github.com/yahwang/2fd79ca74aceafacc92a9c9d631e7c59.js"></script>

#### slack_alert.py

아래 두번째 reference에 친절하게 클래스를 생성한 예시를 참고해서 다음처럼 만들었다.

차이점은 여기서는 Operator 대신 Hook을 바로 사용했다는 점이다.

참고 : message에서 사용된 context에 대한 설명은 아래 두번째 reference에 자세히 설명되어 있다.

<script src="https://gist.github.com/yahwang/a0eed32f89abe0e6db1d304e36726815.js"></script>


### DAG 파일에 적용하기

default_args에서 **on_failure_callback**에 적용하면 DAG 실패 시 메세지가 전달된다. on_success_callback은 성공할 때를 의미한다.

참고 : on_failure_callback에서 설정된 함수에는 context가 dict 타입으로 arg로 전달된다.

( context에는 실패한 DAG에 대한 정보가 담겨 있음)

``` python
from utils.slack_alert import SlackAlert

alert = SlackAlert('#airflow') # 채널 입력

# 예시
default_args = {
    "owner": "yahwang",
    "depends_on_past": False,
    "start_date": datetime(2019, 6, 5),
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
    "provide_context": True,
    "on_failure_callback": alert.slack_fail_alert
}

dag = DAG("DAG_TEST", default_args=default_args, schedule_interval='@once')
...
```

![airflow_slack_3]({{site.baseurl}}/assets/img/devops/airflow_slack_3.png)

`References` : 

* [Integrating Slack Alerts in Airflow](https://medium.com/datareply/integrating-slack-alerts-in-airflow-c9dcd155105){:target="_blank"}

* [[Airflow] Slack으로 결과 전달하기](https://moons08.github.io/programming/airflow-slack/){:target="_blank"}