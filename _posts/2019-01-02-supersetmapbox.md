---
layout: post
title: Superset 활용기(1) - mapbox를 활용한 지도 mapping
date: 2019-01-02 03:00:00 pm
permalink: posts/44
description: apache superset을 활용하여 데이터를 시각화해본다.
categories: [Tech, DataViz]
tags: [Superset, Visualization, Mapbox]
---

> Ubuntu에서 apache superset을 활용하여 위경도 데이터를 시각화해본다.

superset은 여러 지도 시각화 기능을 지원하는데, 그 중 **위경도 좌표**를 기반으로 mapbox로 위치를 시각화하는 방법이 있다. 

### MAPBOX 사용 설정

**[mapbox](https://www.mapbox.com/){:target="_blank"}**는 opensource 지도기반 mapping platform이라고 한다. 무료로 사용할 수 있는 양이 많아서 작은 규모의 프로젝트에서는 충분히 사용할 만한 것 같다.

![mapbox_1]({{site.baseurl}}/assets/img/tech/mapbox_1.jpg)

회원가입을 하면 ACCESS TOKEN을 바로 받을 수 있고 이 토큰을 SUPERSET에 적용시키면 된다.

![mapbox_2]({{site.baseurl}}/assets/img/tech/mapbox_2.jpg)

superset을 설치하면 config.py라는 파일이 존재한다. 확인해보면, **MAPBOX_API_KEY**라는 환경변수를 설정해주면 자동으로 superset이 인식하도록 되어있다.

![mapbox_3]({{site.baseurl}}/assets/img/tech/mapbox_3.jpg)

zshrc(bashrc)에 복사한 토큰으로 환경변수를 설정해주었다.

![mapbox_4]({{site.baseurl}}/assets/img/tech/mapbox_4.jpg)

### MAPBOX 시각화

데이터는 따릉이 대여소 주소와 위경도 좌표를 활용하였다.

다음 그림처럼 CSV 파일을 업로드하면 테이블을 만들 수 있다. 추가적인 설정은 건드리지 않아도 괜찮다.

![mapbox_5]({{site.baseurl}}/assets/img/tech/mapbox_5.jpg)

Sources의 Table을 확인하면 새로 만든 테이블을 확인할 수 있고 왼쪽 Edit record 버튼을 누르면 컬럼 편집 메뉴가 나온다. 여기서 lat, lon에 해당하는 컬럼은 `Groupable` 체크박스에 체크를 해야 한다.

![mapbox_6]({{site.baseurl}}/assets/img/tech/mapbox_6.jpg)

Tables에서 테이블명을 클릭하거나 Chart 메뉴에서 차트를 생성할 수 있다.

![mapbox_7]({{site.baseurl}}/assets/img/tech/mapbox_7.jpg)

MAPBOX 시각화의 주 설정은 다음과 같다.

위, 경도를 각각 설정해주고 Group by에도 위경도를 지정해주어야 한다.

참고 : gu_lon,lat은 구별로 묶어서 보기 위함이고 place_lon,lat은 대여소별 각각 보기 위한 컬럼이다.

![mapbox_9]({{site.baseurl}}/assets/img/tech/mapbox_9.jpg)

**Map Style**은 6가지의 지도 스타일을 지원한다.

![mapbox_8]({{site.baseurl}}/assets/img/tech/mapbox_8.jpg)

구별로 대여소 개수에 따라 크기가 다른 점을 그리는 것을 시도했지만 잘 되지 않았다. labeling을 통해 개수를 점 안에 그릴 수는 있는데 점 자체가 작아 잘 보이지 않는다.

**Clustering Radius**는 지도를 축소해서 볼 때 겹치는 포인트의 수를 묶어서 표현하는 단위를 조절해준다.

어느 지역에 몰려있다는 인사이트를 어느 정도 얻을 수 있다.

![mapbox_10]({{site.baseurl}}/assets/img/tech/mapbox_10.jpg)

**필터** 기능을 활용하면 필터에 맞는 데이터에 지도 초점을 맞춰주기도 한다.

여기서는 은평구를 기준으로 했더니 은평구를 초점으로 맞춰주었다.

![mapbox_11]({{site.baseurl}}/assets/img/tech/mapbox_11.jpg)

> mapbox로 단순 mapping에 대해서 살펴보았는데 다른 컬럼을 접목해서 버블 차트처럼 활용이 가능하다면 더 좋을 것 같다.

(그런 예시를 아직 보지 못했다. GEOJSON을 활용하는 방법을 고려해봐야 할 것 같다.)

#### 시리즈

* Superset 활용기(1) - mapbox를 활용한 지도 mapping
* [Superset 활용기(2) - postgresql과 연동(docker 활용)]({{ site.url }}/posts/45)
* [Superset 활용기(3) - SQL Lab 활용]({{ site.url }}/posts/50)
* [Superset 활용기(4) - 요약 테이블 만들기]({{ site.url }}/posts/58)
* [Superset 활용기(5) - 라인 차트 만들기]({{ site.url }}/posts/59)
