---
layout: post
title: Java에 내장된 정렬 함수 사용하기
date: 2019-02-19 09:00:00 pm
permalink: posts/61
description: Java에 내장된 정렬 함수 사용법을 간단하게 알아본다.
categories: [Dev, Language]
tags: [Java, Arrays, Collections]
---

> Java에 내장된 정렬 함수 사용법을 간단하게 알아본다.

Java에는 util패키지에서 Arrays와 Collections를 활용하여 내장 정렬함수를 지원한다.

### Arrays.sort

Arrays.sort는 int,char 같은 primitive type 배열에서 정렬을 지원한다. ( String은 예외로 가능)

이 함수의 정렬 알고리즘은 **dual pivot quicksort**라고 한다. quicksort가 정렬되어 있는 상태에서는 O(n^2)의 시간복잡도를 가진다는 문제점을 보완하고 속도도 더 빠르다고 한다.

변수에 새로 선언하는 것이 아니라 python처럼 현재 저장되어 있는 변수를 그대로 사용하고 내부적으로 정렬을 수행한다.

``` java
import java.util.Arrays;

int[] numbers = {5,2,8,10,6,9};

Arrays.sort(numbers);
```

#### 내림차순 정렬

내림차순 정렬을 위해서는 primitive type이 아니라 Wrapper 클래스로 선언해야 한다. 그 이유는 Collections에 도움을 받아야 하기 때문이다. **Collections.reverseOrder()**을 추가 인자로 넣으면 된다.

``` java
import java.util.Arrays;
import java.util.Collections;
// Wrapper 클래스를 활용하여 선언
Integer[] numbers = {5,2,8,10,6,9};

Arrays.sort(numbers, Collections.reverseOrder());
```

### Collections.sort

Collections.sort는 ArrayList, LinkedList와 같은 Collection 타입의 정렬을 지원한다. 

이 함수의 정렬 알고리즘은 **merge sort**이다. 그 이유는 quicksort와 달리 merge sort는 stable한 정렬이기 때문이다. stable한 정렬은 같은 key값을 가진 node가 정렬 전과 정렬 후의 위치가 달라지지 않는다는 의미라고 한다. int 같은 경우, 같은 값이 여러 개 있을 때 해당 숫자는 서로 위치가 달라져도 문제될 것이 없기에 quicksort를 사용한다.

내림차순 정렬은 Arrays.sort 대신 Collections.sort만 사용하면 된다.

``` java
import java.util.Collections;
import java.util.ArrayList;

ArrayList<Integer> nums = new ArrayList<Integer>();
nums.add(5); nums.add(2); nums.add(8);
nums.add(10); nums.add(6); nums.add(9);

Collections.sort(nums);
//Collections.sort(nums, Collections.reverseOrder());
```

참고: 파이썬의 sort 함수는 timsort라는 알고리즘을 사용한다. real world 데이터에서 효과적이라고 한다. ( references 참고 )

`References` : 

* [Arrays.sort 예제](https://www.geeksforgeeks.org/arrays-sort-in-java-with-examples/
){:target="_blank"}

* [Collections.sort 예제](https://www.geeksforgeeks.org/arrays-sort-in-java-with-examples/
){:target="_blank"}

* [Python sort 알고리즘 설명1](https://hackernoon.com/timsort-the-fastest-sorting-algorithm-youve-never-heard-of-36b28417f399){:target="_blank"}

* [Python sort 알고리즘 설명2](https://dev.to/s_awdesh/timsort-fastest-sorting-algorithm-for-real-world-problems--2jhd
){:target="_blank"}