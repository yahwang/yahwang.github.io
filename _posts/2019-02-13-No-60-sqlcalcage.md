---
layout: post
title: SQL에서 나이(age) 계산하기
date: 2019-02-13 11:00:00 am
permalink: posts/60
description: SQL로 나이(age) 계산하는 법을 알아본다.
categories: [Data, SQL]
tags: [PostgreSQL, age, MySQL]
---

> SQL로 나이(age) 계산하는 법을 알아본다.

참고 : 데이터 분석을 위한 SQL레시피 내용을 바탕으로 작성하였다.

나이는 매년 변하는 수치이기 때문에 데이터베이스에 저장하는 것은 좋은 방법이 아니다. 저장하더라도 매년 업데이트를 해야 한다. 또한, 나이 계산 시 생일이 지났는지를 고려한 만 나이를 계산해야 하는 경우가 많다.

### MySQL - 계산식을 활용

데이터 분석을 위한 SQL레시피에 따르면 **생일까지 고려한 만 나이**를 계산해주는 식이 존재한다.

날짜에서 '-'를 제거하여 숫자로 만들고 둘의 차에 10000을 나눈 값에 내림을 취하면 된다.

` 예시 : FLOOR( (20190213 - 19950624) / 10000 )`

MySQL에는 날짜타입을 자동으로 텍스트로 인식할 수 있다. CAST로 INT를 지정하기 위해 UNSIGNED(SIGNED)를 활용한다.

``` sql
SELECT FLOOR( (CAST(REPLACE(CURRENT_DATE,'-','') AS UNSIGNED) - 
       CAST(REPLACE('1995-06-24','-','') AS UNSIGNED)) / 10000 ); => 23
```

### PostgreSQL - age function

PostgreSQL에는 나이 계산에 유용한 age function이 존재한다. age function은 기간을 INTERVAL 단위로 알려준다. 여기에 EXTRACT 함수만 사용하면 쉽게 만 나이를 계산할 수 있다.

**SELECT age( 계산할 시점, 기준 시점(생일) );**

``` sql
-- 날짜는 텍스트 타입, 날짜 타입 모두 가능
SELECT age('2019-02-13','1995-06-24'); => 23 years 7 mons 19 days
SELECT EXTRACT( year FROM age(CURRENT_DATE,'1995-06-24')); => 23
```
계산식을 활용할 수도 있다. PostgreSQL에는 INT 계산끼리는 자동으로 floor 처리하고 날짜 타입을 TEXT로 타입지정을 반드시 해야 한다.

``` sql
SELECT (CAST(REPLACE(CAST(CURRENT_DATE AS TEXT),'-','') AS INTEGER) - 
       CAST(REPLACE(CAST('1995-06-24' AS TEXT),'-','') AS INTEGER)) / 10000;
```


