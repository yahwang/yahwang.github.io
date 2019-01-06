---
layout: post
title: Superset 활용기(2) - postgresql과 연동(docker 활용)
date: 2019-01-07 01:00:00 am
permalink: posts/45
description: docker로 만든 apache superset container에 postgresql container를 연동한다.
categories: [Tech]
tags: [Superset, DB, Postgresql]
---

> apache superset container에 postgresql container를 연동해본다.

기본적으로 container를 생성하면 bridge라는 네트워크에 연결이 되어있다. 하지만, 이 네트워크에는 이름이 따로 없어서 할당받은 IP를 확인한 후 사용해야 해서 불편하다.

docker network를 새로 만들어 사용하면 **IP주소 대신 컨테이너 이름으로** 네트워크를 사용할 수 있다. 

``` python
# 현재 postgres와 superset 컨테이너를 각각 만들어 놓은 상태이다.
docker network create dataviz # network 생성
docker network connect dataviz postgres # postgresql 컨테이너를 네트워크에 연결
docker network connect dataviz superset # superset 컨테이너를 네트워크에 연결
docker network inspect dataviz # network 정보 확인
```

dataviz라는 네트워크를 만들어 확인해보면 gateway와 이에 맞는각 컨테이너의 IP가 할당되어 있다.

![superset_postgres_2]({{site.baseurl}}/assets/img/tech/superset_postgres_2.jpg)

superset 컨테이너에서 postgres 컨테이너로 ping을 실행해보면 네트워크가 연결되어 있음을 확인할 수 있다.

![superset_postgres_3]({{site.baseurl}}/assets/img/tech/superset_postgres_3.jpg)

superset에서는 **SQLAlchemy** 라이브러리를 사용하며, 기본적으로 sqlite3와 연결되어 있다. Databases에서 + 버튼을 누르면 새로운 DB를 연동할 수 있다.

``` python
# 연결방법
postgresql://[유저]:[비밀번호]@[네트워크]
```

참고 : psycopg2-binary 라이브러리가 설치되어 있어야 postgresql 연결이 가능하다. (pip로 설치)

![superset_postgres_4]({{site.baseurl}}/assets/img/tech/superset_postgres_4.jpg)

차트를 만들어 활용하려면 Sources-tables에서 테이블을 만들어야 한다.

![superset_postgres_6]({{site.baseurl}}/assets/img/tech/superset_postgres_6.jpg)

데이터베이스를 연결 후, superset의 유용한 기능인 **SQL Lab**에서 활용할 수도 있다.

SQL Lab에서 옵션 설정을 통해 csv 업로드 방식이나 직접 SQL문으로 테이블을 만들 수도 있고 UPDATE, DELETE 같은 DML을 활용할 수도 있다.

![superset_postgres_5]({{site.baseurl}}/assets/img/tech/superset_postgres_5.jpg)

