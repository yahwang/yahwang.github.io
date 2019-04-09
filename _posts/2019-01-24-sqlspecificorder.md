---
layout: post
title: SQL로 CUSTOM 값 기준으로 정렬하기
date: 2019-01-24 02:00:00 am
permalink: posts/51
description: SQL로 유저가 정한 CUSTOM한 값을 기준으로 정렬하는 법을 알아본다.
categories: [Data, SQL]
tags: [MySQL, FIELD, PostgreSQL, array_position] # add tag
---

> SQL로 CUSTOM한 값을 기준으로 정렬하는 법을 알아본다.

SQL로 보통 정렬을 실행할 때는 컬럼값을 기준으로 ( e.g.) ORDER BY COL1 DESC, COL2 ASC ) 한다. 

데이터를 분석할 때는 특정값들을 기준으로 정렬할 필요가 있을 수 있다.

예제는 tips 데이터를 사용한다. tips의 day와 time 컬럼에는 다음과 같은 unique한 값이 존재한다.

| day | time|
|-------|------------|
|  Thur, Fri, Sat, Sun    |    Lunch, Dinner   |

참고: MySQL은 case-insensitive(대소문자 구분 X)하고, PostgreSQL은 case-sensitive(대소문자 구분 O)가 default 기준이다. 

### MySQL

MySQL에서는 FIELD라는 function을 지원한다.

사용법 : ORDER BY + **FIELD(Col, val1, val2, ...)**

``` SQL
SELECT * FROM tips 
ORDER BY FIELD(day, 'Thur','Fri','Sat','Sun'), FIELD(time, 'Dinner','Lunch');
```

순서는 DESC 방식을 기본으로 1번째 값, 2번째 값 순으로 결과가 출력된다.

`주의할 점` : MySQL에서는 특정 컬럼의 모든 unique한 값이 SQL에서 사용되어야 실행된다.

모든 값을 사용하지 않아도 SQL 실행오류는 나지 않지만 정렬이 실행되지 않는다.

### PostgreSQL

PostgreSQL에서는 ARRAY 기능을 활용하여 정렬할 수 있다.

사용법 : ORDER BY + **array_position(ARRAY[val1,val2,...], Col::TYPE)**

컬럼이름 옆에 타입지정을 해야 실행이 된다.

``` SQL
SELECT * FROM tips 
ORDER BY array_position(ARRAY['Thur','Fri','Sat','Sun'],day::TEXT), 
        array_position(ARRAY['Dinner','Lunch'],time::TEXT);
```

PostgreSQL에서는 MySQL과 다르게 모든 Unique한 값을 사용하지 않아도 정렬이 실행된다. 해당 값끼리만 먼저 정렬되고, 나머지는 ROW번호 기준으로 그대로 출력된다.

참고 : case-sensitive하기 때문에 텍스트의 경우, 정확한 값이 아니면 SQL문이 실행돼도 정렬되지 않는다.

PostgreSQL에서는 간단하게 **col=val1, col=val2, ...** 방식으로도 활용이 가능하다. 단, 이 방식은 **ASC** 기준으로 마지막값부터 정렬된다.

``` SQL
SELECT * FROM tips ORDER BY time='Dinner', time='Lunch';
# 기준 : Lunch -> Dinner
```
