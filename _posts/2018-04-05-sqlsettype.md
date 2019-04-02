---
layout: post
title: MySQL에서 SET type 활용하기
date: 2018-04-05 01:00:00 am
permalink: posts/32
description: MySQL에서 String type 중 하나인 SET type에 대해 알아본다.  # Add post description (optional)
categories: [Data, SQL]
tags: [MySQL, SET, FIND_IN_SET] # add tag
---

> SET type은 정해진 리스트 내에서 중복되지 않는 여러 값을 가질 수 있는 string object이다.

SET type은 최대 64개의 Member를 가질 수 있다. 여러 값을 표현할 때는 string 안에 `,` 를 활용하여 구분짓는다.(띄어쓰기 X)

간단한 예로, SET('one', 'two')의 경우, '' / 'one' / 'two' / 'one,two'('two,one') 값을 가질 수 있다.

### SET type의 주요한 특징 Binary(Decimal) Value

SET type은 하나의 값마다 순서대로 **Binary Value**가 부여된다.

1bit가 왼쪽으로 계속 움직이면서 Decimal value는 2배씩 증가한다.
 
| Member | Decimal | Binary |
|--------|---------|--------|
| ''     |   0     |   0000 |
| 'one'  |   1     |   0001 |
| 'two'  |   2     |   0010 |

실습을 위한 students 테이블을 생성해보았다.

``` sql
CREATE TABLE students (id int not null auto_increment primary key, 
    name VARCHAR(10) not null, 
    interests SET('swimming','drawing','cooking','dancing','videogaming'));
INSERT INTO students(name, interests) VALUES ('August','drawing,cooking');
```

interests 컬럼에 swimming, drawing, cooking, dancing, videogaming 요소를 포함한 SET을 설정하였다.

| Member | Decimal | Binary |
|--------|---------|--------|
| 'swimming'  |   1     |   00001 |
| 'drawing'  |   2     |   00010 |
| 'cooking'  |   4     |   00100 |
| 'dancing'  |   8     |   01000 |
| 'videogaming'  |   16     |  10000 |

Multiple value는 각 Member의 합으로 계산된다.

| id | name   | interests                    || Decimal로 표현 |
|----|--------|------------------------------||---------|   
|  1 | August | drawing,cooking              ||2+4= 6|
|  2 | Kevin  |                              ||0|
|  3 | David  | swimming,dancing,videogaming ||1+8+16= 25|
|  4 | James  | cooking,videogaming          ||4+16= 20|
|  5 | Dennis | cooking,dancing,videogaming  ||4+8+16 = 28|
|  6 | Buddy  | videogaming                  ||16|

### 하나의 Member를 찾는 방법

``` sql
SELECT * FROM students WHERE interests LIKE '%drawing%';
SELECT * FROM students WHERE FIND_IN_SET('drawing',interests) > 0;
# 비트연산 활용 (자기 자신 Decimal 값)
SELECT * FROM students WHERE interests & 2(or 0010);
```

**FIND_IN_SET**은,

일치하는 Member가 존재하면 SET에 정의한 순서값 아니면 0을 return한다.

0보다 큰 값으로 조건을 걸면 해당 Member가 존재함을 파악할 수 있다.

``` sql
 SELECT FIND_IN_SET('cooking',interests) FROM students;
 => cooking은 SET에서 3번째로 정의한 값이므로 3,0,0,3,3,0 이 출력된다.
```

### Multiple member를 찾는 방법

AND를 활용해 중복으로 각각의 Member를 선택해야 한다.

참고 : LIKE와 interest='Member1,Member2'와 같은 방법은 실제 value의 순서가 다를 경우 못 찾을 수 있는 경우가 생긴다.

``` sql
SELECT * FROM students WHERE FIND_IN_SET('cooking',interests) > 0 
    and FIND_IN_SET('videogaming', interests);
SELECT * FROM students WHERE interests & 4(or 0100) and interests & 16(or 10000);
```

| id | name   | interests                   |
|----|--------|-----------------------------|
|  4 | James  | cooking,videogaming         |
|  5 | Dennis | cooking,dancing,videogaming |

`References` : 

* [MYSQL SET type 레퍼런스](https://dev.mysql.com/doc/refman/5.7/en/set.html){:target="_blank"}
