---
layout: post
title: SQL에서 집합 연산자(SET OPERATOR) 활용하기
date: 2019-01-25 01:00:00 am
update: 2019-07-30 08:00:00 pm
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

## UNION & UNION ALL - 공통

``` sql
-- 쿼리가 길어지면 반드시 괄호를 포함해야 한다.
( SELECT col1, col2 FROM table1 ) -- Query 1
UNION
( SELECT col1, col2 FROM table2 ); -- Query 2
```

UNION 대신 **UNION ALL**은 중복결과를 포함한 결과를 나타낸다. UNION은 중복을 제거하는 작업을 해야하기 때문에 UNION ALL이 속도가 빠르다. 

중복 제거가 필요한 지 아닌지에 따라 UNION ALL 활용을 선택할 수 있다.

### UNION + ORDER BY

각 쿼리에서 정렬된 결과를 합쳐야 할 경우, PostgreSQL에서만 정렬된 결과가 제대로 나온다.

MySQL에서는 정렬되지 않은 결과가 나오고 심지어 다른 DB에서는 오류가 생길 수도 있다.

`예시`

``` sql
(SELECT name FROM test ORDER BY name)
UNION ALL
(SELECT name FROM test2 ORDER BY name);
```

[DB Fiddle에서 확인 - PostgreSQL](https://www.db-fiddle.com/f/nV2ZSwHyWjK1gXgiZHrfZp/0){:target="_blank"}

`MySQL에서 해결`

테이블을 구분할 컬럼을 임의로 만들고 UNION한 결과를 서브쿼리로 하고 정렬을 하면 된다.

``` sql
SELECT name
FROM (
  (SELECT name, 1 as ord FROM test ORDER BY name)
  UNION ALL
  (SELECT name, 2 FROM test2 ORDER BY name)
  ) a
ORDER BY ord, name;
```

[DB Fiddle에서 확인 - MySQL](https://www.db-fiddle.com/f/nV2ZSwHyWjK1gXgiZHrfZp/1){:target="_blank"}

## EXCEPT와 INTERSECT

EXCEPT와 INETSECT는 PostgreSQL에서만 활용가능하다.

### MySQL

EXCEPT와 INTERSECT 개념을 활용하기 위해 **JOIN** 연산을 활용한다.

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