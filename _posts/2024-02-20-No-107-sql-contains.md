---
layout: post
title: Geospatial(1) - 특정 Polygon 안에 포함된 위치 데이터 검색
date: 2024-02-20 01:00:00 am
permalink: posts/107
description: 특정 Polygon 안에 포함된 데이터 검색 방법에 대해 간단히 정리해본다.
categories: [Data, SQL]
tags: [Athena, DuckDB]
---

> 특정 Polygon 안에 포함된 위치 데이터 검색 방법에 대해 간단히 정리해본다.

SQL 기준 : `ATHENA` `DuckDB`

### 지리 데이터 형식

지리 데이터는 geometry 타입으로 사용하며, point, line, polygon 등이 있다.

WKT, GeoJson는 geometry 타입을 텍스트로 표현하는 방식이다.

### Polyline Tool

웹사이트 : [https://www.keene.edu/campus/maps/tool](https://www.keene.edu/campus/maps/tool){:target="_blank"}

쉽게 원하는 Polygon 좌표를 알아낼 수 있는 도구를 소개한다. 

우클릭으로 원하는 좌표를 선택 후 마지막 Close Shape를 선택해서 Polygon을 생성하면 된다.

우측에 경도, 위도 데이터 집합 형태와 GeoJSON 데이터를 복사해서 활용할 수 있다.

![sql_polygon_contains]({{site.baseurl}}/assets/img/sql/sql_polygon_contains.jpg)

### 기본 사용법

SQL로 사용하기 위해서는 **WKT Format**으로 표현해야 한다.

[What does WKT stand for?](https://mapscaping.com/a-guide-to-wkt-in-gis/){:target="_blank"}

위에서 얻은 데이터를 약간 변형하면 WKT 형태를 바로 만들 수 있다.

```sql
POLYGON((
    127.0201687 37.5154719,
    127.0248035 37.4893246,
    127.0623974 37.4916401,
    127.0460895 37.5271807,
    127.0201687 37.5154719
))
```

아테나에서 SQL로 WKT format의 데이터를 함수를 사용하여 geometry 타입으로 변환한다.

( 작은 따옴표를 사용해서 문자열임을 나타낸다. )

``` sql
SELECT ST_GeometryFromText('POLYGON((
    127.0201687 37.5154719,
    127.0248035 37.4893246,
    127.0623974 37.4916401,
    127.0460895 37.5271807,
    127.0201687 37.5154719
))')
```

DuckDB의 경우, ST_GeomFromText 함수를 사용하며, spatial extension 로딩이 필요하다. 아래 Reference 참고

### 활용

`ST_Contains (A, B)`: A가 B를 포함하는 경우, true를 반환한다.

```sql
-- DuckDB의 경우, ST_GeomFromText만 변경하면 가능
WITH points AS (
	SELECT ST_Point(127.0336542, 37.5176621) AS target_point
	UNION ALL
	SELECT ST_Point(127.0522043, 37.5400817) AS target_point
)

SELECT *
FROM points
WHERE ST_Contains(
		ST_GeometryFromText(
			'POLYGON((
            127.0201687 37.5154719,
            127.0248035 37.4893246,
            127.0623974 37.4916401,
            127.0460895 37.5271807,
            127.0201687 37.5154719
            ))'
		),
		target_point
	)
```

결과로는 Polygon 안에 포함되어 있는 첫번째 Point만 출력된다.

`References` : 

* [지리 공간 데이터 쿼리 - in AWS](https://docs.aws.amazon.com/ko_kr/athena/latest/ug/querying-geospatial-data.html){:target="_blank"}

* [Spatial Extension - DuckDB](https://duckdb.org/docs/extensions/spatial.html){:target="_blank"}




