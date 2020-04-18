---
layout: post
title: Superset 활용기(4) - 요약 테이블 만들기
date: 2019-02-11 10:00:00 am
update: 2020-04-19 00:00:00 am
permalink: posts/58
description: apache superset을 활용하여 요약 테이블 차트를 만들어본다.
categories: [Data, DataViz]
tags: [Superset]
---

> apache superset을 활용하여 요약 테이블 차트를 만들어본다.

    superset 0.36 기준

superstore sales sample 데이터를 활용하여 작성하였다.

superset으로 tableau처럼 시각화할 수 있다는 생각에 tableau에서 지원하는 기본 시각화 중 테이블 차트를 구현해 보았다.

![superset_table_1]({{site.baseurl}}/assets/img/viz/superset_table_1.jpg)
*이미지 출처 : [analyticsvidhya.com/blog/2017/07/data-visualisation-made-easy](https://www.analyticsvidhya.com/blog/2017/07/data-visualisation-made-easy/){:target="_blank"}*

다음 그림처럼 연도별로 매출과 이익을 계산해야 한다.

### 연도별 grouping을 위한 컬럼 생성

tableau는 연,월,일과 같은 계산을 자동으로 해주지만 superset은 그런 기능이 없기 때문에 새로 컬럼을 만들어야 한다.

Sources - Tables 에서 Edit record 버튼을 누르면 현재 테이블 컬럼에 대한 정보가 나온다. + 버튼을 누르면 새로 컬럼을 생성할 수 있다.

![superset_table_2]({{site.baseurl}}/assets/img/viz/superset_table_2.jpg)

컬럼 이름과 Type을 지정하고 **Expression**에 SQL 표현을 사용하면 된다. 우리가 원하는 연도를 계산하기 위해 EXTRACT 함수를 활용한다.

여기서, 만드는 컬럼은 실제로 생성되는 것이 아니라 VIEW처럼 **가상의 컬럼**을 만드는 것이다. SQL Lab에서 확인해보면 해당 컬럼은 존재하지 않는다. Group by를 구현하기 위해서는 Groupable 박스에 체크도 해야 한다.

![superset_table_3]({{site.baseurl}}/assets/img/viz/superset_table_3.jpg)

### Table View

superset에는 **Table View**라는 이름으로 시각화 방법이 있다. 

제일 먼저 주의할 사항은 테이블에 날짜타입 컬럼이 존재하면 Time range가 미리 설정되어 있을 수 있다. Time range는 특정기간의 데이터만 필터링하는 기능이기 때문에 필요없으므로 **No filter**를 선택해야 한다.

다음, Group by에 미리 만들어 놓은 가상의 연도 컬럼을 지정하고 Metric에 매출과 이익의 합계를 설정하면 된다.

이렇게 하면 연도별로 정렬되지 않는 결과가 나온다. SQL처럼 컬럼이름만으로 정렬이 되지 않는다. 일종의 트릭(??)으로 **COUNT_DISTINCT** 함수를 활용한다.

![superset_table_4]({{site.baseurl}}/assets/img/viz/superset_table_4.jpg)

### 참고 : 컬럼 ALIAS 설정하는 법

기본적으로 Metrics 기능(집계 처리)을 사용할 때 컬럼이 계산식 그대로 노출된다.

컬럼 ALIAS를 사용하기 위해서는 테이블 설정에서 미리 계산식(Metric)에 대해 정의가 필요하다.

Metric과 Verbose Name(옵션)을 활용하고 SQL 계산식만 입력해주면 된다.

![table_metrics_1]({{site.baseurl}}/assets/img/viz/table_metrics_1.png)

`Custom Metric 적용 결과`

![table_metrics_2]({{site.baseurl}}/assets/img/viz/table_metrics_2.png)