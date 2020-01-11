---
layout: post
title: SQL에서 연관 서브쿼리 연산자 EXISTS 활용하기 
date: 2018-04-25 04:00:00 pm
update: 2020-01-12 03:00:00 am
permalink: posts/35
description: SQL에서 EXISTS 사용법에 대해 알아본다.
categories: [Data, SQL]
tags: [MySQL, PostgreSQL, EXISTS, JOIN, IN (Subquery)]
---

> MySQL에서 EXISTS 사용법에 대해 알아본다.

    RENEWAL (그동안 EXISTS에 적합하지 않은 예시 사용)

`실습에 활용할 테이블`

`customers 테이블`

| c_id | c_name    | c_grade |
|------|-----------|---------|
| C01  | kevin    | VIP     |
| C02  | terry    | G    |
| C03  | john    | VIP     |
| C04  | jane    | G    |
| C05  | adam    | G    |

`orders TABLE`

c_id를 외래키(FK)로 사용가능

| o_id  | o_date     | c_id | p_id | o_volume |
|-------|------------|------|------|----------|
| O0031 | 2018-04-01 | C03  | P005 |      235 |
| O0033 | 2018-04-22 | C04  | P006 |      285 |
| O0034 | 2018-05-01 | C02  | P007 |        2 |
| O0035 | 2018-07-01 | C03  | P003 |      187 |
| O0036 | 2018-07-04 | C04  | P008 |       64 |
| O0037 | 2018-09-05 | C07  | P007 |      822 |

### EXISTS

한 테이블이 다른 테이블과 외래키(FK)와 같은 관계가 있을 때 유용하다. EXISTS를 활용여부는 쿼리문을 사용하는 이유를 생각하면 파악할 수 있다.

W3schools에서는 **The EXISTS operator is used to test for the existence of any record in a subquery** 로 표현한다.

즉, 두 테이블 간의 결과를 어떤 값이 존재하는 지를 알고 싶은 경우이다. **핵심은 존재하는 가를 판단하는 것이다.** 

쿼리의 의도를 고려했을 때 EXISTS를 선택해야 쿼리문 성능이 효과적이다. 그렇지 않을 경우, JOIN을 활용하는 것이 낫다. 자세한 내용은 아래에서 확인할 수 있다.

### 실습

이 실습의 의도는 주문한 적이 있는(주문이 존재하는) 사용자를 알고 싶다고 정의할 수 있다.

EXISTS는 두 개의 테이블에서 같은 값을 가진 컬럼끼리 활용하여 서브쿼리 형태로 조건을 걸 수 있다.

여기서는 c_id를 기준으로 주문한 적이 있는 사용자를 검색한다.

```sql
SELECT * FROM customers WHERE EXISTS (
    SELECT * FROM orders WHERE orders.c_id = customers.c_id);
```

| c_id | c_name | c_grade |
| ---- | ------ | ------- |
| C02  | terry  | G       |
| C03  | john   | VIP     |
| C04  | jane   | G       |

[DB Fiddle에서 확인](https://www.db-fiddle.com/f/cJzgfY9HCSSUYZVNvWW7uD/2){:target="_blank"}

이처럼 서브쿼리에서 메인쿼리 테이블을 활용하는 형태를 **연관 서브쿼리**라고 한다.

EXISTS 다음으로 오는 SELECT에서 * 대신 아무거나(1, 'aa', ...) 입력해도 상관없다. 

EXISTS는 조건이 맞는 지에 대한 TRUE / FALSE만 확인하기 때문이다. 만족하는 결과가 최소 하나가 나오면 바로 TRUE로 판단한다.

( The EXISTS operator returns true if the subquery returns one or more records. )

여기서는, customers 테이블의 c_id를 EXISTS 서브쿼리에 대입했을 때 값이 존재하는 지를 판단하는 의미로 이해할 수 있다.

결과가 여러 ROW가 나올 수 있지만 한 번만 나오면 바로 TRUE로 판단하고 다음으로 넘어간다.

### IN, JOIN과의 비교

EXISTS 대신 IN (Subquery), JOIN을 활용하여 같은 결과를 얻을 수도 있다. 

``` sql
-- IN
-- DISTINCT 생략해도 결과는 같음
SELECT * FROM customers WHERE c_id IN ( SELECT DISTINCT c_id FROM orders);

-- JOIN
SELECT DISTINCT c.*
FROM customers c JOIN orders o
on o.c_id = c.c_id;
```

**IN (Subquery)는 속도가 느리기 때문에 EXISTS 또는 JOIN을 활용하는 편이 낫다고 한다.**

JOIN의 경우에는, 일반적으로 EXISTS보다 속도가 빠르다고 한다. 단, 중복된 값이 많이 나올 경우에는 EXISTS가 더 빠르다고 한다.

자세한 내용은 References에 링크된 글을 참고하면 이해할 수 있다.

    개인 생각

EXISTS를 IN, JOIN으로 바꿨을 때 DISTINCT를 사용하는 등 쿼리가 약간 일반적이지 않을 경우, EXISTS가 효과적인 것 같다.

쿼리가 먼저 JOIN으로 쉽게 작성할 수 있다면 JOIN이 더 빠를 것으로 예상한다.

### NOT EXISTS

orders 테이블에는 customers 테이블에 존재하지 않는 고객 ID가 존재한다. (Foreign Key를 설정하지 않은 경우, 발생할 수 있다.)

NOT EXISTS를 사용하면 알아낼 수 있다.

``` sql
SELECT * FROM orders WHERE NOT EXISTS 
    (SELECT * FROM customers WHERE customers.c_id = orders.c_id);
```

| o_id  | o_date     | c_id | o_volume |
|-------|------------|------|----------|
| 37 | 2018-09-05 | C07  |      822 |

`References` : 

* [MySQL EXISTS - MySQL Tutorial](https://www.mysqltutorial.org/mysql-exists/){:target="_blank"}

* [EXISTS와 IN, JOIN 비교 블로그](http://mysqlguru.github.io/mysql/2014/05/22/avoid-mysql-in.html){:target="_blank"}
