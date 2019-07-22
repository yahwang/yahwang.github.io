---
layout: post
title: SQL로 증감률(성장률) 계산하기
date: 2019-07-14 01:00:00 am
permalink: posts/74
description: SQL로 증감률(성장률) 계산하는 법을 알아본다.
categories: [Data, SQL]
tags: [PostgreSQL, LAG, MySQL]
---

> SQL로 증감률(성장률) 계산하는 법을 알아본다.

`데이터 예시`

| date       | sales |
| ---------- | ----- |
| 2019-01-01 | 50    |
| 2019-01-02 | 70    |
| 2019-01-03 | 30    |
| 2019-02-01 | 60    |
| 2019-02-02 | 80    |
| 2019-02-03 | 40    |
| 2019-03-01 | 100   |
| 2019-03-02 | 120   |
| 2019-03-03 | 80    |
| 2019-04-01 | 130   |
| 2019-04-02 | 150   |
| 2019-04-03 | 135   |

### 1. 월별 합계 구하기

``` sql
SELECT EXTRACT(MONTH FROM date) as month, SUM(sales) as total_sales
FROM sample
GROUP BY EXTRACT(MONTH FROM date);
```

| month | total_sales |
| ----- | ----------- |
| 1     | 150         |
| 2     | 180         |
| 3     | 300         |
| 4     | 415         |

### 2. 전월 데이터를 현재 월의 row에 연결하기

`PostgreSQL`

**LAG** function을 사용하여 이전 월의 데이터를 현재 월의 데이터 row로 가져온다.

``` sql
WITH month_summary AS (
    SELECT EXTRACT(MONTH FROM date) as month, SUM(sales) as total_sales
    FROM sample
    GROUP BY EXTRACT(MONTH FROM date) 
)

SELECT month, total_sales,
       LAG(total_sales,1,'0') OVER (ORDER BY month) as prev_sales
FROM month_summary;
```

`MySQL 5`

MySQL 5에서는 window function을 지원하지 않으므로 변수를 활용하여 구할 수 있다.

주의할 점은 prev_sales를 먼저 정의해야 로직이 성립된다.

``` sql
SET @prev:=0;

SELECT a.month, 
       @prev as prev_sales,
       @prev := a.total_sales as total_sales
FROM (SELECT EXTRACT(MONTH FROM date) as month, SUM(sales) as total_sales
	  FROM sample
	  GROUP BY EXTRACT(MONTH FROM date)) a;
```

| month | total_sales | prev_sales |
| ----- | ----------- | ---------- |
| 1     | 150         | 0          |
| 2     | 180         | 150        |
| 3     | 300         | 180        |
| 4     | 415         | 300        |

### 최종 : 증감률(성장률) 계산하기

prev_sales와 total_sales 데이터를 활용해 계산만 하면 된다.

DB Fiddle 링크에서 직접 확인할 수 있다.

`PostgreSQL`

[DB Fiddle - PostgreSQL](https://www.db-fiddle.com/f/bdmH6M8J6bHfPfq6Lebn28/3){:target="_blank"}

``` sql
WITH month_summary AS (
    SELECT EXTRACT(MONTH FROM date) as month, SUM(sales) as summary
    FROM sample
    GROUP BY EXTRACT(MONTH FROM date) 
)

SELECT month, total_sales, 
       100 * (total_sales - LAG(total_sales,1) OVER (ORDER BY month)) / 
       LAG(total_sales,1) OVER (ORDER BY month) || '%' as growth_rate
FROM month_summary;
```

`MySQL 5`

[DB Fiddle - MySQL 5](https://www.db-fiddle.com/f/kVnjXJwUTzcgtj4ZLvQaKP/8){:target="_blank"}

``` sql
SET @prev:=0;

SELECT a.month, 
       CONCAT(ROUND(100 * CASE @prev WHEN 0 THEN 0
       ELSE (a.total_sales - @prev) / @prev END,0), '%') as growth,
       @prev := a.total_sales as total_sales
FROM (SELECT EXTRACT(MONTH FROM date) as month, SUM(sales) as total_sales
      FROM sample
      GROUP BY EXTRACT(MONTH FROM date)) a;
```

| month | total_sales | growth_rate |
| ----- | ----------- | ----------- |
| 1     | 150         |             |
| 2     | 180         | 20%         |
| 3     | 300         | 66%         |
| 4     | 415         | 38%         |


`References` : 

* [Calculating Month-Over-Month Growth Rate in SQL](http://www.silota.com/docs/recipes/sql-mom-growth-rate.html){:target="_blank"}

* [증감률 구하는 간단한 방법](https://www.theteams.kr/teams/860/post/64454
){:target="_blank"}



