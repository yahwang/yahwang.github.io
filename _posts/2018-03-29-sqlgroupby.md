---
layout: post
title: SQL에서 GROUP BY + @ 활용하기
date: 2018-03-29 10:00:00 pm
permalink: posts/31
description: SQL에서 GROUP BY를 더 유용하게 활용할 수 있는 방법을 알아본다.  # Add post description (optional)
img: thumbnail/sql.jpg  # Add image post (optional)
categories: [Tech]
tags: [SQL, GROUP BY, ROLLUP, GROUP_CONCAT] # add tag
---

> GROUP BY와 함께 사용하면 유용한 GROUP_CONCAT과 ROLLUP 활용법에 대해 알아본다.

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

###  GROUP_CONCAT

GROUP_CONCAT은 **컬럼값들을 하나의 값으로 이어주는 역할**을 한다.

연도, 나라별 각각 다른 profit을 product별로 합쳐본다.

``` sql
SELECT product, GROUP_CONCAT(profit) FROM sales GROUP BY product;
```

| product    | GROUP_CONCAT(profit) |
|------------|----------------------|
| Calculator | 150,75,50            |
| Computer   | 1500,1200,1500,2700  |
| Phone      | 100,10               |
| TV         | 250                  |

GROUP_CONCAT은 함수 내 **DISTINCT**와 **정렬**을 지원한다.

country별 product를 판매량이 높은 순으로 정렬한다.

``` sql
SELECT country, GROUP_CONCAT(DISTINCT product ORDER BY profit DESC) as products 
FROM sales GROUP BY country;
```

| country |        products        |
|---------|------------------------|
| Finland | Computer,Phone         |
| India   | Computer,Calculator    |
| USA     | Computer,TV,Calculator |

또한, **SEPARATOR** 설정도 가능하다.

``` sql
SELECT country, GROUP_CONCAT(DISTINCT product ORDER BY profit DESC SEPARATOR "_") as products 
FROM sales GROUP BY country;
```

| country |        products        |
|---------|------------------------|
| Finland | Computer_Phone         |
| India   | Computer_Calculator    |
| USA     | Computer_TV_Calculator |

**응용편 )** 연도별 판매한 product를 판매량이 높은 순으로 정렬한다.

``` sql
# 먼저 product별 profit 합계를 구한 후 GROUP_CONCAT을 적용했다.

SELECT year, GROUP_CONCAT(product ORDER BY profit DESC) as products
FROM (SELECT year, product, sum(profit) as profit FROM sales GROUP BY product, year) a 
GROUP BY year;
```

| year | products |
|------|-------------------------------|
| 2000 | Computer,Calculator,Phone     |
| 2001 | Computer,TV,Calculator,Phone  |

### ROLLUP 그룹별 집계

ROLLUP을 활용하면 **GROUP BY에서 선택한 기준에 따라 합계**가 구해진다.

모든 product의 profit 합계와 모든 country의 profit 합계(총합)가 구해진다.

``` sql
SELECT country, product, sum(profit) FROM sales GROUP BY country, product;
SELECT country, product, sum(profit) FROM sales GROUP BY country, product with ROLLUP;
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

ROLLUP은 집계한 기준값을 NULL값으로 대체한다. **IFNULL**을 활용하면 원하는 텍스트를 넣을 수 있다.

``` sql
SELECT IFNULL(country,"ALL country") as country, 
       IFNULL(product,"ALL product") as product, 
       sum(profit) FROM sales GROUP BY country, product with ROLLUP;
```

| country     | product     | sum(profit) |
|-------------|-------------|-------------|
| Finland     | Computer    |        1500 |
| Finland     | Phone       |         110 |
| Finland     | **ALL product** |        1610 |
| India       | Calculator  |         150 |
| India       | Computer    |        1200 |
| India       | **ALL product** |        1350 |
| USA         | Calculator  |         125 |
| USA         | Computer    |        4200 |
| USA         | TV          |         250 |
| USA         | **ALL product** |        4575 |
| **ALL country** | **ALL product** |        7535 |

`Link` : 

* [MYSQL ROLLUP 레퍼런스](https://dev.mysql.com/doc/refman/5.7/en/group-by-modifiers.html){:target="_blank"}
* [MYSQL GROUP_CONCAT 레퍼런스](https://www.w3resource.com/mysql/aggregate-functions-and-grouping/aggregate-functions-and-grouping-group_concat.php){:target="_blank"}

