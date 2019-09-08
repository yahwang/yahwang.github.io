---
layout: post
title: SQL로 중복 데이터 확인 및 삭제하기
date: 2019-09-08 05:00:00 pm
permalink: posts/79
description: SQL로 중복 데이터를 확인 및 삭제하는 법을 알아본다.
categories: [Data, SQL]
tags: [PostgreSQL, MySQL, duplicates]
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


    데이터 삭제 쿼리

``` sql
DELETE FROM contacts
WHERE id IN (SELECT id
             FROM ( SELECT id, ROW_NUMBER() OVER (PARTITION BY first_name, last_name, email) as row_num
                    FROM contacts ) a
             WHERE row_num > 1);
```

### MySQL 5

중복 데이터 확인 쿼리에 **DISTINCT**를 추가해서 활용했다.

    삭제할 데이터 id 확인

``` sql
-- IN subquery 버전
SELECT *
FROM contacts
WHERE (first_name, last_name, email) IN ( SELECT DISTINCT first_name, last_name, email
                                          FROM contacts
                                          GROUP BY email, first_name, last_name
                                          HAVING COUNT(email) > 1 AND COUNT(first_name) > 1 
                                                 AND COUNT(last_name) > 1)
ORDER BY first_name;

-- JOIN 버전
SELECT a.*
FROM contacts a
JOIN (SELECT DISTINCT first_name, last_name, email
      FROM contacts
      GROUP BY email, first_name, last_name
      HAVING COUNT(email) > 1 AND COUNT(first_name) > 1 AND COUNT(last_name) > 1) b
ON a.first_name=b.first_name AND a.last_name=b.last_name AND a.email=b.email
ORDER BY a.first_name;
```

[DB Fiddle - MySQL 5 에서 확인](https://www.db-fiddle.com/f/mHRDZMqTD6hbiq21k7gW2c/0){:target="_blank"}

    데이터 삭제 쿼리

MIN 함수를 활용해서 남길 데이터를 제외한 id를 NOT IN으로 처리하였다.

참고 : MySQL은 DELETE 시 자체 데이터를 바로 사용 못하는 이유로 아래 Error reference를 참고했다.

``` sql
DELETE FROM contacts
WHERE id NOT IN ( SELECT *
                  FROM (SELECT MIN(id)
                        FROM contacts
                        WHERE (first_name,last_name,email) IN ( SELECT DISTINCT first_name, last_name, email
                                                                FROM contacts
                                                                GROUP BY email, first_name, last_name
                                                                HAVING COUNT(email) > 1 AND COUNT(first_name) > 1 
                                                                       AND COUNT(last_name) > 1)
                        GROUP BY first_name, last_name, email) tmp);
```

`References` : 

* [Finding Duplicate Rows in SQL - SILOTA](http://www.silota.com/docs/recipes/sql-finding-duplicate-rows.html){:target="_blank"}

* [How To Delete Duplicate Rows in MySQL - MySQLTUTORIAL](http://www.mysqltutorial.org/mysql-delete-duplicate-rows/){:target="_blank"}

* [MySQL Error 1093 : You can't specify target table ...](https://www.lesstif.com/display/DBMS/MySQL+Error+1093+%3A+You+can%27t+specify+target+table+%27cwd_group%27+for+update+in+FROM+clause){:target="_blank"}

