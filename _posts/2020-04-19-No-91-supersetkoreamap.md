---
layout: post
title: Superset 활용기(6) - Country Map 차트 만들기
date: 2020-04-19 01:00:00 am
permalink: posts/91
description: Superset의 Country Map 차트에서 대한민국을 시각화해본다.
categories: [Data, DataViz]
tags: [Superset]
---

> Superset의 Country Map 차트에서 대한민국을 시각화해본다.

    Superset 0.36 기준

Superset에서 Country Map 차트 기능은 각 나라별 행정 구역 관련 데이터를 시각화하는 용도로 활용된다.

County Map에서는 **ISO 3166-2** 코드를 기준으로 행정구역을 인식하게 되어 있다. 

우리나라는 ISO 3166-2:KR 코드가 존재한다. 자세한 정보는 아래 reference에서 확인 가능하다.

`참고`

OpenSource에 기여하는 경험을 해보기 위해 대한민국 지도를 추가했다. 코드 기여가 아닌 공식문서대로 geojson파일을 생성하고 

List에 Korea 옵션을 추가하는 방식이었다. 2019년 11월에 merge되었지만 0.36버전부터 적용되었다.

### 사용 데이터

시각화 데이터는 e-나라지표에서 제공하는 공공데이터를 사용하였다. 우리나라는 서울시, 경기도 등 17개의 행정구역으로 나누어져 있다.

<script src="https://gist.github.com/yahwang/25b5606d8f07bc1d85596d633f40cbf7.js"></script>

### 지도 시각화

ISO 3166-2 코드가 입력된 컬럼을 설정하고 Country를 Korea로 설정해준다. 

지역 이름이 영어로 표시되는 한계점이 있다. 

<div class="myvideo">
   <img style="display:inline-block;" src="{{ site.baseurl }}/assets/img/viz/countrymap_1.png"> 
   <video style="display:inline-block;" autoplay controls loop="loop">
       <source src="{{ site.baseurl }}/assets/img/viz/countrymap_2.mp4" type="video/mp4" />
   </video>
</div>

`References` : 

* [ISO 3166-2:KR 지리 식별 부호](https://ko.wikipedia.org/wiki/ISO_3166-2:KR){:target="_blank"}

* [Country Map Tools - Apache Superset](https://superset.incubator.apache.org/installation.html){:target="_blank"}


