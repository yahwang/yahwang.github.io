---
layout: post
title: MySQL에서 연관 서브쿼리 연산자 EXISTS 활용하기 
date: 2018-04-25 04:00:00 pm
update: 2018-12-04 03:00:00 pm
permalink: posts/35
description: MySQL에서 EXISTS 사용법에 대해 알아본다.  # Add post description (optional)
categories: [Data, SQL]
tags: [MySQL, EXISTS, JOIN, IN (Subquery)] # add tag
---

> MySQL에서 EXISTS 사용법에 대해 알아본다.

`실습에 활용할 테이블`

`order TABLE`

| o_id  | o_date     | c_id | p_id | o_volume |
|-------|------------|------|------|----------|
| O0031 | 2018-04-01 | C03  | P005 |      235 |
| O0032 | 2018-04-15 | C01  | P007 |      541 |
| O0033 | 2018-04-22 | C04  | P006 |      285 |
| O0034 | 2018-05-01 | C02  | P007 |        2 |
| O0035 | 2018-07-01 | C03  | P003 |      187 |
| O0036 | 2018-07-04 | C04  | P008 |       64 |
| O0037 | 2018-09-05 | C07  | P007 |      822 |

`customer 테이블`

| c_id | c_name    | c_grade |
|------|-----------|---------|
| C01  | 홍길동    | VIP     |
| C02  | 김진호    | 일반    |
| C03  | 김진희    | VIP     |
| C04  | 박재우    | 일반    |
| C05  | 이승민    | 일반    |

### EXISTS

EXISTS는 두 개의 테이블에서 같은 값을 가진 컬럼끼리 활용하여 한 테이블 내에서 조건을 걸 수 있다.

W3schools에서는 The EXISTS operator is used to test for the existence of any record in a subquery 로 표현한다.

메인 쿼리의 테이블이 다른 테이블과 FK 같은 관계가 있을 때, 그 테이블에서 확인가능한 조건을 기반으로 

메인 쿼리의 각 ROW마다 TRUE / FALSE를 판단하고 원하는 결과를 추출한다. 

다음 예는 주문 전체에서 VIP 고객의 주문내역만 찾는 쿼리이다.

여기서는 order 테이블이 FK인 c_id 컬럼을 가지고 있다. 

주문 테이블에서 VIP 고객의 주문만을 찾기 위해서 고객 ID 컬럼(c_id)을 활용한다.

``` sql
SELECT * FROM order WHERE EXISTS 
    (SELECT * FROM customer WHERE order.c_id = customer.c_id AND customer.c_grade='VIP');
```

| o_id  | o_date     | c_id | p_id | o_volume |
|-------|------------|------|------|----------|
| O0031 | 2018-04-01 | C03  | P005 |      235 |
| O0032 | 2018-04-15 | C01  | P007 |      541 |
| O0035 | 2018-07-01 | C03  | P003 |      187 |

이처럼 서브쿼리에서 메인쿼리 테이블을 활용하는 형태를 **연관 서브쿼리**라고 한다.

메인쿼리의 컬럼은 ALIAS를 지정하여 서브쿼리에서 활용해야 한다.

EXISTS 다음으로 오는 SELECT에서 * 대신 아무거나(1, 'aa', ...) 입력해도 상관없다. 

MySQL에서는 조건절이 맞는 지에 대한 TRUE / FALSE만 확인하기 때문이다.

여기서는, order 테이블에서 각각 row의 c.id를 EXISTS 서브쿼리에 대입했을 때 값이 존재하느냐 하지않느냐를 판단하는 의미로 이해할 수 있다.

결과가 여러 ROW가 나올 수 있지만 한 번만 나오면 바로 TRUE로 판단하고 다음으로 넘어간다.

### IN, JOIN과의 비교

EXISTS 대신 IN (Subquery), JOIN을 활용하여 같은 결과를 얻을 수도 있다.

``` sql
# IN
SELECT * FROM order WHERE c_id IN ('C01','C03');
SELECT * FROM order WHERE c_id IN (SELECT c_id FROM customer WHERE c_grade='VIP');
# JOIN
SELECT o_id,o_date,order.c_id,p_id, o_volume FROM study.order JOIN customer 
    on order.c_id = customer.c_id WHERE c_grade='VIP';
```

처리 속도 면에서는 단순 IN이 제일 빠르다. 하지만, 찾아야 할 값이 많을 경우에는 IN (Subquery)를 활용해야 한다. 

**IN (Subquery)는 속도가 EXISTS에 비해 느리기 때문에 EXISTS 또는 JOIN을 활용하는 편이 낫다고 한다.**

JOIN의 경우에는, 일반적으로 EXISTS보다 속도가 빠르다고 한다. 단, 중복된 값이 많이 나올 경우에는 EXISTS가 더 빠르다고 한다.

EXISTS는 만족하는 결과가 최소 하나가 나오면 바로 TRUE로 판단하기 때문인 듯 하다.

(The EXISTS operator returns true if the subquery returns one or more records.)

자세한 내용은 References에 링크된 연재글을 참고하면 이해할 수 있다.

### NOT EXISTS

order 테이블에는 customer 테이블에 존재하지 않는 고객 ID가 존재한다. (Foreign Key를 설정하지 않은 경우, 발생할 수 있다.)

NOT EXISTS를 사용하면 역으로 알아낼 수 있다.

``` sql
SELECT * FROM order WHERE NOT EXISTS 
    (SELECT * FROM customer WHERE order.c_id = customer.c_id);
```

| o_id  | o_date     | c_id | p_id | o_volume |
|-------|------------|------|------|----------|
| O0037 | 2018-09-05 | C07  | P007 |      822 |

`References` : 

* [EXISTS와 IN, JOIN 비교 블로그](http://mysqlguru.github.io/mysql/2014/05/22/avoid-mysql-in.html){:target="_blank"}
