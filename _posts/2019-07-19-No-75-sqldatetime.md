---
layout: post
title: SQL로 Date / Time 데이터 다루기 (기초)
date: 2019-07-19 01:00:00 am
update: 2020-01-19 06:00:00 am
permalink: posts/75
description: SQL로 Date / Time 데이터 다루는 법을 알아본다.
categories: [Data, SQL]
tags: [PostgreSQL, MySQL]
---

> SQL로 Date / Time 데이터 다루는 법을 알아본다.

### 데이터 타입

`PostgreSQL`

```
DATE, TIMESTAMP, TIMESTAMP WITH TIME ZONE(TIMESTAMPTZ), ...
```

참고 : [PostgreSQL - Date/Time Types](https://www.postgresql.org/docs/9.6/datatype-datetime.html){:target="_blank"}

`MySQL`

```
DATE, DATETIME, TIMESTAMP, ...
```

MySQL에서는 TIMESTAMP가 TIME ZONE이 포함된 시간을 의미하며, 

'1970-01-01 00:00:01' UTC ~ '2038-01-19 03:14:07' UTC 까지 가능한 범위가 존재한다.

참고 : [MySQL - Date/Time Types](https://dev.mysql.com/doc/refman/5.7/en/datetime.html){:target="_blank"} / [MYSQL DATETIME VS TIMESTAMP 차이](http://blog.daum.net/_blog/BlogTypeView.do?blogid=03aaf&articleno=12379936&_bloghome_menu=recenttext){:target="_blank"}

#### MySQL의 TIMESTAMP와 PostgreSQL의 TIMESTAMPTZ 비교

입력된 TIMESTAMP 데이터를 UTC로 저장 후 TIME ZONE에 따라 변환하는 방식은 같다.

MySQL은 UTC 시간으로 데이터를 INSERT해야 한다. TIME ZONE 설정에 따라 시간이 변경된다.

단, PostgreSQL은 'YYYY-MM-DD HH:MI:SS**+09**'와 같은 형태로 직접 TIMEZONE이 포함된 데이터를 INSERT할 수 있다.

TIMEZONE에 관계없는 데이터를 사용하려면 MySQL - DATETIME, PostgreSQL - TIMESTAMP 타입을 사용한다.

#### TIMEZONE 설정

`MySQL`

```sql
-- 현재 타임존 확인
SELECT @@global.time_zone, @@session.time_zone;

-- 타임존 변경
SET TIME_ZONE = 'Asia/Seoul';
SET GLOBAL TIME_ZONE = 'Asia/Seoul'; -- root 권한 유저의 경우,
```

영구적으로 적용하려면 my.conf에서 수정

참고 : [mysql timezone 한국으로 설정하기](https://jwkim96.tistory.com/23){:target="_blank"}

[DB Fiddle - MySQL 5에서 확인](https://www.db-fiddle.com/f/xiPc4YT72QgWQEHLan6KPA/0){:target="_blank"}

`PostgreSQL`

영구적으로 적용하려면 postgresql.conf에서 수정

```sql
-- 현재 타임존 확인
SHOW TIMEZONE;
-- GMT는 UTC와 같다.

-- 타임존 변경 (현재 세션에서만 적용)
SET TIME ZONE 'Asia/Seoul';
```

[DB Fiddle - PostgreSQL 에서 확인](https://www.db-fiddle.com/f/3qd8cc1aApg1jaZBr6tuWE/0){:target="_blank"}

참고 : [PostgreSQL Set Time Zone](https://kb.objectrocket.com/postgresql/postgresql-set-time-zone-1064){:target="_blank"} - by ObjectRocket

#### 현재 시간 표시

|      함수    |     MySQL  |   PostgreSQL    |
| ------------- | --------- |-----------------|
| 오늘            | CURRENT_DATE 또는 CURDATE() |  CURRENT_DATE   |
| 현재 날짜+시간 ( 타임존 O ) | CURRENT_TIMESTAMP 또는 NOW() | **LOCALTIMESTAMP** 또는 [CURRENT_TIMESTAMP / NOW()]::TIMESTAMP |
| 현재 날짜+시간 ( UTC ) | UTC_TIMESTAMP | CURRENT_TIMESTAMP 또는 NOW() |

PostgreSQL에서는 ::TIMESTAMP 없이 CURRENT_TIMESTAMP나 NOW()를 출력하면 UTC로 출력된다. 

그러나, 내부적으로는 LOCALTIMESTAMP와 같다고 인식한다.

### 0. 입출력 형식

둘 다 'YYYY-MM-DD HH:MM:SS' 과 'YYYY-MM-DD**T**HH:MM:SS' 형식을 지원한다.

`MySQL`

'YYYY-MM-DD HH:MM:SS' 문자열을 DATE 타입 선언없이도 자동으로 인식한다. TIMESTAMP 타입으로 따로 명시하는 방법은 없다.

```sql
SELECT DATE "2019-09-09";
-- TIMESTAMP라고 표현하지만(SQL 표준 방식 적용) DATETIME 타입이다. 
SELECT TIMESTAMP "2019-09-09 13:00:00";
```

`PostgreSQL`

뒤에 ::을 붙이는 방식으로도 타입 표현이 가능하다. (주로 사용되는 패턴)

```sql
SELECT "2019-09-09"::DATE;
-- 단위 변환 가능
SELECT "2019-09-09T13:00:00"::DATE; 

SELECT '2019-09-09 13:00:00'::TIMESTAMP;
SELECT '2019-09-09 13:00:00'::TIMESTAMPTZ;
```

#### DATE FORMAT 변환 ( DATE => STRING )

각각의 함수가 존재하며, FORMAT 형식이 다른 것을 주의해야 한다.

`MySQL`

% + 글자 형식으로 사용

``` sql
SELECT DATE_FORMAT("2019-09-09 13:00:00", "%Y-%m-%d");
=> 2019-09-09
```

[MySQL DATE_FORMAT() Function - w3schools](https://www.w3schools.com/sql/func_mysql_date_format.asp){:target="_blank"}

`PostgreSQL`

``` sql
SELECT to_char('2019-09-09T13:00:00'::timestamp, 'YYYY-MM-DD');
=> 2019-09-09
```

[Data Type Formatting - PostgreSQL](https://www.postgresql.org/docs/9.1/functions-formatting.html){:target="_blank"}

### 1. DATE / TIME 데이터 연산

날짜 단위에는 **INTERVAL**을 명시한다.

`PostgreSQL`

일반적인 연산은 +, - 를 통해 계산한다. 

``` sql
-- 더하기
SELECT DATE '2019-01-01' + INTERVAL '6 month'; -- 날짜 단위에 ' '가 필요
-- 빼기
SELECT TIMESTAMP '2019-01-01 18:00' - INTERVAL '2 hour';
```

`MySQL`

MySQL은 함수를 사용해서 계산해야 한다. +, -를 사용할 경우, 잘못된 결과가 나올 수 있기 때문이다.

( +,-로 정확한 계산을 하려면 UNIX_TIMESTAMP로 모두 변환해야 한다. )

``` sql
-- 더하기
SELECT DATE_ADD('2019-01-01', INTERVAL 6 month); -- 날짜 단위에 ' '가 없음
--SELECT '2019-01-01' + INTERVAL 6 month; 도 가능
-- 빼기
SELECT DATE_SUB('2019-01-01 18:00', INTERVAL 2 hour);
```

#### 날짜 차이 계산

`PostgreSQL`

``` sql
-- 날짜 차이
SELECT CURRENT_DATE - DATE '2019-01-01';
-- 특정 단위 차이
SELECT date_part('day', CURRENT_TIMESTAMP - '2019-01-01 13:00'::TIMESTAMP);
```

`MySQL`

``` sql
-- 날짜 차이 ( 1 - 2)
SELECT DATEDIFF(CURDATE(), DATE('2019-01-01'));
-- 특정 단위 차이 ( 2 - 1 )
SELECT TIMESTAMPDIFF(DAY, TIMESTAMP('2019-01-01 13:00'), CURRENT_TIMESTAMP);
```

### 2. 특정 단위(일, 월, ...) 추출 또는 통합

참고: week을 계산하는 방식이 달라 주의가 필요하다.

``` sql
-- PostgreSQL
SELECT EXTRACT(WEEK FROM '2019-07-23'::date);
-- result : 30
-- MySQL
SELECT EXTRACT(WEEK FROM '2019-07-23');
-- result : 29
```

#### 단순 숫자로 추출하는 법

`공통`

``` sql
SELECT EXTRACT(MONTH FROM '2019-01-01 18:00');
-- result : 1
```

`PostgreSQL`

EXTRACT는 호환을 위해 가능하고 실제로는 date_part를 통해 실행된다.

```sql
SELECT date_part('month', TIMESTAMP '2019-01-01 18:00');
```

#### TIMESTAMP 타입을 유지하는 법

`PostgreSQL`

**DATE_TRUNC**를 활용할 수 있다.

``` sql
SELECT DATE_TRUNC('week', '2019-07-23'::date);
-- result : 2019-07-22
```

`MySQL`

**STR_TO_DATE** 함수를 활용하여 구할 수 있다.

``` sql
-- 주의 : week에 1을 더해준다.
SELECT STR_TO_DATE(CONCAT('2019',EXTRACT (week FROM '2019-07-23')+1,'Monday'), '%x %v %W');
-- result : 2019-07-22
```

