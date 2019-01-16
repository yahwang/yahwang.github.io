---
layout: post
title: SQL에서 한 컬럼의 값들을 하나의 값으로 합치기
date: 2019-01-15 10:00:00 am
permalink: posts/46
description: SQL에서 GROUP BY를 더 유용하게 활용할 수 있는 방법을 알아본다.  # Add post description (optional)
categories: [Tech, SQL]
tags: [MySQL, GROUP_CONCAT, PostgreSQL, STRING_AGG] # add tag
---

> GROUP BY와 함께 사용하면 유용한 GROUP_CONCAT과 STRING_AGG 활용법에 대해 알아본다.

데이터 출처 : [MySQL reference](https://dev.mysql.com/doc/refman/5.7/en/group-by-modifiers.html){:target="_blank"}

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

### GROUP_CONCAT과 STRING_AGG 함수는 컬럼값들을 하나의 값으로 합치는 역할을 한다.

컬럼에 해당하는 값이 기준마다 정해져 있지 않고 여러개일 때 알아보는 용도로 유용하다.

예를 들면, 어떤 사람이 마트에서 어떤 물건을 구입했는 지를 확인할 때 각자 구매한 종류가 다를 때 활용할 수 있다. 예제에서도 USA만 TV를 판매했다.

### MySQL - GROUP_CONCAT

연도, 나라별 각각 다른 profit을 product 기준으로 합쳐본다.

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

country별 판매한 (unique한)제품명을 구한다.

``` sql
SELECT country, GROUP_CONCAT(DISTINCT product) as products 
FROM sales GROUP BY country;
```

| country |        products        |
|---------|------------------------|
| Finland | Computer,Phone         |
| India   | Calculator,Computer    |
| USA     | Calculator,Computer,TV |

country별 판매한 (unique한)제품명을 profit 순으로 정렬하여 구한다.

``` sql
SELECT country, GROUP_CONCAT(DISTINCT product ORDER BY profit DESC) as products 
FROM sales WHERE country != 'USA' GROUP BY country ;
-- USA는 calculator가 2개라 위 식 적용세 문제가 있어 생략
```

| country |        products        |
|---------|------------------------|
| Finland | Computer,Phone         |
| India   | Computer,Calculator    |

또한, **SEPARATOR** 설정도 가능하다.

``` sql
SELECT country, GROUP_CONCAT(DISTINCT product SEPARATOR "_") as products 
FROM sales GROUP BY country;
```

| country |        products        |
|---------|------------------------|
| Finland | Computer_Phone         |
| India   | Calculator_Computer    |
| USA     | Calculator_Computer_TV |

### PostgreSQL - STRING_AGG

STRING_AGG 함수는 **SEPERATOR**를 항상 지정해줘야 한다. ( GROUP_CONCAT은 default로 ,를 적용 )

단, 주의할 사항은 profit은 숫자이기 때문에 **VARCHAR** 타입으로 캐스팅을 해줘야 한다.

``` sql
SELECT product, STRING_AGG(CAST(profit AS VARCHAR), ',') FROM sales GROUP BY product;
-- == GROUP_CONCAT(profit)
```

STRING_AGG도 함수 내 **DISTINCT**와 **정렬**을 지원한다. 그러나, 정렬은 다른 컬럼이 아닌 함수 내에 쓰인 컬럼에 대해서만 가능하다. 

( 글자에 대한 정렬만 가능 )

``` sql
SELECT country, STRING_AGG(DISTINCT product, ',' ORDER BY product DESC) FROM sales GROUP BY country;
```

| country |        products        |
|---------|------------------------|
| Finland | Phone,Computer         |
| India   | Computer,Calculator    |
| USA     | TV,Computer,Calculator |

다른 컬럼에 대해 정렬을 하려면 미리 FROM 절에 정렬을 실행한 서브쿼리를 활용해야 한다.

**응용편 )** 연도별 판매한 product를 판매량이 높은 순으로 정렬한다.

먼저, product별 profit 합계를 구한 서브쿼리를 활용한다.

`MySQL`

``` sql
# MySQL은 GROUP_CONCAT 함수 내에서 정렬을 사용한다.
SELECT year, GROUP_CONCAT(product ORDER BY profit DESC) as products
FROM (SELECT year, product, sum(profit) as profit FROM sales GROUP BY product, year) a 
GROUP BY year;
```

`PostrgreSQL`

``` sql
# PostrgreSQL은 FROM 절 서브쿼리에서 먼저 정렬을 하고 그대로 출력한다.
SELECT year, STRING_AGG(product, ',') as products
FROM (SELECT year, product, sum(profit) as profit FROM sales GROUP BY product, year ORDER BY profit DESC) a 
GROUP BY year;
```

| year | products |
|------|-------------------------------|
| 2000 | Computer,Calculator,Phone     |
| 2001 | Computer,TV,Calculator,Phone  |

`References` : 

* [MYSQL GROUP_CONCAT 레퍼런스](https://www.w3resource.com/mysql/aggregate-functions-and-grouping/aggregate-functions-and-grouping-group_concat.php){:target="_blank"}

