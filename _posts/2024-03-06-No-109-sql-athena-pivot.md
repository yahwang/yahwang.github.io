---
layout: post
title: SQL로 PIVOT 테이블 만들기(2)
date: 2024-03-06 01:00:00 am
permalink: posts/109
description: Athena로 PIVOT 테이블 만드는 방법에 대해 간단히 정리해본다.
categories: [Data, SQL]
tags: [Athena, DuckDB]
---

> SQL로 PIVOT 테이블 만드는 방법에 대해 간단히 정리해본다.

SQL 기준 : `ATHENA` `DuckDB`

아래 stackoverflow 글의 도움을 받아 작성하였다.

## 기준 데이터

```sql
WITH example AS (
    SELECT 'user1' AS user_name, 'A' AS category, 10 AS quantity
    UNION ALL
    SELECT 'user1' AS user_name, 'B' AS category, 20 AS quantity
    UNION ALL
    SELECT 'user1' AS user_name, 'C' AS category, 30 AS quantity
    UNION ALL
    SELECT 'user2' AS user_name, 'A' AS category, 100 AS quantity
    UNION ALL
    SELECT 'user2' AS user_name, 'C' AS category, 50 AS quantity
    UNION ALL
    SELECT 'user3' AS user_name, 'A' AS category, 60 AS quantity
    UNION ALL
    SELECT 'user3' AS user_name, 'B' AS category, 70 AS quantity
)

SELECT *
FROM example
```

|user_name|category|quantity|
|---------|--------|--------|
|user1|A|10|
|user1|B|20|
|user1|C|30|
|user2|A|100|
|user2|C|50|
|user3|A|60|
|user3|B|70|

## PIVOT 테이블 만들기

Athena에서는 `map_agg`라는 함수를 사용한다. 이 함수는 Key, Value 구조로 데이터를 만들어준다.

단, 이미 집계된 데이터에서만 적용해야 한다.

```sql
...

SELECT user_name, map_agg(category, quantity) AS agg
FROM example
GROUP BY user_name
```

|user_name|agg|
|-|-|
|user1|{A=10, B=20, C=30}|
|user2|{A=100, C=50}|
|user3|{A=60, B=70}|


```sql
WITH example AS (
    SELECT 'user1' AS user_name, 'A' AS category, 10 AS quantity
    UNION ALL
    SELECT 'user1' AS user_name, 'B' AS category, 20 AS quantity
    UNION ALL
    SELECT 'user1' AS user_name, 'C' AS category, 30 AS quantity
    UNION ALL
    SELECT 'user2' AS user_name, 'A' AS category, 100 AS quantity
    UNION ALL
    SELECT 'user2' AS user_name, 'C' AS category, 50 AS quantity
    UNION ALL
    SELECT 'user3' AS user_name, 'A' AS category, 60 AS quantity
    UNION ALL
    SELECT 'user3' AS user_name, 'B' AS category, 70 AS quantity
)

SELECT user_name, agg['A'] AS qty_A, agg['B'] AS qty_B, agg['C'] AS qty_C
FROM (
    SELECT user_name, map_agg(category, quantity) AS agg
    FROM example
    GROUP BY user_name
) tmp
```

|user_name|qty_A|qty_B|qty_C|
|-|-|-|-|
|user1|10|20|30|
|user2|100||50|
|user3|60|70||


### DuckDB

DuckDB에서는 `PIVOT` 명령어가 존재한다. 집계 기능까지 제공하기 때문에 좀 더 다양하게 사용할 수 있다.

아래는 수량을 일부 나눈 데이터의 집계까지 하는 방식이다.

```sql
WITH example AS (
    SELECT 'user1' AS user_name, 'A' AS category, 5 AS quantity
    UNION ALL
    SELECT 'user1' AS user_name, 'A' AS category, 5 AS quantity
    UNION ALL
    SELECT 'user1' AS user_name, 'B' AS category, 20 AS quantity
    UNION ALL
    SELECT 'user1' AS user_name, 'C' AS category, 30 AS quantity
    UNION ALL
    SELECT 'user2' AS user_name, 'A' AS category, 50 AS quantity
    UNION ALL
    SELECT 'user2' AS user_name, 'A' AS category, 50 AS quantity
    UNION ALL
    SELECT 'user2' AS user_name, 'C' AS category, 50 AS quantity
    UNION ALL
    SELECT 'user3' AS user_name, 'A' AS category, 60 AS quantity
    UNION ALL
    SELECT 'user3' AS user_name, 'B' AS category, 70 AS quantity
)

PIVOT example ON category USING sum(quantity)
```

|user_name|A|B|C|
|-|-|-|-|
|user1|10|20|30|
|user2|100||50|
|user3|60|70||

`References` : 

* [How to pivot rows into columns in AWS Athena? - stackoverflow](https://stackoverflow.com/questions/48013254/how-to-pivot-rows-into-columns-in-aws-athena){:target="_blank"}

* [PIVOT Statement - DuckDB](https://duckdb.org/docs/sql/statements/pivot){:target="_blank"}

* [SQL로 Pivot Table 만들기](https://yahwang.github.io/posts/76){:target="_blank"}
