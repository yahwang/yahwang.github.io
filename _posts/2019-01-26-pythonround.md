---
layout: post
title: Python에서 round 함수 사용 시 주의할 점
date: 2019-01-26 01:00:00 am
permalink: posts/53
description: Python에서 round 함수 사용 시 주의할 점에 대해 알아본다.
categories: [Tech, Python]
tags: [Round] # add tag
---

> Python에서 round 함수 사용 시 주의할 점에 대해 알아본다.

python에서 round 함수를 실행했을 때, 우리가 일반적으로는 아는 반올림과는 다른 결과를 보이는 것을 확인할 수 있다.

``` python
# int
round(15,-1) == round(25,-1) == 20 
# float
round(1.5) == round(2.5) == 2   
```

python에서는 우리가 알고 있는 human arithmetic 방식이 아닌 **binary arithmetic** 방식을 취한다고 한다. 그 중, **round to the nearest; ties to even** 모드를 사용하고 있다.

round to the nearest는 우리가 아닌 일반적인 반올림 방식과 같지만 ties to even에서 차이가 생긴다. 여기서 말하는 tie는 기준 값을 중심으로 절반 예를 들면, 1.5는 1과 2와의 차이가 딱 절반이다. 이 때, 계산하는 방식이 다르다.

ties to even을 해석하면, 짝수를 만들기 위해 **앞자리 수가 홀수면 올림, 짝수면 내림**을 취한다. 그래서 round(1.5)와 round(2.5)의 결과가 2로 같게 된다.

round 방식을 바꿔서 사용하려면 코드를 만들어야 한다. (python의 math 라이브러리에 round함수는 없다.)방법 중에 하나로 decimal library를 활용하는 방법이 있다. 아래 참고 사이트에 들어가면 편하게 사용하기 위한 **decimal_round**라는 함수를 직접 정의해 주어서 그대로 사용하면 된다.

#### 참고 : Java에서의 round

Java에서는 java.lang.math 클래스에 round라는 함수가 있다. 이 함수는 1/2을 더하고 더한 값에 내림을 취하는 알고리즘이다. 문제는 소수점 첫째자리에서만 반올림이 가능하다는 점이다. 곱하고 나눠주는 트릭으로 문제를 풀 수 있다.

``` java
import java.lang.Math
...
System.out.println(Math.round(2.5)) => 3
# 2번째 소수점 반올림 계산을 위한 트릭
System.out.println(Math.round(2.555*100)/100.0) => 2.56
```

2.5에 0.5를 더하면 3이고 3에서 내림은 결국 3이기 때문에 우리가 아는 반올림 결과와 같다. 단, 음수에서는 계산이 달라진다.

`References` : 

* [Rounding in Python](https://kfolds.com/rounding-in-python-when-arithmetic-isnt-quite-right-11a79a30390a){:target="_blank"}