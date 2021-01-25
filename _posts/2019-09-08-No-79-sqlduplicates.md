---
layout: post
title: SQL로 중복 데이터 확인 및 삭제하기
date : 2019-09-08 05:00:00 pm
update: 2021-01-26 00:00:00 am
permalink: posts/79
description: SQL로 중복 데이터를 확인 및 삭제하는 법을 알아본다.
categories: [Data, SQL]
tags: [PostgreSQL, MySQL, duplicates, DELETE JOIN]
---

> SQL로 중복 데이터를 확인 및 삭제하는 법을 알아본다.

    사용 데이터

| id  | first_name | last_name | email                      |
| --- | ---------- | --------- | -------------------------- |
| 1   | Carine     | Schmitt   | carine.schmitt@verizon.net |
| 2   | Jean       | King      | jean.king@me.com           |
| 3   | Peter      | Ferguson  | peter.ferguson@google.com  |
| 4   | Janine     | Labrune   | janine.labrune@aol.com     |
| 5   | Susan      | Nelson    | susan.nelson@comcast.net   |
| ..   |...    |...   | ...   |

출처 : MYSQLTUTORIAL (아래 Reference에 명시)

## 중복 데이터 확인

### 공통

GROUP BY와 HAVING을 사용하면 된다. 중복을 확인할 컬럼의 수에 따라 조건을 추가해주면 된다.

``` sql
SELECT first_name, last_name, email, COUNT(*) as cnt
FROM contacts
GROUP BY email, first_name, last_name
HAVING COUNT(email) > 1 AND COUNT(first_name) > 1 AND COUNT(last_name) > 1;
```

| first_name | last_name | email                    | cnt |
| ---------- | --------- | ------------------------ | --- |
| Janine     | Labrune   | janine.labrune@aol.com   | 4   |
| Jean       | King      | jean.king@me.com         | 2   |
| Roland     | Keitel    | roland.keitel@yahoo.com  | 3   |
| Susan      | Nelson    | susan.nelson@comcast.net | 3   |


