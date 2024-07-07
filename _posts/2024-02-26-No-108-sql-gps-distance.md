---
layout: post
title: Geospatial(2) - 위경도 좌표 간 거리 계산하기
date: 2024-02-26 01:00:00 am
permalink: posts/108
description: 위경도 좌표 간 거리 계산하는 방법에 대해 간단히 정리해본다.
categories: [Data, SQL]
tags: [Athena, DuckDB]
---

> 위경도 좌표 간 거리 계산하는 방법에 대해 간단히 정리해본다.

SQL 기준 : `ATHENA` 

## GEOGRAPHY 타입

GEOGRAPHY는 GEOMETRY와 달리 위치를 지구 표면 위에 표시하는 방식(geographic coordinates)이다.

GEOMETRY를 GEOGRAPHY로 변환해서 사용할 수도 있다.

## 기본 사용법

GEOMETRY를 GEOGRAPHY 타입으로 변환하려면 **to_spherical_geography** 함수를 사용한다.

참고로, ATHENA ENGINE VERSION 3는 Trino 기반이기에 Trino 문서를 확인하면 된다.

```sql
SELECT ST_POINT(127.0278908, 37.4979810) AS geometry_data,
        to_spherical_geography(ST_POINT(127.0278908, 37.4979810)) AS geography_data
```

ATHENA에서 출력 결과는 똑같다.

|geometry_data|geography_data|
|-------------|--------------|
|POINT (127.0278908 37.497981)|POINT (127.0278908 37.497981)|

### 거리 구하기

ST_DISTANCE는 두 좌표 간 거리(미터)를 구하는 함수이다. 

예시로, 구글에서 서울, 부산 좌표를 사용했고 두 도시의 거리는 약 320KM이라 한다.

참고로, GEOGRAPHY 타입끼리 거리를 구하는 방식을 **Great Circle Distance**라고 한다.

간단하게 말하면 지구 표면에서의 최단거리를 구하는 방식이다.

```sql
WITH points AS (
    SELECT ST_POINT(126.9917937, 37.5518911) AS seoul_geom, ST_POINT(129.0688702, 35.2100142) AS busan_geom
)

SELECT ST_DISTANCE(seoul_geom, busan_geom)/1000 AS geom_dist,
        ST_DISTANCE(to_spherical_geography(seoul_geom), to_spherical_geography(busan_geom))/1000 AS geog_dist
FROM points
```

GEOMETRY와 GEOGRAPHY 타입끼리 거리를 계산해보면 차이를 확인할 수 있다.

|geom_dist|geog_dist|
|---------|--------------|
|0.00313|319.95660|

## 활용

위치 데이터를 수집한 후 총 이동거리를 계산할 수 있다.

예시는 10초 간 강남역에서 삼성역까지 일직선 상 위치 좌표들이다. 네이버 지도 거리 상 약 3.4KM로 확인된다.

```sql
WITH points AS (
    SELECT TIMESTAMP '2024-02-26 10:00:01' AS operated_at, ST_POINT(127.0278908, 37.4979810)  AS geom_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:02' AS operated_at, ST_POINT(127.0323122, 37.4993089)  AS geom_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:03' AS operated_at, ST_POINT(127.0362614, 37.5005346)  AS geom_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:04' AS operated_at, ST_POINT(127.0402106, 37.5018283)  AS geom_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:05' AS operated_at, ST_POINT(127.0435160, 37.5027135)  AS geom_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:06' AS operated_at, ST_POINT(127.0465637, 37.5036328)  AS geom_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:07' AS operated_at, ST_POINT(127.0501696, 37.5047903)  AS geom_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:08' AS operated_at, ST_POINT(127.0538183, 37.5057776)  AS geom_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:09' AS operated_at, ST_POINT(127.0566085, 37.5067308)  AS geom_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:10' AS operated_at, ST_POINT(127.0632192, 37.5088415)  AS geom_location
),
geog_points AS (
    SELECT operated_at, LAG(to_spherical_geography(geom_location), 1) OVER (ORDER BY operated_at) AS geog_prev_location,
            to_spherical_geography(geom_location) AS geog_location
    FROM points
)
        
SELECT SUM(ST_DISTANCE(geog_prev_location, geog_location)) AS total_distance
FROM geog_points
```

LAG 함수를 활용해 timestamp에 따라 이전 좌표를 가져온 다음 현재 좌표와의 거리를 계산한 후 합을 구한다.

대략 네이버 거리와 비슷한 것을 확인할 수 있다.

|total_distance|
|---------|
|3343.19695|

### DuckDB에서 활용 (참고)

spatial extension에서는 공식적으로 spherical geometry를 지원하지 않는다고 나와있다.

[Feature: Spherical calculations #16](https://github.com/duckdb/duckdb_spatial/issues/16){:target="_blank"}

이 문서에 따르면 문서화되지 않았지만 이미 배포되었다고 해서 테스트해보았다.

GEOGRAPY타입을 지원하지 않아 Point2D라는 duckdb에서만 지원하는 타입을 사용해야 한다.

주의할 점은 타입 선언 시 Longitude, Latitude가 아닌 Latitude, Longitude 방식이다.

```sql
WITH points AS (
    SELECT TIMESTAMP '2024-02-26 10:00:01' AS operated_at, ST_Point2D(37.4979810, 127.0278908) AS geom_2d_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:02' AS operated_at, ST_Point2D(37.4993089, 127.0323122) AS geom_2d_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:03' AS operated_at, ST_Point2D(37.5005346, 127.0362614) AS geom_2d_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:04' AS operated_at, ST_Point2D(37.5018283, 127.0402106) AS geom_2d_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:05' AS operated_at, ST_Point2D(37.5027135, 127.0435160) AS geom_2d_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:06' AS operated_at, ST_Point2D(37.5036328, 127.0465637) AS geom_2d_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:07' AS operated_at, ST_Point2D(37.5047903, 127.0501696) AS geom_2d_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:08' AS operated_at, ST_Point2D(37.5057776, 127.0538183) AS geom_2d_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:09' AS operated_at, ST_Point2D(37.5067308, 127.0566085) AS geom_2d_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:10' AS operated_at, ST_Point2D(37.5080245, 127.0603860) AS geom_2d_location
    UNION ALL
    SELECT TIMESTAMP '2024-02-26 10:00:11' AS operated_at, ST_Point2D(37.5088415, 127.0632192) AS geom_2d_location
)

SELECT SUM(ST_Distance_spheroid(geom_2d_prev_location, geom_2d_location)) AS total_distance
FROM (
    SELECT operated_at, LAG(geom_2d_location, 1) OVER (ORDER BY operated_at) AS geom_2d_prev_location, geom_2d_location
    FROM points
) tmp
```

|total_distance|
|---------|
|3349.51090|

`References` : 

* [Geography and Geometry in PostGIS](https://mapscaping.com/geography-and-geometry-in-postgis/){:target="_blank"}

* [18. Geography - PostGIS](http://postgis.net/workshops/postgis-intro/geography.html){:target="_blank"}

* [Geospatial functions - Trino](https://trino.io/docs/current/functions/geospatial.html#to_spherical_geography){:target="_blank"}


