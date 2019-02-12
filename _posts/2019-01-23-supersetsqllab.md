---
layout: post
title: Superset 활용기(3) - SQL Lab 활용
date: 2019-01-23 00:00:00 am
permalink: posts/50
description: docker로 만든 apache superset container에 postgresql container를 연동한다.
categories: [Tech, SQL]
tags: [Superset, DB, Postgresql, SQL Lab]
---

> Superset에는 workbench, pgAdmin같은 SQL Lab이라는 기능이 존재한다.

![sqllab_0]({{site.baseurl}}/assets/img/sql/sqllab_0.jpg)

SQL Lab에서 superset에 등록한 테이블을 선택하면, 테이블의 메타데이터와 Preview를 확인할 수 있다.

여기서, 테이블은 CSV파일을 업로드하거나 데이터베이스를 연결한 상태 모두 가능하다.

![sqllab_1]({{site.baseurl}}/assets/img/sql/sqllab_1.jpg)

SQL문을 실행하면 처리시간을 확인할 수 있고 쿼리결과 내에서 검색기능도 지원한다. 쿼리에 오류가 있을 경우, 친절하게 오류 로그를 보여준다.

**.CSV** 버튼을 누르면 CSV 파일로 데이터를 다운받을 수 있고 특히, **Explore** 버튼을 누르면 현재 쿼리 결과를 바탕으로 차트를 만드는 화면으로 이동한다. 쿼리 결과로 CTE처럼 임시 테이블을 만드는 것 같다.  

![sqllab_2]({{site.baseurl}}/assets/img/sql/sqllab_2.jpg)

또한, 쿼리에 대한 **history(log)** 기록이 남고 **save query** 기능으로 자주 사용하는 쿼리를 저장하여 활용할 수도 있다.

#### 시리즈

* [Superset 활용기(1) - mapbox를 활용한 지도 mapping]({{ site.url }}/posts/44)
* [Superset 활용기(2) - postgresql과 연동(docker 활용)]({{ site.url }}/posts/45)
* Superset 활용기(3) - SQL Lab 활용
* [Superset 활용기(4) - 요약 테이블 만들기]({{ site.url }}/posts/58)
* [Superset 활용기(5) - 라인 차트 만들기]({{ site.url }}/posts/59)
