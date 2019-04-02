---
layout: post
title: SQL에서 소계, 합계를 계산하는 ROLLUP 활용하기
date: 2018-03-29 10:00:00 pm
update: 2019-01-29 06:00:00 pm
permalink: posts/31
description: SQL에서 소계, 합계를 계산하는 ROLLUP 활용할 수 있는 방법을 알아본다.  # Add post description (optional)
categories: [Data, SQL]
tags: [MySQL, PostgreSQL, GROUP BY, ROLLUP, GROUPING] # add tag
---

> SQL에서 소계, 합계 계산에 유용한 ROLLUP 활용법에 대해 알아본다.

사용할 데이터는 [MySQL reference](https://dev.mysql.com/doc/refman/5.7/en/group-by-modifiers.html){:target="_blank"}에서 가져왔다.

| year | country | product    | profit |
|------|---------|------------|--------|
| 2000 | Finland | Computer   |   1500 |
| 2000 | Finland | Phone      |    100 |
| 2000 | India   | Calculator |    150 |
| 2000 | India   | Computer   |   1200 |
| 2000 | USA     | Calculator |     75 |
| 2000 | USA     | Computer   |   1500 |
| 2001 | Finland | Phone      |     10 |
| 2001 | USA     | Calculator |     50 |
| 2001 | USA     | Computer   |   2700 |
| 2001 | USA     | TV         |    250 |

## ROLLUP 그룹별 집계

ROLLUP을 활용하면 **GROUP BY에서 선택한 기준에 따라 합계**가 구해진다.

모든 product의 profit 합계와 모든 country의 profit 합계(총합)가 구해진다.

### PostgreSQL

PostgreSQL에서는 **ROLLUP(컬럼1, 컬럼2)**  방식을 사용한다.

``` sql
SELECT country, product, sum(profit) FROM sales GROUP BY ROLLUP(country, product);
```

### MySQL

MySQL에서는 ROLLUP 대신 **WITH ROLLUP**을 사용한다.

``` sql
SELECT country, product, sum(profit) FROM sales GROUP BY country, product WITH ROLLUP;
```

ROLLUP 적용 전 (왼쪽) VS ROLLUP을 적용한 모습(오른쪽)

| country | product    | sum(profit) || country | product    | sum(profit) |
|---------|------------|-------------||---------|------------|-------------|
| Finland | Computer   |        1500 || Finland | Computer   |        1500 |
| Finland | Phone      |         110 || Finland | Phone      |         110 |
| India   | Calculator |         150 || **Finland** | **NULL**      |        **1610** |
| India   | Computer   |        1200 || India   | Calculator |         150 |
| USA     | Calculator |         125 || India   | Computer   |        1200 |
| USA     | Computer   |        4200 || **India**   | **NULL**       |        **1350** |
| USA     | TV         |         250 || USA     | Calculator |         125 |
||||| USA     | Computer   |        4200 |
||||| USA     | TV         |         250 |
||||| **USA**     | **NULL**       |        **4575** |
||||| **NULL**    | **NULL**       |        **7535** |

ROLLUP은 집계한 기준값을 NULL값으로 대체한다. **COALESCE**을 활용하면 원하는 텍스트를 넣을 수 있다. 

( MySQL에서는 IFNULL로 대체 가능)

``` sql
SELECT COALESCE(country,"ALL countries") as country, 
       COALESCE(product,"ALL products") as product, 
       sum(profit) FROM sales GROUP BY country, product WITH ROLLUP;
```

| country     | product     | sum(profit) |
|-------------|-------------|-------------|
| Finland     | Computer    |        1500 |
| Finland     | Phone       |         110 |
| Finland     | **ALL products** |        1610 |
| India       | Calculator  |         150 |
| India       | Computer    |        1200 |
| India       | **ALL products** |        1350 |
| USA         | Calculator  |         125 |
| USA         | Computer    |        4200 |
| USA         | TV          |         250 |
| USA         | **ALL products** |        4575 |
| **ALL countries** | **ALL products** |        7535 |

**참고:**

mysql 8.0부터는 Oracle처럼 **GROUPING** 함수를 사용할 수 있다. 결과는 IFNULL을 적용한 쿼리와 같다. 

GROUPING(컬럼) 값은 집계가 위치해야 할 ROW(NULL이 표시되는 지점)에서 1 아니면 0을 리턴한다.

IF문을 통해 그 지점을 다른 문자로 대체할 수 있다.

``` sql
SELECT IF(GROUPING(country),'ALL countries',country), 
       IF(GROUPING(product),'ALL products',country), SUM(profit) 
FROM sales GROUP BY country, product WITH ROLLUP;
```

`References` : 

* [MYSQL ROLLUP 레퍼런스](https://dev.mysql.com/doc/refman/5.7/en/group-by-modifiers.html){:target="_blank"}
