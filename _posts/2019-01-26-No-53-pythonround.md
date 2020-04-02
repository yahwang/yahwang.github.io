---
layout: post
title: Python에서 round 함수 사용 시 주의할 점
date: 2019-01-26 01:00:00 am
update: 2020-04-02 08:00:00 pm
permalink: posts/53
description: Python에서 round 함수 사용 시 주의할 점에 대해 알아본다.
categories: [Dev, Language]
tags: [Python] # add tag
---

> Python에서 round 함수 사용 시 주의할 점에 대해 알아본다.

python에서 round 함수를 실행했을 때, 우리가 일반적으로는 아는 반올림과는 다른 결과를 보이는 것을 확인할 수 있다.

``` python
# int
round(15,-1) == round(25,-1) == 20 

# float
round(1.5) == round(2.5) == 2   
```

python에서는 우리가 알고 있는 human arithmetic 방식이 아닌 **binary arithmetic** 방식을 취한다고 한다. 

### round to the nearest; ties to even

그 중, **round to the nearest; ties to even** 모드를 사용하고 있다.

round to the nearest는 우리가 아닌 일반적인 반올림 방식과 같지만 ties to even에서 차이가 생긴다. 여기서 말하는 tie는 

기준 값을 중심으로 절반 예를 들면, 1.5는 1과 2와의 차이가 딱 절반이다. 이 때, 계산하는 방식이 다르다.

ties to even을 해석하면, 짝수를 만들기 위해 **앞자리 수가 홀수면 올림, 짝수면 내림**을 취한다. 

그래서 round( 1.5 )와 round( 2.5 )의 결과가 2로 같게 된다.

round 방식을 바꿔서 사용하려면 코드를 만들어야 한다. (python의 math 라이브러리에 round함수는 없다.) 

### 해결방법

방법 중에 하나로 decimal library를 활용하는 방법이 있다. 아래 참고 사이트에서 **my_round**라는 함수를 직접 정의해주셨다.

### 추가 이슈

binary arithmetic은 소수점 숫자(floating point)를 제대로 표현하지 못하는 한계가 있다. 계산 시 주의할 필요가 있다.

아래처럼 0.1235는 실제로 0.1235에 미치지 못한다. 따라서, ties to even 방식과 관계없이 반올림으로 0.124가 되지 못한다.

``` python
from deciaml import Decimal

Decimal(0.1235)
# Decimal('0.12349999999999999866 .... ')

Decimal(0.1)
# Decimal('0.100000000000000005551 .... ')

0.1+0.1+0.1 == 0.3 
# => False
```

#### 참고 : Java에서의 round

Java에서는 java.lang.math 클래스에 round라는 함수가 있다. 이 함수는 1/2을 더하고 더한 값에 내림을 취하는 알고리즘이다. 

문제는 소수점 첫째자리에서만 반올림이 가능하다는 점이다. 곱하고 나눠주는 트릭으로 문제를 풀 수 있다.

``` java
import java.lang.Math
...
System.out.println(Math.round(2.5)) => 3
# 2번째 소수점 반올림 계산을 위한 트릭
System.out.println(Math.round(2.555*100)/100.0) => 2.56
```

2.5에 0.5를 더하면 3이고 3에서 내림은 결국 3이기 때문에 우리가 아는 반올림 결과와 같다. 단, 음수에서는 계산이 달라진다.

`References` : 

* [[Python] 반올림, 내림, 올림하기, round함수 주의사항](https://blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=221551624153&parentCategoryNo=&categoryNo=50&viewDate=&isShowPopularPosts=true&from=search){:target="_blank"}

* [15. Floating Point Arithmetic: Issues and Limitations](https://docs.python.org/3.7/tutorial/floatingpoint.html){:target="_blank"}