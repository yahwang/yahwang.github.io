---
layout: post
title: for - if 반복문 성능을 올리는 법
date: 2017-11-26 05:30:00 pm
permalink: posts/8
description: 조건문이 필요한 계산의 처리속도를 높인다.# Add post description (optional)
img: thumbnail/r_note.png   # Add image post (optional)
tags: [Tech, R] # add tag
---

> 2016년 1월 작성된 R-bloggers의 글을 정리한다. -- 

약간의 코드 변화만으로도 성능을 매우 높일 수 있다.

모든 그래프는 `Mac OS X with 2.6GHz & 8GB RAM`에서 테스트한 기록이다.

``` r
# Raw Code
for( i in 1:nrow(df) ){
    if ( condition )
        df[i, 5] <- "True"
    else
        df[i, 5] <- "False" }
```

`df` : 4개의 컬럼을 가진 dataframe

`condition` : df값을 활용한 조건문

## Output 벡터 선언(Vectorization)

``` r
# Output을 저장할 벡터 선언
output <- vector('character', length=nrow(df))
for( i in 1:nrow(df) ){
    if ( condition )
        output[i] <- "True"
    else
        output[i] <- "False" }
# Output을 새로운 컬럼으로 할당
df$new_col <- output
```

![vectiorization]({{site.baseurl}}/assets/img/r/vectorization.png)

for문 대신 apply 함수를 사용할 수도 있지만 apply 함수가 훨씬 느리다.

![vectiorization]({{site.baseurl}}/assets/img/r/apply.png)

## for 문 밖에 조건 변수(condition) 선언 

**cond** : logical 벡터

e.g.) logi [1:5] FALSE FALSE TRUE FALSE FALSE

``` r
# condition 벡터 생성
output <- vector('character', length=nrow(df))
cond <- condition
for( i in 1:nrow(df) ){
    if ( cond[i] ) 
        output[i] <- "True"
    else
        output[i] <- "False" }
df$new_col <- output        
```

![condition]({{site.baseurl}}/assets/img/r/condition.png)

## True 조건에 맞는 row만 실행

``` r
output <- vector('character', length=nrow(df))
cond <- condition
# for 문을 실행할 row 설정
for( i in ( 1:nrow(df) )[ cond ] ){
    if ( cond[i] ) 
        output[i] <- "True"
    else
        output[i] <- "False" }
df$new_col <- output   
```

![true_condition]({{site.baseurl}}/assets/img/r/true_conditions.png)

## ifelse문 사용 ( 간단한 for문을 작성할 시 )

지금까지 했던 방법을 활용하지 않고 ifelse로만 작성한다.

```  r
# output을 미리 할당하지 않고 바로 계산
output <- ifelse( condition, "True", "False" )
df$new_col <- output
```

![ifelse]({{site.baseurl}}/assets/img/r/ifelse.png)

## Rcpp ( 추후 공부가 필요 )

Rcpp는 C++을 이용하는 방법으로 매우 빠른 속도를 보여준다.

![rcpp]({{site.baseurl}}/assets/img/r/rcpp.png)

**기타 방법으로는,**

* Parallel Processing

* 반복문 끝에 garbage collector를 실행하는 `gc()`를 사용

* 코드 중간 필요없는 object를 삭제하는 `rm()` 활용

* data.frame 대신 `data.table` 사용

`Link` : 

* [Strategies to Speedup R Code](https://www.r-bloggers.com/strategies-to-speedup-r-code/){:target="_blank"}