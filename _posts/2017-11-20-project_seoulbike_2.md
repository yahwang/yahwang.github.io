---
layout: post
title: 서울자전거 따릉이 지도 시각화
date: 2017-11-20 05:30:00 pm
description: # Add post description (optional)
img: tableau_bike.png # Add image post (optional)
tags: [Project, Tableau] # add tag
---

> 크롤링한 CSV 데이터 기반 태블로를 활용한 지도 시각화 --  

먼저 엑셀을 통해 주소 데이터가 정확하지 못한 부분을 정제했다.

## 데이터 로딩

주소에서 자치구명만을 추출하기 위해 사용자 분할을 사용했다. (구분기호는 스페이스로 설정)

![tableau_bike]({{site.baseurl}}/assets/img/tableau/tableau_bike_1.png)

자치구명 / 위도 / 경도에 `지리적 역할`을 지정한다.

![tableau_bike]({{site.baseurl}}/assets/img/tableau/tableau_bike_2.png)

`데이터 정제가 완료된 형태`

![tableau_bike]({{site.baseurl}}/assets/img/tableau/tableau_bike_3.png)

## 데이터 시각화

위도, 경도를 더블클릭하면 기본적으로 화면에 지도가 나타난다.

대여소 : 세부정보 / 자치구 : 색상에 Drag & Drop 하면 자치구별로 색상이 다르게 대여소 위치가 표시된다.

![tableau_bike]({{site.baseurl}}/assets/img/tableau/tableau_bike_4.png)

### 지도 시각화

자치구를 세부정보에 올리면 자치구별로 색상이 채워진다.

이 때, 인식을 못하는 자치구가 생길 수 있다.

![tableau_bike]({{site.baseurl}}/assets/img/tableau/tableau_bike_5.png)

알 수 없음을 클릭해서 `위치편집`에 들어가 시/도를 서울시로 변경하면 지도에 반영된다.

![tableau_bike]({{site.baseurl}}/assets/img/tableau/tableau_bike_6.png)

좌측 측정값 메뉴 아래 `레코드 수`를 색상에 올리면 대여소 개수를 기준으로 색상의 농도가 정해진다.

![tableau_bike]({{site.baseurl}}/assets/img/tableau/tableau_bike_7.png)

### 두 가지 방식으로 표현하는 이중 축

행에 위치한 `위도`를 Ctrl+Drag로 추가하고 우클릭 - `이중 축`을 선택한다.

![tableau_bike]({{site.baseurl}}/assets/img/tableau/tableau_bike_8.png)

2개의 Layer가 생기게 되는데 2번째 Layer를 수정하면 또 다른 표시를 할 수 있다.

대여소를 세부정보에 올려 대여소 위치를 점으로 시각화했다.

![tableau_bike]({{site.baseurl}}/assets/img/tableau/tableau_bike_9.png)

> 대여소가 점점 늘어날 계획이지만 아직은 특정 지역에 몰려 있고 비어 있는 공간을 확인할 수 있다.

![tableau_bike]({{site.baseurl}}/assets/img/tableau/tableau_bike_10.png)


`Link` : 

* [Tableau Public에서 확인](https://public.tableau.com/profile/.7794#!/vizhome/_16418/sheet0){:target="_blank"}