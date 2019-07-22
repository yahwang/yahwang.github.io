---
layout: post
title: Python의 Generator 활용하기
date: 2019-04-14 01:00:00 am
permalink: posts/69
description: Python에서 Generator 사용법을 알아본다.
categories: [Dev, Language]
tags: [Python, Generator] # add tag
---

> Python에서 Generator 사용법을 알아본다.

## Iterable VS Iterator

### Iterable object

리스트, Set, Dictionary와 같은 컬렉션이나 문자열과 같은 문자 Sequence를 말한다. ( for 문과 같이 하나씩 데이터를 처리할 수 있다. )

기본적으로, Iterable은 Iterator가 아니다.

### Iterator object

**next()** 함수로 데이터를 순차적으로 호출가능한 object

#### Iterable object를 Iterator object로 활용

```python
my_list = [1,2]
my_iter = iter(my_list) # iter 함수로 iterator로 선언

next(my_iter)  # 1
my_iter.__next__() # 2  python3에서는 __next__()도 가능
```

next()로 가져올 데이터가 없을 경우, **StopIteration exception**을 발생시킨다.

```python
next(my_iter)
```

    ------------------------------------------------------------------

    <ipython-input-34-94a4229f6542> in <module>
    ----> 1 next(my_iter)
    
    StopIteration: 


```python
next(my_iter, "No more data")  # StopIteration exception 예외 처리
```

    'No more data'

```python
# for 문을 활용하면 exception없이 마지막 데이터 처리 후 종료된다.
my_iter = iter([1,2,3])
for i in my_iter:
    print(i) # i == next(my_iter)
```

    1
    2
    3

참고 :  for in [list] 형태는 iter(list)를 내부에서 호출한다.

## Generator - iterator의 특수한 형태

next()를 호출하면 **yield**를 찾을 때까지 코드를 수행한다. yield를 만날 경우, 해당 함수는 값을 전달하고 그 라인에서 정지된다. 

이후, 해당 함수는 **종료되는 것이 아니라 그 상태로 유지**된다. 다음 yield가 없을 때 종료된다.

함수의 local 변수 등 **함수 내부에서 사용된 데이터들은 메모리에 그대로 유지**된다.


```python
# generator 함수는 yield를 사용함으로써 정의된다. 
def gen():
    yield 'hello'
    yield 'world!'
```

변수로 선언 후 사용해야 한다. 변수로 사용하지 않으면 first value만 반복된다.


```python
make_gen = gen()
print(next(make_gen))  # 'hello'
print(next(make_gen))  # 'world!'
```

    hello
    world!


```python
# 무한 반복 generator 예시
def infinite_gen():
    while True:
        yield "No end"
```

### Lazy Evaluation- 메모리를 효율적으로 사용

list는 모든 데이터를 메모리에 적재하지만, generator의 경우, next() 메소드를 통해 차례로 값에 접근할 때마다 

메모리에 적재하는 방식이다. / 다음 value가 yield되면 이전 value는 사라진다.

**대용량 데이터를 활용할 때 매우 유용하다.**


```python
import sys
print("List 메모리 사용량")
print( sys.getsizeof([i for i in range(100)]) )
print( sys.getsizeof([i for i in range(10000)]) )
```

    List 메모리 사용량
    912
    87624


```python
print("Generator 메모리 사용량")
print( sys.getsizeof((i for i in range(100))) )
print( sys.getsizeof((i for i in range(10000))) )
```

    Generator 메모리 사용량
    88
    88


### generator expression - List comprehension과 결과는 같지만 한 개씩 접근 가능

sum, map과 같은 list에 적용할 수 있는 함수를 사용할 수 있다.


```python
my_gen = ( i**2 for i in [1,2,3,4,5] )
my_gen
```

    <generator object <genexpr> at 0x7f42242f5af0>


```python
print( sum(my_gen) )
```

    55

### generator를 활용한 데이터 파이프라인 예시

출처 : python-generators-tutorial by dataquest


<div class="dataframe">
<table border="1">
  <thead>
    <tr style="text-align: center;">
      <th>BeerID</th>
      <th>Name</th>
      <th>URL</th>
      <th>Style</th>
      <th>StyleID</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Vanilla Cream Ale</td>
      <td>/homebrew/recipe/view/1633/vanilla-cream-ale</td>
      <td>Cream Ale</td>
      <td>45</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Southern Tier Pumking clone</td>
      <td>/homebrew/recipe/view/16367/southern-tier-pumk...</td>
      <td>Holiday/Winter Special Spiced Beer</td>
      <td>85</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Zombie Dust Clone - EXTRACT</td>
      <td>/homebrew/recipe/view/5920/zombie-dust-clone-e...</td>
      <td>American IPA</td>
      <td>7</td>
    </tr>
  </tbody>
</table>
</div>

```python
beer_data = "recipeData.csv" 

# generator 1
lines = (line for line in open(beer_data, encoding="ISO-8859-1"))
# generator 2
lists = (l.split(",") for l in lines)

# CSV 파일에서 컬럼명만 먼저 추출
columns = next(lists) 

# generator 3
beerdicts = (dict(zip(columns, data)) for data in lists)
```

```python
next(beerdicts)
```

    {'BeerID': '1',
     'Name': 'Vanilla Cream Ale',
     'URL': '/homebrew/recipe/view/1633/vanilla-cream-ale',
     'Style': 'Cream Ale',
     'StyleID': '45',
     'Size(L)': '21.77',
     'OG': '1.055',
     'FG': '1.013',
     'ABV': '5.48',
      ...}

`References` : 

* [generator란 무엇인가](http://bluese05.tistory.com/55){:target="_blank"}

* [python-generators-tutorial by dataquest](https://www.dataquest.io/blog/python-generators-tutorial/){:target="_blank"}
