---
layout: post
title: Superset 활용기(5) - 라인 차트 만들기
date: 2019-02-12 02:00:00 pm
permalink: posts/59
description: apache superset을 활용하여 라인 차트(line chart)를 만들어본다.
categories: [Data, DataViz]
tags: [Superset]
---

> apache superset을 활용하여 라인 차트를 만들어본다.

superstore sales sample 데이터를 활용하여 작성하였다.

![superset_line_1]({{site.baseurl}}/assets/img/viz/superset_line_1.jpg)

이미지 출처 : [www.analyticsvidhya.com/blog/2017/07/data-visualisation-made-easy]()

tableau로 만든 다음 그림처럼 연도별 월별 매출 라인 차트를 그려보았다.

### Timeseries Chart 기능

superset에는 Time Series 타입을 위한 차트를 지원한다. Time 메뉴에서 선택가능한 컬럼을 기준으로만 차트를 만들 수 있다. Time column은 DATETIME타입의 컬럼만 자동으로 인식한다.

#### 요약 테이블처럼 가상의 컬럼을 생성하지 않아도 tableau처럼 월, 일, 시간 등을 자동으로 group by 함수를 적용할 수 있다. (하지만 약간 다르다.. 아래 월별 시각화 참고..) 

**Time Grain**에서 원하는 단위를 선택할 수 있다. **Time range**는 내가 원하는 기간을 특정하여 차트를 그릴 수 있게 하는 기능이다.

![superset_line_2]({{site.baseurl}}/assets/img/viz/superset_line_2.jpg)

#### 월별 시각화

1-12월까지 연도를 제외한 월별로만 집계하는 것을 superset에서 아직 지원하지 않는다. 다른 기준들도 마찬가지다. 보통, 요일별 월별 일별 이런 차트를 만드는 경우가 있는데 superset에서는 아직 그런 차트를 만들기 어렵다.

superset에서는 Time Grain에 따라 시간을 확장하거나 축소해서 표현만 할 수 있다. 예로, Month를 선택해도 연도는 항상 포함되어 시간의 흐름을 보여주는 차트를 만든다. 

![superset_line_3]({{site.baseurl}}/assets/img/viz/superset_line_3.jpg)

특이한 점은 차트 속성에 **Range Filter**가 존재하는데 드래그를 통해 선택한 기간만 차트를 보여줄 수 있다.

![superset_line_4]({{site.baseurl}}/assets/img/viz/superset_line_4.jpg)

#### 시리즈

* [Superset 활용기(1) - mapbox를 활용한 지도 mapping]({{ site.url }}/posts/44)
* [Superset 활용기(2) - postgresql과 연동(docker 활용)]({{ site.url }}/posts/45)
* [Superset 활용기(3) - SQL Lab 활용]({{ site.url }}/posts/50)
* [Superset 활용기(4) - 요약 테이블 만들기]({{ site.url }}/posts/58)
* Superset 활용기(5) - 라인 차트 만들기