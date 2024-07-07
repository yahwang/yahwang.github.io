---
layout: post
title: N-interval(N시간 간격) 데이터 처리하기
date: 2024-02-19 01:00:00 am
permalink: posts/106
description: N-interval(N시간 간격) 데이터 처리하는 방법에 대해 간단히 정리해본다.
categories: [Data, SQL]
tags: [Athena, DuckDB]
---

> N-interval(N시간 간격) 데이터 처리하는 방법에 대해 간단히 정리해본다.

*참고: stakoverflow를 보고 배웠으나 기존 링크를 찾을 수 없어서 참고자료로 남길 수 없음*

SQL 기준 : `ATHENA` `DuckDB`

## 기본 SQL

**UNIT** : minute, hour

**N** : 간격

**date_trunc, [unit]** : TIMESTAMP 데이터를 UNIT 시간에 맞게 변환하는 함수

```sql
date_trunc( [UNIT], TIMESTAMP ) - INTERVAL '1' [UNIT] * ( [UNIT](TIMESTAMP) % [N] )
```

5분 간격이라고 할 때, 해당 시간의 분을 5분으로 나눈 나머지 시간을 빼주면 된다.

24분 ==> 24분 - 4(24 % 5)분 => 20분

시간의 경우도 같은 원리로 가능하다. ( 3시간 간격 )

08시 ==> 08시 - 2(8 % 3)시 => 06시

### 분 간격

```sql
WITH time_table AS (
    SELECT TIMESTAMP '2024-02-19 13:53:00' AS ts
    UNION ALL
    SELECT TIMESTAMP '2024-02-19 13:58:00' AS ts
    UNION ALL
    SELECT TIMESTAMP '2024-02-19 14:01:00' AS ts
)

SELECT ts, date_trunc('minute', ts) - interval '1' minute * (minute(ts) % 5) AS itv_ts
FROM time_table
```

데이터가 5분 간격으로 변환된 것을 확인할 수 있다.

|ts|itv_ts|
|--|------|
|2024-02-19 13:58:00|2024-02-19 13:55:00|
|2024-02-19 13:53:00|2024-02-19 13:50:00|
|2024-02-19 14:01:00|2024-02-19 14:00:00|

### 시간 간격

minute을 단순히 hour로만 변경하면 된다.

```sql
WITH time_table AS (
    SELECT TIMESTAMP '2024-02-19 15:53:00' AS ts
    UNION ALL
    SELECT TIMESTAMP '2024-02-19 17:58:00' AS ts
    UNION ALL
    SELECT TIMESTAMP '2024-02-19 18:01:00' AS ts
)

SELECT ts, date_trunc('hour', ts) - interval '1' hour * (hour(ts) % 2) AS itv_ts
FROM time_table
```

데이터가 2시간 간격으로 변환된 것을 확인할 수 있다.

|ts|itv_ts|
|--|------|
|2024-02-19 15:58:00|2024-02-19 14:00:00|
|2024-02-19 17:53:00|2024-02-19 16:00:00|
|2024-02-19 18:01:00|2024-02-19 18:00:00|


## 활용

5분 간격 데이터 집계하기

```sql
WITH time_table AS (
    SELECT TIMESTAMP '2024-02-19 15:31:00' AS ts
    UNION ALL
    SELECT TIMESTAMP '2024-02-19 15:33:00' AS ts
    UNION ALL
    SELECT TIMESTAMP '2024-02-19 15:36:00' AS ts
    UNION ALL
    SELECT TIMESTAMP '2024-02-19 15:37:00' AS ts
    UNION ALL
    SELECT TIMESTAMP '2024-02-19 15:38:00' AS ts
),
itv_time_table AS (
    SELECT date_trunc('minute', ts) - interval '1' minute * (minute(ts) % 5) AS itv_ts
    FROM time_table
)

SELECT itv_ts, COUNT(*) AS cnt
FROM itv_time_table
GROUP BY itv_ts
ORDER BY itv_ts
```

|ts|cnt|
|--|------|
|2024-02-19 15:30:00|2|
|2024-02-19 15:35:00|3|