[DB Fiddle - MySQL 5 에서 확인](https://www.db-fiddle.com/f/diVwLqAmeYe8Xvi9eRLmga/0){:target="_blank"}

## 중복 데이터 삭제

중복 데이터를 삭제하기 위해서는 먼저 남길 데이터를 제외한 데이터를 구분할 컬럼(e.g. id)의 값을 구해야 한다.

### MySQL 5

    삭제할 데이터 id 확인

SELF JOIN을 통해 중복된 row의 id를 확인하는 방법이지만 결과를 보면 데이터가 오히려 중복되어 더 생기는 현상이 있다. 

(삭제 쿼리에 활용할 경우, 문제는 없어보임)

``` sql
SELECT t1.*
FROM contacts t1 JOIN contacts t2
ON t1.first_name=t2.first_name AND t1.last_name=t2.last_name AND t1.email=t2.email
WHERE t1.id > t2.id;
```

[DB Fiddle - MySQL 5 에서 확인](https://www.db-fiddle.com/f/bZyWoSx1sDEjHw3Rb6wPaz/2){:target="_blank"}

    데이터 삭제 쿼리

MySQL에서 지원하는 **DELETE JOIN** 방식을 활용한다.

contacts(t1) 테이블에서 FROM 절 이후 JOIN된 결과에 해당하는 ROW들을 삭제한다는 의미이다.

``` sql
DELETE t1 FROM contacts t1 
JOIN contacts t2
ON t1.first_name=t2.first_name AND t1.last_name=t2.last_name AND t1.email=t2.email
WHERE t1.id > t2.id;
```

[DB Fiddle - MySQL 5 에서 확인](https://www.db-fiddle.com/f/4s9gf42vvSG6v6KikpDyFP/2){:target="_blank"}

### PostgreSQL & MySQL 8

WINDOW FUNCTION을 지원하는 경우, **ROW_NUMBER**를 활용하여 처리할 수 있다.

PARTITION BY로 중복된 컬럼을 지정하고, ROW_NUM > 1을 설정하여 삭제할 데이터만 가져올 수 있다.

    삭제할 데이터 id 확인

``` sql
SELECT *
FROM ( SELECT id, first_name, last_name, email,
       ROW_NUMBER() OVER (PARTITION BY first_name, last_name, email) as row_num
       FROM contacts ) a
WHERE row_num > 1
ORDER BY first_name; -- 단순 정렬 용도
```

| id  | first_name | last_name | email                    | row_num |
| --- | ---------- | --------- | ------------------------ | ------- |
| 7   | Janine     | Labrune   | janine.labrune@aol.com   | 2       |
| 9   | Janine     | Labrune   | janine.labrune@aol.com   | 3       |
| 13  | Janine     | Labrune   | janine.labrune@aol.com   | 4       |
| 15  | Jean       | King      | jean.king@me.com         | 2       |
| 17  | Roland     | Keitel    | roland.keitel@yahoo.com  | 2       |
| 18  | Roland     | Keitel    | roland.keitel@yahoo.com  | 3       |
| 8   | Susan      | Nelson    | susan.nelson@comcast.net | 2       |
| 16  | Susan      | Nelson    | susan.nelson@comcast.net | 3       |

[DB Fiddle - MySQL 8 에서 확인](https://www.db-fiddle.com/f/bZyWoSx1sDEjHw3Rb6wPaz/0){:target="_blank"}


    간단한 데이터 삭제 쿼리

데이터가 적을 경우, 간단하게 IN 으로 해당 id들을 제거할 수 있다.

``` sql
DELETE FROM contacts
WHERE id IN (SELECT id
             FROM ( 
                 SELECT id, ROW_NUMBER() OVER (PARTITION BY first_name, last_name, email) as row_num
                 FROM contacts 
                 ) tmp
             WHERE row_num > 1);
```

[DB Fiddle - MySQL 8 에서 확인](https://www.db-fiddle.com/f/uxCSKY7VZ4taXzuHp9FPRp/1){:target="_blank"}

    데이터 삭제 쿼리

PostgreSQL에서는 **DELETE + USING** 방식을 활용한다. 데이터가 많은 것을 고려할 경우, 이 방법을 먼저 사용해야 할 듯하다.

JOIN 과 ON 대신 USING과 WHERE이 사용된다.

``` sql
DELETE FROM contacts t1 
USING contacts t2
WHERE t1.first_name=t2.first_name AND t1.last_name=t2.last_name AND t1.email=t2.email AND t1.id > t2.id;
```

[DB Fiddle - PostgreSQL 9.6 에서 확인](https://www.db-fiddle.com/f/4s9gf42vvSG6v6KikpDyFP/3){:target="_blank"}

### 속도가 느릴 경우

데이터가 너무 많을 경우, 일부분씩 나누어서 DELETE를 하는 것을 고려해볼 수 있다. (특히, 실 사용중인 DB인 경우)

위에서 설명한 삭제할 id를 미리 테이블로 만들어 DELETE JOIN에 사용하는 것이다. (JOIN 연산을 단순화한다.)


`References` : 

* [Finding Duplicate Rows in SQL - SILOTA](http://www.silota.com/docs/recipes/sql-finding-duplicate-rows.html){:target="_blank"}

* [How To Delete Duplicate Rows in MySQL - MySQLTUTORIAL](http://www.mysqltutorial.org/mysql-delete-duplicate-rows/){:target="_blank"}

* [MySQL DELETE JOIN - MySQLTUTORIAL](https://www.mysqltutorial.org/mysql-delete-join/){:target="_blank"}

* [PostgreSQL DELETE JOIN - PostgreSQLTUTORIAL](https://www.postgresqltutorial.com/postgresql-delete-join/){:target="_blank"}

