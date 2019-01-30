---
layout: post
title: SQL에서 누적합, 누적백분율 활용하기
date: 2019-01-29 21:00:00 pm
permalink: posts/54
description: SQL에서 누적합, 누적백분율 활용하여 분석에 활용한다.
categories: [Tech, SQL]
tags: [PostgreSQL, MySQL, WINDOW FUNCTION, ABC analysis]
---

> SQL에서 누적합, 누적백분율을 활용하여 분석에 활용한다.

데이터는 Kaggle의 [Big Mart Sales](https://www.kaggle.com/brijbhushannanda1979/bigmart-sales-data#Test.csv){:target="_blank"}를 활용하였다. (일부 컬럼만)

이 데이터는 16가지 종류로 분류되는 물건들의 판매량을 포함하고 있다.

`데이터 예시`

|item_identifier|item_type|sales|
|------|---------|------|
|FDA15|	Dairy|	3735.138|
|DRC01|	Soft Drinks|	443.4228|
|FDN15|	Meat|	2097.27|
|FDX07|	Fruits and Vegetables|	732.38|
|NCD19|	Household|	994.7052|

## 누적합, 누적백분율

WINDOW FUNCTION을 활용하면 쉽게 구할 수 있다. SUM 함수는 OVER에 아무 조건을 걸지 않으면 총합을 의미하고, ORDER BY 조건을 걸면 정렬된 순서대로 누적합을 계산한다. 백분율 계산식만 간단히 세우면 누적백분율도 계산할 수 있다.

``` sql
WITH total_sales AS(
    SELECT Item_type, SUM(Item_outlet_sales) as sales 
    FROM martsales
    GROUP BY Item_type ORDER BY sales
)
SELECT item_type, sales, 
       ROUND(100.0*sales / SUM(sales) OVER(), 2) as ratio,
       ROUND(100.0*SUM(sales) OVER(ORDER BY sales DESC)
             / SUM(sales) OVER(), 2) as cum_ratio
FROM total_sales;
-- PostgreSQL의 경우, ROUND(100.0*sales / SUM(sales) OVER()::numeric,2)
```

|item_type|sales|ratio|cum_ratio|
|------|---------|------|
|Fruits and Vegetables|	2820059.8168|15.17|	15.17|
|Snack Foods|	2732786.0870|14.70|	29.87|
|Household|	2055493.7132|11.06|	40.92|
|Frozen Foods|	1825734.7886|9.82|	50.75|
|Dairy|	1522594.0512|8.19|	58.93|
|Canned|	1444151.4926|7.77|	66.70|
|Baking Goods|	1265525.3422|6.81|	73.51|
|Health and Hygiene|	1045200.1378|5.62|	79.13|
|Meat|	917565.6120|4.94|	84.07|
|Soft Drinks|	892897.7220|4.80|	88.87|
|Breads|	553237.1888|2.98|	91.85|
|Hard Drinks|	457793.4272|2.46|	94.31|
|Starchy Foods|	351401.2504|1.89|	96.20|
|Others|	325517.6096|1.75|	97.95|
|Breakfast|	232298.9516|1.25|	99.20|
|Seafood|	148868.2194|0.80|	100.00|

`참고:` 

WITH와 WINDOW FUNCTION이 없는 MySQL 5.x 버전에서는 variable을 활용하여 누적합을 다음과 같이 구할 수 있다. 

CROSS JOIN으로 0으로 초기화된 csum이라는 컬럼을 먼저 만들고 누적합을 계산한다. variable 자체를 테이블에 update를 통해 넣어서 자동으로 계산하는 방법도 있다.

``` sql
SELECT a.Item_type, a.sales, (@csum := @csum + a.sales) as cum_sum
FROM (SELECT Item_type, SUM(Item_outlet_sales) as sales 
	  FROM martsales GROUP BY Item_type ORDER BY sales DESC) a, (SELECT @csum:=0) b;
```

### 활용 - ABC 분석

누적백분율을 활용하면 ABC 분석과 같은 경우에 활용할 수 있다. 

상위 매출 기준으로 70%는 A등급, 25%는 B등급, 5%는 C등급으로 정의해보았다. 

``` sql
WITH total_sales AS(
	SELECT Item_type, SUM(Item_outlet_sales) as sales 
	FROM martsales
	GROUP BY Item_type ORDER BY sales),
total_ratio AS (
    SELECT item_type, sales, 
       ROUND(100.0*SUM(sales) OVER(ORDER BY sales DESC) 
             / SUM(sales) OVER()::numeric,2) as cum_ratio
    FROM total_sales
)
SELECT item_type, cum_ratio, 
	CASE WHEN cum_ratio < 70 THEN 'A' 
	     WHEN cum_ratio < 95 THEN 'B' ELSE 'C' END as item_grade 
FROM total_ratio;
```

|item_type|sales|cum_ratio|item_grade|
|------|---------|------|----------|
|Fruits and Vegetables|	2820059.8168|	15.17|A|
|Snack Foods|	2732786.0870|	29.87|A|
|Household|	2055493.7132|	40.92|A|
|Frozen Foods|	1825734.7886|	50.75|A|
|Dairy|	1522594.0512|	58.93|A|
|Canned|	1444151.4926|	66.70|A|
|Baking Goods|	1265525.3422|	73.51|B|
|Health and Hygiene|	1045200.1378|	79.13|B|
|Meat|	917565.6120|	84.07|B|
|Soft Drinks|	892897.7220|	88.87|B|
|Breads|	553237.1888|	91.85|B|
|Hard Drinks|	457793.4272|	94.31|B|
|Starchy Foods|	351401.2504|	96.20|C|
|Others|	325517.6096|	97.95|C|
|Breakfast|	232298.9516|	99.20|C|
|Seafood|	148868.2194|	100.00|C|