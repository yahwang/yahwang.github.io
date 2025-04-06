---
layout: post
title: Kibana에서 Map을 활용한 geospatial 필터링 대시보드 구성하기
date: 2025-04-07 01:00:00 am
permalink: posts/119
description: Kibana에서 Map을 활용한 geospatial 필터링 대시보드 구성하는 방법을 알아본다.
categories: [DataViz]
tags: [kibana, map]
---

> Kibana에서 Map을 활용한 geospatial 필터링 대시보드 구성하는 방법을 알아본다.

## 개요

Kibana에서는 Map을 활용하여 geospatial 데이터를 시각화할 수 있다. Map을 활용하면 geospatial 필터링이 가능하다.

아래 영상은 Data table에서 Map에 표현된 영역으로 필터링된 데이터를 보여준다.

데이터는 [서울시 공공와이파이 서비스 위치 정보](https://data.seoul.go.kr/dataList/OA-20883/S/1/datasetView.do){:target="_blank"}를 사용하였다.

`시연 영상`

<div class="myvideo">
   <video style="display:block; max-width:100%; height:auto;" autoplay controls loop="loop">
       <source src="{{ site.baseurl }}/assets/img/viz/kibana_dashboard_map_filter_1.mp4" type="video/mp4" />
   </video>
</div>

## Map 구성

왼쪽 아래 Tools 아이콘은 Map에 Geospatial field가 포함된 index를 Layer에 추가해야 활성화된다.

![kibana_dashboard_map_filter_3]({{site.baseurl}}/assets/img/viz/kibana_dashboard_map_filter_3.jpg)

Tools를 활용해 Map에 영역을 그리면 필터가 생성되는 것을 확인할 수 있다. 이 필터를 통해 다른 대시보드 패널(Lens, Data table 등)과 

자동으로 연동된다. 대시보드 필터가 모든 패널에 적용되기 때문이다. 

그렇다면 **서로 다른 INDEX라도 이름과 타입이 같은 geospatial field가 존재한다면 연동이 가능하다.**

Map을 단순 영역 필터링으로만 사용한다면 ( 다른 패널의 결과 확인이 중요한 경우 ) 임의의 문서가 1개만 존재하는 index를 생성하더라도 

같은 결과를 얻을 수 있다. ( map-filter index는 coord 필드를 가진 문서 1개만 들어있다. )

대시보드 연산을 줄여서 성능에 도움이 될 수 있지 않을까 생각한다.

![kibana_dashboard_map_filter_4]({{site.baseurl}}/assets/img/viz/kibana_dashboard_map_filter_4.jpg)

## 다중 영역 관리

Map 내에서 기본적으로 영역을 여러 개 그릴 수 있으나 **겹치는 지역**만 필터링된다.

필터를 커스텀하게 만든다면 다중 영역 선택도 가능하다. 아래 템플릿을 보면 must 대신 should를 활용한다.

A영역 또는 B영역+@에 포함되는 데이터를 필터링한다. 단, 영역이 Map에서 보이지는 않는다.

왼쪽이 Map 영역에서 그릴 때 생기는 필터, 오른쪽이 다중 영역을 위한 필터 템플릿이다.

![kibana_dashboard_map_filter_2]({{site.baseurl}}/assets/img/viz/kibana_dashboard_map_filter_2.jpg)

`다중 영역을 위한 템플릿`

<table style="width:100%;">
<tr>
<td style="vertical-align:top; white-space:pre-wrap; text-align:left;">
Map 영역에서 그릴 때 생기는 필터
<pre>
{
  "query": {
    "bool": {
      "must": [
        {
          "exists": {
            "field": "coord"
          }
        },
        {
          "geo_distance": {
            "distance": "0.57km",
            "coord": [
              126.98257,
              37.48555
            ]
          }
        }
      ]
    }
  }
}
</pre>
</td>
<td style="vertical-align:top; white-space:pre-wrap; text-align:left;">
다중 영역 가능한 필터
<pre>
{
  "query": {
    "bool": {
      "should": [
        {
          "bool": {
            "should": [
              {
                "geo_distance": {
                  "distance": "1km",
                  "coord": [
                    126.953148,
                    37.480967
                  ]
                }
              },
              {
                "geo_distance": {
                  "distance": "1km",
                  "coord": [
                    127.0498872,
                    37.5586668
                  ]
                }
              }
            ]
        }}]}}}
</pre>
</td>
</tr>
</table>

> Kibana 대시보드로도 geospatial한 분석이 가능할 것으로 보인다.