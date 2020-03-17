---
layout: post
title: SQL에서 User-Defined Variable 사용하기
date: 2020-03-17 09:00:00 pm
permalink: posts/88
description: SQL에서 User Defined Variable 다루는 법을 알아본다.
categories: [Data, SQL]
tags: [PostgreSQL, MySQL, variable]
---

> SQL에서 User Defined Variable 다루는 법을 알아본다.

SQL 문제를 풀다보면 쿼리가 매우 길어지는 경우가 있다. User Defined Variable을 사용하면 쿼리가 읽기 쉬워지고 오류를 찾기도 쉽다.

보통 Procedure나 함수를 정의할 때 Variable을 사용하지만 여기서는 간단한 adhoc query를 기준으로 다룬다.

## MySQL

변수 이름에 @를 붙이고 := 으로 선언한다. ( = 도 가능)

참고 : Procedure에서는 @없이도 사용가능하며, 이 때는 Local variable이라고 한다. DECLARE로 타입을 먼저 선언한 후 SET으로 값을 초기화할 수 있다.

``` sql
SET @const_int:=100;
SET @txt:='Hello world'; 

SELECT @const_int, @txt;
```

| @const_int | @txt        |
|------------|-------------|
| 100        | Hello world |

WINDOW 함수를 지원하지는 5버전에서는 LAG같은 함수를 variable을 활용해서 구할 수 있다. 참고 : [SQL로 증감률(성장률) 계산하기 - yahwang]({{ site.url }}/posts/74)

`활용 예시`

codesignal의 문제 풀이(일부 수정)다. 두 기준 모두 extreme score(min or max)를 주는 경우를 확인하는 문제이다.

``` sql
SET @min_first:=(SELECT MIN(first_c) FROM scores);
SET @min_second:=(SELECT MIN(second_c) FROM scores);
SET @max_first:=(SELECT MAX(first_c) FROM scores);
SET @max_second:=(SELECT MAX(second_c) FROM scores);
    
SELECT arbiter_id, first_c, second_c
FROM (
    SELECT *,
    (CASE WHEN first_c = @min_first OR first_c = @max_first THEN 1 ELSE 0 END) +
    (CASE WHEN second_c = @min_second OR second_c = @max_second THEN 1 ELSE 0 END) AS passed
    FROM scores) a
WHERE passed = 2;
```


## PostgreSQL

PostgreSQL은 PL/pgSQL에서만 Variable 사용을 허용한다. Stackoverflow의 도움을 받아 **WITH 구문**으로 활용할 수 있다는 점을 배웠다.

    기본 사용법

가독성이 좀 떨어진다.

``` sql
WITH myvar (var1, var2) AS (values(5, 'foo'))  

SELECT * FROM myvar;   
```

| var1 | var2 |
|------|------|
| 5    | foo  |

###  single-value table 활용

하나의 value만 갖는 테이블 자체를 variable처럼 만들어서 활용할 수 있다. PostgreSQL에서만 가능한 특별한 방법인 **( table 테이블 )** 을 사용할 수 있다.

``` sql
WITH 
    const_1 AS ( VALUES('Hello world') ), 
    const_2 AS ( VALUES(100) ) 

SELECT (table const_1) as const_1, (table const_2) as const_2,
        (SELECT * FROM const_1) as const_1_b; 
-- SELECT 쿼리로도 가능
```

| const_1     | const_2 | const_1_b   |
|-------------|---------|-------------|
| Hello world | 100     | Hello world |

`활용 예시`

mysql의 풀이를 postgres 식으로 변형한다.

``` sql
-- WITH 구문과 (table .. ) 활용
WITH 
    min_first AS (SELECT MIN(first_c) FROM scores),
    min_second AS (SELECT MIN(second_c) FROM scores),
    max_first AS (SELECT MAX(first_c) FROM scores),
    max_second AS (SELECT MAX(second_c) FROM scores)
    
SELECT arbiter_id, first_c, second_c
FROM (
    SELECT *,
    (CASE WHEN first_c = (table min_first) OR first_c = (table max_first) THEN 1 ELSE 0 END) +
    (CASE WHEN second_c = (table min_second) OR second_c = (table max_second) THEN 1 ELSE 0 END) AS passed
    FROM scores) a
WHERE passed = 2;
```

`References` : 

* [User-Defined Variables - Mysql Docs](https://dev.mysql.com/doc/refman/5.7/en/user-variables.html){:target="_blank"}

* [How to declare a variable in a PostgreSQL query - stackoverflow](https://stackoverflow.com/questions/1490942/how-to-declare-a-variable-in-a-postgresql-query){:target="_blank"}