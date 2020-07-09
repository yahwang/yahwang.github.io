---
layout: post
title: MySQL과 PostgreSQL Query 차이점 정리
date: 2019-12-17 02:00:00 am
update: 2020-07-09 11:00:00 pm
permalink: posts/mysql-vs-postgres
description: MySQL과 PostgreSQL Query의 차이점을 정리해본다.
categories: [Data, SQL]
tags: [MySQL, PostgreSQL]
---

> MySQL과 PostgreSQL Query의 차이점을 정리해본다. (상시 업데이트)

참고 : 전문적인 내용보다는 참고 용도로 정리하고 있다.

### MySQL의 database == PostgreSQL의 schema

    데이터베이스 구조

MySQL : **database** -> table

PostgreSQL : database -> **schema** -> table

테이블의 집합이라는 의미로 MySQL에서는 database, PostgreSQL에서는 schema가 사용된다.

`PostgreSQL의 database`

PostgreSQL은 하나의 데이터베이스를 기준으로 접속한다. 접속한 데이터베이스명을 표시한다.

![mysql-postgres-1]({{site.baseurl}}/assets/img/sql/mysql-postgres-1.png)

`PostgreSQL의 schema`

PostgreSQL에서 schema를 지정하지 않으면 public을 기본으로 사용한다.

search_path는 schema 탐색 범위를 의미한다.

![mysql-postgres-3]({{site.baseurl}}/assets/img/sql/mysql-postgres-3.png)

### 기본 정보 확인 쿼리

|     쿼리 설명     |      MySQL        |        PostgreSQL      |
|--------------------|-----------------|--------------------|
|데이터베이스(schema) 확인| show databases; | \dn |
|테이블 확인 | show tables; | \dt |

![mysql-postgres-2]({{site.baseurl}}/assets/img/sql/mysql-postgres-2.png)

참고 : PostgreSQL에서 쿼리로 확인하려면 information_schema를 활용하면 된다.

```sql
-- \dt를 쿼리문으로 변환
SELECT table_name, table_schema, table_type
FROM information_schema.tables
WHERE table_schema IN ('public');
```

### 테이블 생성 시 증가하는 컬럼 설정 방법

MySQL은 **AUTO_INCREMENT** 속성 / PostgreSQL은 **serial** 타입으로 지정

참고 : [Using PostgreSQL SERIAL To Create Auto-increment Column](http://www.postgresqltutorial.com/postgresql-serial/)

``` sql
-- MySQL
CREATE TABLE table_name(
   id INT NOT NULL AUTO_INCREMENT,
    ...
-- PostgreSQL
CREATE TABLE table_name(
   id SERIAL,
    ...
```

### *PostgreSQL* 은 작은 따옴표 / 큰 따옴표 사용을 명확히 구분

작은 따옴표(single quote)는 string을 표현하고 큰 따옴표(double quotes)는 컬럼명과 같은 identifier 네이밍에 활용된다.

``` sql
-- MySQL
SELECT "HELLO"; -- => HELLO

-- PostgreSQL
SELECT "HELLO"; -- => Syntax Error
SELECT 'HELLO'; -- => HELLO
SELECT 'HELLO' AS "Postgres String";
```

문자열 안에 작은 따옴표가 들어가야 할 경우, **''** 형태로 사용하면 된다.

``` sql
-- PostgreSQL
SELECT 'yahwang''s blog'; -- => yahwang's blog

-- MySQL - 큰 따옴표 활용 가능
SELECT "yahwang's blog";
SELECT 'yahwang''s blog';
```

참고 : PostgreSQL은 기본적으로 모든 identifier(컬럼명 등)를 lower-case(소문자)로 인식한다.

컬럼명에 대문자가 있다면 "first_Name"처럼 큰 따옴표(double quotes)를 사용해야 한다.

### *PostgreSQL* 은 정수 / 정수를 정수로 계산한다.

타입 캐스트 또는 하나를 실수로 바꾸면 소수점 계산이 가능하다.

``` sql
SELECT 100 / 3;

-- 해결방법
SELECT CAST(100 AS float) / 3;
SELECT 100.0 / 3; 
```

### *PostgreSQL* 은 오른쪽 공백이 들어간 문자를 다르게 인식한다.

참고 : [MySQL에서 'a' = 'a '가 true로 평가된다? - 우아한형제 기술블로그](http://woowabros.github.io/study/2018/02/26/mysql-char-comparison.html#postgresql%EC%9D%80-%EC%99%9C){:target="_blank"}

``` sql
-- MySQL
SELECT 'hello' = 'hello   '; -- => True

-- PostgreSQL
SELECT 'hello' = 'hello   '; -- => False
```

### *MySQL* 은 HAVING 절에 ALIAS를 허용한다.

표준 SQL에서는 SELECT보다 GROUP BY, HAVING 연산이 먼저 수행한다. ( the logical order of processing )

그래서, ALIAS를 허용하지 않는 것이 원칙이다. 그러나, GROUP BY 절에서는 둘 다 ALIAS를 사용할 수 있다. 

단, HAVING 절은 MySQL만 사용 가능하다. ( MySQL에서는 HAVING 절의 ALIAS가 필수인 듯 )

``` sql
-- MySQL
SELECT EXTRACT(MONTH FROM date) as month, SUM(sales) as total_sum
FROM sample
GROUP BY EXTRACT(MONTH FROM date)
HAVING month > 2;
-- HAVING EXTRACT(MONTH FROM date) > 2; 은 오류 발생

-- PostgreSQL
SELECT EXTRACT(MONTH FROM date) as month, SUM(sales) as total_sum
FROM sample
GROUP BY EXTRACT(MONTH FROM date)
HAVING EXTRACT(MONTH FROM date) > 2;
```

주의할 점은 PostgreSQL의 HAVING 절을 MySQL에 사용하면 date 컬럼을 오히려 인식하지 못하는 오류가 생길 수 있다. ( 정확한 이유는 찾지 못함 )

[db-fiddle에서 확인 - MySQL 5](https://www.db-fiddle.com/f/4QGXEPLuaVHpHb4JaKrxkK/0){:target="_blank"}

참고 : [MySQL Handling of GROUP BY](https://dev.mysql.com/doc/refman/5.7/en/group-by-handling.html){:target="_blank"}

## MySQL 특정 함수

`IF 함수`

CASE WHEN 대신 SELECT 절에 활용 가능 ( 쿼리문이 간결해지는 효과 )

``` sql
-- MySQL에만 IF문이 존재
SELECT IF(5-3 > 0, 'TRUE', 'FALSE');

-- PostgreSQL 
SELECT CASE WHEN 5-3 > 0 THEN 'TRUE' ELSE 'FALSE' END;
```

`IFNULL 함수`

IFNULL은 추가 인자로 한 개만 가능 / PostgreSQL에서는 COALESCE 함수로 사용

IFNULL은 첫번째 인자가 NULL이라면 다음 인자값을 리턴하는 의미 

( COALESCE는 NULL이 아닌 값이 처음 나오는 값을 리턴하므로 같은 함수는 아니다. )

``` sql
-- MySQL에만 IFNULL 문이 존재
SELECT IFNULL(NULL, 'IS NULL');

-- PostgreSQL 
SELECT COALESCE(NULL, 'IS NULL');
```