---
layout: post
title: SQL로 Date / Time 데이터 다루기 (기초)
date: 2019-07-19 01:00:00 am
update: 2019-07-23 02:00:00 am
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
DATE, DATETIME, TIMESTAMP(시스템 TIME ZONE 포함), ...
```

참고 : [MySQL - Date/Time Types](https://dev.mysql.com/doc/refman/5.7/en/datetime.html){:target="_blank"} / [MYSQL DATETIME VS TIMESTAMP 차이](http://blog.daum.net/_blog/BlogTypeView.do?blogid=03aaf&articleno=12379936&_bloghome_menu=recenttext){:target="_blank"}

#### MySQL의 TIMESTAMP와 PostgreSQL의 TIMESTAMPTZ 비교

MySQL은 'YYYY-MM-DD hh:mm:ss' 데이터를 UTC로 저장 후 return 할 때 TIME ZONE에 따라 return하는 반면,

PostgreSQL은 'YYYY-MM-DD hh:mm:ss**+09**'와 같은 형태로 직접 TIMEZONE 데이터를 INSERT할 수 있다.

### 유용한 함수

|      함수    |     MySQL  |   PostgreSQL    |
| ------------- | --------- |-----------------|
| 오늘            | CURRENT_DATE 또는 CURDATE() |  CURRENT_DATE   |
| 현재 날짜+시간(타임존 O) | CURRENT_TIMESTAMP또는 NOW() | CURRENT_TIMESTAMP 또는 NOW() |
| 현재 날짜+시간(타임존 X) | CURRENT_TIMESTAMP | LOCALTIMESTAMP |

### DATE / TIME 데이터 연산

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

참고 : 'YYYY-MM-DD HH:MM:SS' 문자열을 DATE 타입 선언없이도 자동으로 인식한다.

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

### 특정 단위(일, 월, ...) 추출 또는 통합

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

