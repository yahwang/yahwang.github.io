---
layout: post
title: SQL에서 TOP N, 상위 퍼센트 데이터 검색하기
date: 2019-01-18 01:00:00 am
permalink: posts/48
description: SQL에서 WINDOW FUNCTION을 활용하여 TOP N, 상위 퍼센트 데이터를 구해본다.
categories: [Tech, SQL]
tags: [MySQL, PostgreSQL, ROW_NUMBER, PERCENT_RANK, FIRST_VALUE] # add tag
---

> SQL에서 WINDOW FUNCTION을 활용하여 TOP N, 상위 퍼센트 데이터를 구해본다.

테스트를 위해서 [tips](https://github.com/mwaskom/seaborn-data/blob/master/tips.csv){:target="_blank"} 데이터를 활용하였다.

SQL에는 `순위와 관련된 WINDOW FUNCTION`이 존재한다. 

`RANK / DENSE_RANK / PERCENT_RANK / ROW_NUMBER`

**주의할 점은, MySQL은 8.0부터 사용가능하다.**

#### 순위관련 함수 차이

**RANK와 DENSE_RANK 차이** - RANK는 공동 순위를 순위선정에 포함한다.

RANK는 공동 1등 뒤를 3등으로 인정, DENSE_RANK는 2등으로 인정

RANK : 1 / 1 / 3 / 3 / 5 &nbsp;&nbsp;&nbsp; < > &nbsp;&nbsp; DENSE_RANK : 1 / 1 / 2 / 2 / 3

**RANK(DENSE_RANK)와 ROW_NUMBER() 차이** - ROW_NUMBER는 공동순위를 순위계산에 인정하지 않는다.

RANK : 1 / 1 / 3 / 3 / 5 &nbsp;&nbsp;&nbsp; < > &nbsp;&nbsp; ROW_NUMBER : 1 / 2 / 3 / 4 / 5

ROW_NUMBER는 같은 순위인 경우 특정한 기준없이 위에 있는 ROW가 앞순위를 차지한다.

## TOP N 구하기

TOP N을 구할 때 보통 RANK보다는 ROW_NUMBER를 사용한다. (값이 같은 것보다는 개수가 의미가 더 있어서??)

### 단순 기준 TOP N

``` sql
SELECT total_bill, ROW_NUMBER() OVER (ORDER BY total_bill DESC) as ranking 
FROM tips LIMIT 3;
```

| total_bill | ranking |
|------------|---------|
| 50.81      |    1    |
| 48.33      |    2    |
| 48.27      |    3    |

### 그룹별 TOP N

그룹기준으로 순위를 계산하기 위해서는 **PARTITION BY**를 활용해야 한다. PARTITION BY는 그룹별로 각각 계산한다는 의미이다.

이렇게 하면 ROW마다 자기가 MALE, FEMALE 인 지에 따라 순위가 정해진다. 하지만, TOP N이라는 조건을 걸 수가 없다.

``` sql
SELECT total_bill, sex, 
       ROW_NUMBER() OVER (PARTITION BY sex ORDER BY total_bill DESC) as ranking 
FROM tips;
```
그룹별로 **TOP N**을 구하기 위해서는 **서브쿼리**를 활용해야 한다. ROW_NUMBER로 만든 ranking 컬럼에서 조건을 걸어주어야 한다.

``` sql
SELECT *
FROM (SELECT total_bill, sex, 
      ROW_NUMBER() OVER (PARTITION BY sex ORDER BY total_bill DESC) as ranking FROM tips) a
WHERE a.ranking <= 3;
```

| total_bill | sex   | ranking |  
|------------|-------|---------|
|44.3        | Female| 1       |
|43.11       | Female| 2       |
|35.83       | Female| 3       |
|50.81       | Male  | 1       |
|48.33       | Male  | 2       |
|48.27       | Male  | 3       |

### FIRST_VALUE 활용

TOP 1을 구할 경우에는 FIRST_VALUE 활용도 가능하다. **DISTINCT**를 활용하여 값이 중복되는 것을 방지한다.

``` sql
SELECT DISTINCT sex, 
       FIRST_VALUE(total_bill) OVER (PARTITION BY sex ORDER BY total_bill DESC) as top_1 
FROM tips;
```

| sex   | top_1   |
|-------|---------|
| Female|   44.3  |
| Male  |  50.81  |

## 상위 퍼센트 구하기

PERCENT_RANK 함수를 활용하면 구할 수 있다. PERCENT_RANK는 누적백분율을 계산해준다.

### 단순 기준 상위 퍼센트

LIMIT는 정수만 입력 가능하기 때문에 서브쿼리를 활용여 조건을 걸어야 한다.

물론, 미리 퍼센트가 몇 명인지 계산하여 LIMIT를 활용할 수도 있다.

``` sql
SELECT * FROM (SELECT total_bill, 
       PERCENT_RANK() OVER (ORDER BY total_bill DESC) as per_rank FROM tips) a
WHERE a.per_rank <= 0.01;
```
총 295명 중 1퍼센트에 속하는 사람은 3명이다.

| total_bill | per_rank |
|------------|----------|
| 50.81      |    0     |
| 48.33      |    0.004 |
| 48.27      |    0.008 |

### 그룹별 상위 퍼센트

``` sql
SELECT *
FROM (SELECT total_bill, sex, 
      PERCENT_RANK() OVER (PARTITION BY sex ORDER BY total_bill DESC) as per_rank FROM tips) a
WHERE a.per_rank <= 0.02;
```
Female 87명 중 2퍼센트는 2명, Male 157명 중 2퍼센트는 4명이다.  

| total_bill | sex   | ranking |  
|------------|-------|---------|
|44.3        | Female| 0       |
|43.11       | Female| 0.011   |
|50.81       | Male  |0        |
|48.33       | Male  |0.006    |
|48.27       | Male  |0.013    |
|48.17       | Male  |0.019    |