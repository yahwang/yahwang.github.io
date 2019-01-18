---
layout: post
title: SQL로 CSV 파일 업로드해 테이블로 만들기
date: 2019-01-17 11:00:00 pm
permalink: posts/47
description: SQL에서 CSV 파일을 업로드해 테이블로 만드는 방법을 알아본다.
categories: [Tech, SQL]
tags: [MySQL, PostgreSQL, Load_csv] # add tag
---

> SQL에서 CSV 파일을 업로드해 테이블로 만드는 방법을 알아본다.

#### CSV 파일을 업로드 하기 전 테이블을 정의해서 미리 생성해야 한다.

``` sql
CREATE TABLE tips (테이블명) (...);
```

컬럼 타입을 지정할 때 데이터에 맞는 타입을 잘 설정해야 한다. 

예를 들어, float 데이터를 int 타입 컬럼에 넣으면 int타입으로 바뀌어 업로드될 수 있다.

### MySQL

MySQL에는 **파일에 접근 가능한 경로에 대한 제약조건**이 존재한다.

보통 /var/lib/mysql-files/ 이렇게 되어있는 경우가 많다. docker container에서는 NULL로 설정되어 있었다.

``` sql
SELECT @@GLOBAL.secure_file_priv;
```

![sql_csv_1]({{site.baseurl}}/assets/img/sql/sql_csv_1.jpg)

경로가 설정되어 있는 경우, 파일의 업로드나 다운로드는 그 폴더에서만 가능하다.
`/etc/mysql/my.cnf`에 접근하여 

secure-file-priv에 ''를 입력하면 제약조건이 무시된다. ( NULL인 경우에도 제약조건이 걸려서 사용할 수 없으니 변경해야 한다.)

![sql_csv_2]({{site.baseurl}}/assets/img/sql/sql_csv_2.jpg)

MySQL을 다시 실행하면 ( service mysql restart ), SQL문으로 테이블에 데이터를 업로드할 수 있다.

``` sql
LOAD DATA INFILE '/home/tips.csv' (파일명) INTO TABLE tips (테이블명)
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
-- IGNORE 1 ROWS는 컬럼명인 header를 무시한다는 의미
```
MySQL에서는 Workbench를 활용해 쉽게 테이블을 업로드할 수 있다.

docker를 활용해도 로컬에 있는 CSV파일을 제약조건에 관계없이 업로드할 수 있다.

![sql_csv_3]({{site.baseurl}}/assets/img/sql/sql_csv_3.jpg)

### PostgreSQL

PostgreSQL은 제약조건없이 바로 SQL문을 활용해 업로드할 수 있다.

``` sql
COPY tips (테이블명) FROM '/home/tips.csv' DELIMITER ',' CSV HEADER;
-- CSV : 파일 포맷을 의미 / HEADER : HEADER LINE 제외한다는 의미
```

PostgreSQL도 pgAdmin4를 활용하면 쉽게 업로드할 수 있다.

![sql_csv_4]({{site.baseurl}}/assets/img/sql/sql_csv_4.jpg)

참고 : docker를 활용할 때는 pgAdmin을 활용해 로컬에 있는 파일이 업로드가 되지 않아서 

container 내부로 파일을 옮기고 SQL문으로 해야한다.

`References` : 

* [MySQL load_data](https://dev.mysql.com/doc/refman/8.0/en/load-data.html){:target="_blank"}
* [PostgreSQL load_data](http://www.postgresqltutorial.com/import-csv-file-into-posgresql-table){:target="_blank"}