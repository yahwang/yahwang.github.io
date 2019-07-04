---
layout: post
title: Superset 대시보드 공유하기
date: 2019-07-03 10:00:00 pm
permalink: posts/73
description: superset에서 생성한 dashboard를 공유한다.
categories: [Data, DataViz]
tags: [Superset, Dashboard, Chart]
---

> Superset에서 생성한 Dashboard를 public하게 공유할 수 있다.

    superset 0.28.1 기준

다음처럼 Dashboard를 공유하여 유용하게 활용할 수 있다.

![dashboard_1]({{site.baseurl}}/assets/img/viz/dashboard_sample.png)

그림 : Django에서 iframe에 dashboard URL을 적용한 경우

### Public 권한 설정

superset은 FAB(Flask App Builder)를 기반으로 권한이 주어진 user만 접근할 수 있다. 

Dashboard만 모니터링하는 user들을 위해서 로그인이 필요없는 Public 권한을 설정할 수 있다.

기본적으로 녹색테두리 권한을 추가하고 Dashboard 내 Chart에 사용되는 테이블들에 대한 권한을 추가하는 방식이다.

**datasource access on [DB].[TABLE]** 이 기본 형식으로 이렇게 선택하면 된다.

datasource access on [DB]라는 권한도 존재하지만 이렇게만 설정하면 Dashboard를 볼 수 없었다.

![dashboard_2]({{site.baseurl}}/assets/img/viz/dashboard_permission.png)

### Dashboard 공유하기

Dashboard URL 주소를 그대로 활용하면 된다. dashboard에 share dashboard라는 기능이 존재하지만 

다음처럼 standalone이라는 파라미터를 활용할 수 없다.

    localhost[서버]:8088/superset/dashboard/1/?standalone=true

standalone은 navigation bar를 숨겨 깔끔하게 해준다. 주로 iframe으로 dashboard를 활용할 때 유용하다.

![dashboard_3]({{site.baseurl}}/assets/img/viz/dashboard_header.png)

그림 : navigation bar가 보일 때 (standalone이 없는 경우)

### iframe으로 활용하기 - config 수정

그냥 URL 자체로도 공유할 수 있지만 특정 웹사이트에서 iframe으로 활용할 수도 있다.

config를 수정해야 하기 때문에 superset_config.py에 내용을 추가한다.

아래 참고 2에 custom config 관련하여 설명해놓았다.

``` python
# superset_config.py에 추가

#HTTP_HEADERS = {'X-Frame-Options': 'SAMEORIGIN'}
# If you need to allow iframes from other domains 
HTTP_HEADERS = {}
```

superset init을 실행해서 config가 적용되도록 해준다. 이후 iframe으로 URL을 설정해서 사용할 수 있다.

#### 참고 1 : URL에 dashboard 이름 명시하기

URL에서 dashboard는 default로 숫자로 구분한다. 다음 그림처럼 설정하면 이름을 명시할 수 있다.

![dashboard_4]({{site.baseurl}}/assets/img/viz/dashboard_name.png)

    localhost[서버]:8088/superset/dashboard/seoulbike

#### 참고 2 : superset에 custom config 파일 만들기

superset_config.py라는 파일을 만들고 PYTHONPATH에 이 파일이 위치한 폴더를 추가해준다. 

예시) export PYTHONPATH=/폴더:$PYTHONPATH

superset_config.py에는 내가 수정할 부분만 추가하면 된다. 그리고 superset init을 실행하면 이런 출력을 확인할 수 있다.

superset init은 최초 실행 이후엔 config를 업데이트하는 용도로 쓰인다.

    Loaded your LOCAL configuration at [/ ... /superset_config.py]

custom config 관련 참고 : [superset configuration](https://superset.incubator.apache.org/installation.html#configuration){:target="_blank"}