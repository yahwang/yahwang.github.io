---
layout: post
title: 논리 연산자인 and(&&), or(||)에서 short-circuit evaluation 방식
date: 2019-02-01 01:00:00 pm
permalink: posts/55
description: 논리 연산자인 and(&&), or(||)에서 short-circuit evaluation에 대해 알아본다.
categories: [Dev, Language]
tags: [Python, Java, Short-circuit]
---

> 논리 연산자인 and(&&), or(ll)에서 short-circuit evaluation에 대해 알아본다.

python에서 &와 and가 같은 의미인 줄로 알았다가 최근에 다름을 알게 되었다.

### Short-circuit evaluation

AND와 OR에서는 첫 번째 조건의 결과에 따라 두 번째 조건을 확인하지 않아도 결과가 정해진다. 따라서, 두 번째 조건 실행을 하지 않는 것이 효율적이다.

이 방식을 **Short-circuit evalutaion**이라고 한다. (알고는 있었지만 이런 용어가 있는 지는 몰랐다.)

|논리 연산|첫 번째 조건|결과|
|----|-----|-------------|
|A AND B | A - False | False |
|A OR B | A - True | True |

### eager operator VS short-circuit operator

**eager operator**는 첫 번째 조건과 상관없이 두 번째 조건을 실행한다.

eager operator는 bit operator와 모양이 같지만 조건 결과가 boolean이면 eager operator로 쓰인다.

|언어|eager|short-circuit|
|----|-----|-------------|
|Python | & / l | and / or |
|Java | & / l | && / ll |

참고 : C에서는 eager operator는 사용하지 않는다.

아래 위키피디아를 확인하면 다른 언어에서도 존재하는 것을 확인할 수 있다.

#### python

두 번째 조건이 실행이 되면 ZeroDivision 에러가 발생한다.

``` python
a, b = 10, 5
# eager - 두 번째 조건을 실행하기 때문 
    a < 0 & (b/0) == 0 => ZeroDivisionError
# short-circuit - 첫 번째 조건에서 종료
    a < 0 and (b/0) == 0 => False
```
#### Java

Java는 증감연산자를 활용해서 테스트해보았다. 두 번째 조건의 실행여부에 따라 y값이 달라지는 걸 확인할 수 있다.

``` java
int x = -1; int y = 0; boolean z =;
// eager
    z = x>0 & ++y == 1;
    System.out.println(y);  =>  1
// short-circuit
    z = x>0 && ++y == 1;
    System.out.println(y);  =>  0

```

`References` : 

* [Short-circuit evaluation - Wikipedia](https://en.wikipedia.org/wiki/Short-circuit_evaluation#Support_in_common_programming_languages){:target="_blank"}
* [참고 블로그](http://ohyecloudy.com/pnotes/archives/542/){:target="_blank"}