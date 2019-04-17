---
layout: test_post
title: CPython의 GIL에 대한 이해
date: 2019-04-18 01:00:00 am
permalink: posts/70
description: CPython에서 GIL에 대해 알아본다.
categories: [Dev, Language]
tags: [Python, GIL, Thread] # add tag
---

> CPython의 GIL에 대해 알아본다.

**[What is the Python Global Interpreter Lock (GIL) by Real Python](https://realpython.com/python-gil/){:target="_blank"}을 기반으로 작성하였다.**


## Thread-safe memory management

Thread safety란 멀티 스레드 프로그래밍에서 일반적으로 어떤 함수나 변수, 혹은 객체가 여러 스레드로부터 동시에 접근이 이루어져도 

프로그램의 실행에 문제가 없음(free of race condition)을 뜻한다. Thread-safe memory management 방법에는 여러가지가 있다. 

Python에는 Jython, ItronPython 등 여러 Interpreter 언어가 존재하는데 그 중 대표적인 **CPython**에서는 GIL을 사용한다. 

(참고 : [PyPy도 GIL을 사용한다.](http://doc.pypy.org/en/latest/faq.html#does-pypy-have-a-gil-why){:target="_blank"})

##  GIL(Global Interpreter Lock)을 선택한 이유 - easy-to-use

CPython에 적용되는 C로 구현된 extensions(libraries)들이 특히 thread-safe memory management가 필요하다. 

GIL은 구현하기 쉽기 때문에 C extensions 적용도 간단해진다. Python의 설계의도(easy-to-use)와 부합하기 때문에 GIL이 적용된 것이다.

또한, single-threaded program에서 performance를 높여주는 효과도 있다.

### CPython의 메모리 관리 with reference counting

모든 객체는 자신을 가리키는 reference를 count하는 변수(reference count variable)가 존재한다.

ref count가 0이 될 때 메모리가 release된다.


```python
import sys

a=[1,2,3]
b=a

print( sys.getrefcount(a) ) # 현재 함수도 reference에 포함
del b
print( "after removing b : ", sys.getrefcount(a) )
```

    3
    after removing b :  2


reference count variable은 thread-safety를 위해 **race condition**으로부터 안전해야 하는데 GIL이 이를 해결해준다. 

그렇지 않은 경우, leaked memory 문제 또는 reference가 존재하는 데도 메모리가 release되는 문제가 생길 수 있다. 

* leaked memory : reference가 존재하지 않는 memory (release 되지 못하고 메모리를 차지하는 경우)

* race condition : 둘 이상의 thread가 공유 데이터에 접근해 서로 데이터를 바꾸려고 하는 경우

참고 : 다른 언어에서는 Garbage collection와 같은 방식으로 메모리를 관리하고 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;performance가 떨어지는 것을 보완하기 위해 JIT Compiler와 같은 boosting feature를 사용한다.

##  GIL(Global Interpreter Lock)에 대한 이해

lock이란 어떤 데이터를 이용해 작업하고 있는 도중에 다른 thread가 접근하지 못하도록 하고 

먼저 오픈한 thread가 닫기 전까지 사용할 수 없게 만드는 방법이다.

![]({{site.baseurl}}/assets/img/python/python_gil_1.png)

> GIL is a mutex(or lock) that allows only one thread to hold the control of the Python interpreter.

GIL은 interpretor에 lock을 걸어 모든 시간에 하나의 선택된 thread의 명령만 실행할 수 있다는 의미이다. 

여러 작업을 동시에 처리하는 작업(병렬)은 기본적으로 지원하지 않는다. (해결방법은 따로 존재)

GIL의 실행단위는 **bytecode**이며, Python에서 bytecode를 실행하기 위해서는 interpreter lock을 먼저 acquire해야 한다.

참고 : byte code 예시


```python
import dis
dis.dis(lambda x: x+1)
```

      2           0 LOAD_FAST                0 (x)
                  2 LOAD_CONST               1 (1)
                  4 BINARY_ADD
                  6 RETURN_VALUE


#### GIL이 미치는 영향

CPU-bound and Multi-threaded 프로그래밍에서는 bottleneck 문제가 생길 수 있다.

|   Program        | Single-thread | Multi-thread |
|-----------|---------------|--------------|
| **CPU-bound** |    성능 향상    |     **Bottleneck**      |
| **I/O bound** |   관계 없음    |   성능  향상     |

참고 : 단점에도 불구하고 GIL을 제거하면 C extensions에 문제가 생기고 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;오히려 향상되었던 performance가 저하되는 문제가 생긴다고 한다. (아직 해결되지 못한 과제)

### 1. CPU-bound and Multi-threaded program

![]({{site.baseurl}}/assets/img/python/python_gil_2.png)

참고 : GIL의 thread 전환 시간


```python
import sys
sys.getswitchinterval() # 0.005초
```

    0.005

#### CPU-bound single-threaded example


```python
import time

def countdown(n):
    while n>0:
        n-=1

COUNT = 100000000
start = time.time()
countdown(COUNT)
print("Total time : ", time.time()-start)
```

    Total time :  3.7545740604400635


#### CPU-bound multi-threaded example


```python
import time
from threading import Thread

def countdown(n):
    while n>0:
        n-=1

COUNT = 100000000
t1 = Thread(target=countdown, args=(COUNT//2,))
t2 = Thread(target=countdown, args=(COUNT//2,))
start = time.time()
t1.start()
t2.start()
t1.join()
t2.join()

print("Total time : ", time.time()-start)
```

    Total time :  3.758510112762451


multithread가 더 오래 걸리는 이유는 lock을 acquire&release 과정에서 발생하는 **overhead**때문이다.

이런 프로그램 실행 속도의 향상을 위해서는 **multiprocessing**이나 **ProcessPoolExecutor** 사용을 고려해야 한다. 
    
&nbsp;&nbsp;(GIL을 피하기 위해 thread가 아닌 process를 추가로 생성한다.)

### 2. I/O-bound and Multi-threaded program

![]({{site.baseurl}}/assets/img/python/python_gil_3.png)

`References` : 

* [파이썬으로 클라우드 하고 싶어요 by 하용호](https://www.slideshare.net/kthcorp/h32011c6pythonandcloud-111205023210phpapp02?from_m_app=ios){:target="_blank"}

* [An Intro to Threading in Python by Real Python](https://realpython.com/intro-to-python-threading/#producer-consumer-using-queue){:target="_blank"}
