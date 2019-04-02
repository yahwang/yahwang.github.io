---
layout: post
title: SQL에서 집합 연산자(SET OPERATOR) 활용하기
date: 2019-01-25 01:00:00 am
permalink: posts/52
description: SQL로 집합 연산자(SET OPERATOR) 활용하는 법을 알아본다.
categories: [Data, SQL]
tags: [PostgreSQL, UNION, EXCEPT, INTERSECT, MySQL]
---

> SQL로 집합 연산자(SET OPERATOR) 활용하는 법을 알아본다.

SQL에는 집합 개념을 활용한 **UNION(합집합), UNION ALL(중복 포함 합집합) INTERSECT(교집합), EXCEPT(차집합)** 연산자가 존재한다.

참고 : Oracle에서는 EXCEPT 대신 MINUS 연산자가 사용된다.

![sql_set_0]({{site.baseurl}}/assets/img/sql/sql_set_0.jpg)

출처 : essentialsql.com/sql-set-operations-sql-server

집합 연산자는 컬럼 이름은 달라도 상관없지만 **컬럼 타입과 컬럼 순서(SELECT 절)**가 같아야 한다. 컬럼 이름이 다를 경우, 마지막 SELECT 절의 컬럼이름을 따른다.

#### MySQL에서는 INTERSECT와 EXCEPT 연산자는 존재하지 않기 때문에 다른 방식을 활용해야 한다.

### PostgreSQL

``` sql
SELECT col1, col2 FROM table1
UNION
SELECT col1, col2 FROM table2;
```

UNION 대신 UNION ALL, EXCEPT, MINUS를 넣을 수 있다.

UNION ALL은 중복결과를 포함한 결과를 나타낸다. UNION은 중복을 제거하는 작업을 해야하기 때문에 UNION ALL이 속도가 빠르다. 중복 제거가 필요한 지 아닌지에 따라 UNION ALL 활용을 선택할 수 있다.

### MySQL

UNION과 UNION ALL 활용은 PostgreSQL과 같다. 

단,  EXCEPT와 INTERSECT 개념을 활용하기 위해 **JOIN** 연산을 활용한다.

#### INTERSECT

모든 컬럼을 key로 INNER JOIN을 실행하면 간단히 해결할 수 있다.

``` sql
SELECT a.col1, a.col2, 
FROM table1 a JOIN table2 b
    ON a.col1 = b.col1 AND a.col2 = B.col2
```

#### EXCEPT

LEFT(RIGHT) JOIN을 실행하면 한쪽 테이블에 존재하지 않는 ROW에 대해 null 값이 생긴다. 이 NULL 값만을 WHERE 절에서 포함하면 된다.

| a.col1 | a.col2 | b.col1 | b.col2 |
|--------|--------|--------|--------|
|   A    |  100   |   NULL |  NULL  |  
|   B    |  200   |   NULL |  NULL  |
|   C    |  300   |   C    |  300   |
|   D    |  400   |   D    |  400   |

``` sql
SELECT a.col1, a.col2, 
FROM table1 a LEFT JOIN table2 b
    ON a.col1 = b.col1 AND a.col2 = b.col2
WHERE b.x IS NULL;
```