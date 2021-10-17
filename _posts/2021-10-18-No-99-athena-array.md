---
layout: post
title: Athena의 Array 타입 활용하기
date: 2021-10-18 01:00:00 am
permalink: posts/99
description: Athena의 Array 타입 활용하는 법을 알아본다.
categories: [Data, ETL]
tags: [Athena, Array]
---

> Athena의 Array 타입 활용하는 법을 알아본다.

# ARRAY 타입 기본 활용

ARRAY는 같은 타입으로만 구성되어야 한다. 중첩 ARRAY도 동일하다.

``` sql
SELECT ARRAY['a','b','c']
-- 중첩 ARRAY ( 정수와 소수는 구분하지 않음 )
SELECT ARRAY[ ARRAY[1,2,3], ARRAY[1.1,2.2,3.0] ]
```

`특정 원소만 추출`

``` sql
WITH
dataset AS (
  SELECT ARRAY[1,2,3] AS items
)
SELECT element_at(items, 1)
FROM dataset
```

`KEY, Value 구조 활용`

ROW 타입을 활용한다.

``` sql
WITH dataset AS (
  SELECT
    CAST(
      ROW(33.33, 128.55) AS ROW(lat REAL, lon REAL)
    ) AS point
)
SELECT point, point.lat, point.lon FROM dataset
```

| point                   | lat   | lon    |
|-------------------------|-------|--------|
| {lat=33.33, lon=128.55} | 33.33 | 128.55 |

`STRING => ARRAY`

``` sql
SELECT regexp_split('a_b_c', '_')
-- [a,b,c]
```

`ARRAY => STRING`

``` sql
SELECT array_join(ARRAY['a','b','c'], '_')
-- a_b_c
```

# UNNEST 활용하기

UNNEST는 ARRAY 내의 데이터와 다른 테이블의 데이터를 JOIN하기 위해서 활용할 수 있다.

CROSS JOIN을 활용하여 하나의 ARRAY를 각각의 row로 분리한다. t( ) 안에 새로운 컬럼명을 지정한다.

``` sql
WITH
dataset AS (
  SELECT 1 AS no, ARRAY['a','b','c'] AS items
  UNION ALL
  SELECT 2 AS no, ARRAY['d','e','f'] AS items
)
SELECT *
FROM dataset, UNNEST(items) AS t(word)
```

| no | items   | word |   
|----|---------|------|
| 1  | [a,b,c] | a    | 
| 1  | [a,b,c] | b    |
| 1  | [a,b,c] | c    | 
| 2  | [d,e,f] | d    | 
| 2  | [d,e,f] | e    | 
| 2  | [d,e,f] | f    | 

## SEQUENCE(start, stop, step) 활용

숫자 타입과 타임스탬프 타입을 지원하며, stop의 value는 포함이다.

``` sql
WITH
dataset AS (
  SELECT SEQUENCE(1, 8, 2) AS items
)
SELECT *
FROM dataset, UNNEST(items) AS t(number)
```

| items        | number | 
|--------------|--------|
| [1, 3, 5, 7] | 1      | 
| [1, 3, 5, 7] | 3      | 
| [1, 3, 5, 7] | 5      | 
| [1, 3, 5, 7] | 7      | 

`TIMESTAMP 데이터`

시계열 데이터를 활용하여 데이터를 처리할 때 유용하다.

``` sql
WITH
dataset AS (
  SELECT SEQUENCE(TIMESTAMP '2021-01-01 00:00:00', TIMESTAMP '2021-01-01 00:03:00', 
    INTERVAL '1' MINUTE) AS items
)
SELECT *
FROM dataset, UNNEST(items) AS t(register_at)
```

| items                                                                       | register_at             |
|-----------------------------------------------------------------------------|-------------------------|
| [2021-01-01 00:01:00.000, 2021-01-01 00:02:00.000, 2021-01-01 00:03:00.000] | 2021-01-01 00:01:00.000 | 
| [2021-01-01 00:01:00.000, 2021-01-01 00:02:00.000, 2021-01-01 00:03:00.000] | 2021-01-01 00:02:00.000 | 
| [2021-01-01 00:01:00.000, 2021-01-01 00:02:00.000, 2021-01-01 00:03:00.000] | 2021-01-01 00:03:00.000 | 

## 집계 함수 사용

`array_agg`

GROUP BY와 함께 사용하면 데이터를 ARRAY로 모을 수 있다. DISTINCT도 사용 가능하다.

array_agg로 데이터를 모아 다른 데이터와 JOIN 후 다시 UNNEST를 활용하면 유용할 수 있다.

``` sql
WITH
dataset AS (
  SELECT 'a' AS id, 1 AS items
  UNION ALL
  SELECT 'a' AS id, 2 AS items
)
SELECT id, array_agg(items) AS arr
FROM dataset
GROUP BY id
```

| id | arr   |
|----|-------|
| a  | [2,1] |

`reduce`

ARRAY 안의 데이터들을 집계하려면 UNNEST를 사용하여 각각의 데이터로 분리 후 GROUP BY + SUM을 사용할 수 있다.

reduce를 사용하면 처리 시간과 데이터 전송을 줄일 수 있다고 한다.

``` sql
WITH
dataset AS (
  SELECT ARRAY[1,2,3,4] AS items
  UNION ALL 
  SELECT ARRAY[5,6,7,8] AS items
)
SELECT items, reduce(items, 0 , (s, x) -> s + x, s -> s) AS total
FROM dataset
```

| items        | total |
|--------------|-------|
| [5, 6, 7, 8] | 26    | 
| [1, 2, 3, 4] | 10    | 

`References` : 

* [[athena] split string into array](https://dittoking.tistory.com/38){:target="_blank"}

* [어레이 쿼리 - Amazon Athena](https://docs.aws.amazon.com/ko_kr/athena/latest/ug/querying-arrays.html){:target="_blank"}