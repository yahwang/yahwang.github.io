---
layout: post
title: Airflow 보안 설정하기 (with RBAC)
date: 2020-02-10 03:00:00 am
update: 2020-02-27 03:00:00 am
permalink: posts/86
description: FAB가 제공하는 기능을 통해 Airflow에 기본 보안을 설정한다.
categories: [Data, DataOps]
tags: [Airflow, RBAC, FERNET_KEY]
---

> FAB가 제공하는 기능을 통해 Airflow에 기본 보안을 설정한다.

    1.10.3 기준

Airflow를 설치할 경우, 기본적으로 보안 옵션이 적용되지 않는다. 1.10 버전부터 webserver UI에서 **Flask-AppBuilder (FAB)**를 지원한다.

FAB는 **authentication**과 **Role-Based Access Control(RBAC)**을 지원한다. authentication은 다양한 방법이 존재하지만, 

여기서는 default 값인 AUTH_DB( DB를 통한 인증 )를 사용한다.

### FERNET_KEY 설정

Airflow는 기본적으로 meta DB에 password 정보를 평문으로 입력한다. 보안을 위해 Fernet 방식(Symmetric key)을 지원한다.

    FERNET_KEY 생성방법

``` python
pip install 'apache-airflow[crypto]'

from cryptography.fernet import Fernet
fernet_key= Fernet.generate_key()
print(fernet_key.decode())
```

생성된 결과를 airflow.cfg의 설정을 변경하거나 AIRFLOW__CORE__FERNET_KEY 환경변수로 설정할 수 있다.

    airflow.cfg

``` python
[core]
...
...
# Secret key to save connection passwords in the db
fernet_key = 
```

참고 : [Airflow - Securing Connections](https://airflow.apache.org/docs/stable/howto/secure-connections.html#securing-connections){:target="_blank"}

### FAB 설정방법

환경변수 **AIRFLOW__WEBSERVER__RBAC**를 True로 설정한다. 또는,

$AIRFLOW_HOME( Default는 ~/airflow) 폴더에 있는 airflow.cfg의 **rbac** 옵션을 True로 설정한다.

    airflow.cfg

``` python
[webserver]
...
...
# Use FAB-based webserver with RBAC feature
rbac = True
```

Airflow를 이미 설치한 경우, 설정 변경 후 airflow upgradedb를 실행한다. $AIRFLOW_HOME에 webserver_config.py가 생기며, 

다음과 같이 확인할 수 있다. ( 지원하는 authentication 타입도 확인 가능 )

![airflow_rbac_1]({{site.baseurl}}/assets/img/dataops/airflow_rbac_1.png)

### Admin user 생성

Airflow를 재실행 후 접속하면 로그인을 요구한다. 

![airflow_rbac_2]({{site.baseurl}}/assets/img/dataops/airflow_rbac_2.png)

CLI command를 활용하여 먼저 Admin 계정을 생성해야 한다. 이후로는 UI를 통해서도 생성할 수 있다.

[Airflow CLI - create_user](https://airflow.apache.org/docs/stable/cli.html#create_user){:target="_blank"}

``` bash
airflow create_user -r Admin [-u USERNAME] [-e EMAIL] [-f FIRSTNAME]
                    [-l LASTNAME] [-p PASSWORD]
```

로그인을 하면 Security 메뉴가 추가된 UI를 확인할 수 있다. ( Data Profiling 메뉴는 보안 옵션으로 인해 새 UI에서는 제거된다고 한다. )

![airflow_rbac_3]({{site.baseurl}}/assets/img/dataops/airflow_rbac_3.png)

RBAC에서 기본 Role은 5가지가 존재하며, 자세한 정보는 링크에서 확인할 수 있다.

[Airflow - RBAC UI Security](https://airflow.apache.org/docs/stable/security.html?highlight=ldap#rbac-ui-security){:target="_blank"}

![airflow_rbac_4]({{site.baseurl}}/assets/img/dataops/airflow_rbac_4.png)

RBAC 기능은 1.10.2 버전 부터 제공하는 **DAG level Access Control**을 함께 적용했을 때 유용하다.

( 이 내용은 따로 작성할 예정임 )

`References` : 

* [Airflow 1.10 - New Webserver UI with Role-Based Access Control](https://github.com/apache/airflow/blob/master/UPDATING.md#new-webserver-ui-with-role-based-access-control){:target="_blank"}

* [Airflow 1.10.2 - DAG level Access Control for new RBAC UI](https://github.com/apache/airflow/blob/master/UPDATING.md#dag-level-access-control-for-new-rbac-ui){:target="_blank"}

