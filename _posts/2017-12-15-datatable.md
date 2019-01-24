---
layout: post
title: data.table & dplyr 비교하기
date: 2017-12-15 05:30:00 pm
lastmod:
permalink: posts/15
description: 빠른 속도가 강점인 data.table과 dplyr을 활용하여 데이터 가공 속도를 비교한다.# Add post description (optional)
categories: [Tech]
tags: [R, data.table, dplyr] # add tag
---

> 대용량 처리가 뛰어나다고 알려진 data.table을 dplyr과 테스트 및 비교해본다. -- 

Kaggle에서 약 50MB의 [wine csv파일](https://www.kaggle.com/hiteshp/weekend-which-wine-wins/data){:target="_blank"}을 사용하였다.

rbenchmark를 활용해 테스트한 결과를 확인하였다.

## 파일 Loading fread

dplyr은 read 기능이 없기 때문에 tidyverse 중 readr과 비교한다.

`data.table::fread (data.table) ㅣVSㅣ readr::read_csv (readr)`

``` r
wine_dt <- data.table::fread('wine.csv', encoding = 'UTF-8')
wine_df <- readr::read_csv('wine.csv', locale = locale(encoding = 'UTF-8'))
benchmark(
  data.table = wine_dt <- fread('wine.csv', encoding = 'UTF-8'),
  data.frame = wine_df <- read_csv('wine.csv', locale = locale(encoding = 'UTF-8')),
  replications = 50, columns = c('test','elapsed','relative','replications'))
```

``` r
결과
      test      elapsed  relative  replications 
 2  data.frame   42.44     1.466      50        
 1  data.table   28.95     1.000      50        
```

> fread(data.table)가 readr보다 약 1.5배 정도 빠른 것으로 나타난다.

## Subsetting 

`data.table:: setkey() & J() ㅣVSㅣ dplyr::filter()`

setkey(DT, colnames)를 설정하면 인덱스 Key를 생성하면서 DT를 오름차순으로 정렬한다.

wine_dt2에만 setkey를 설정했다.

### 특정값을 사용할 때

``` r
setkey(wine_dt2, country, province)
benchmark(
  DF.dplyr = wine_df %>% filter(country=='US'&province=='Oregon'),
  DT = wine_dt[country=='US' & province=='Oregon',],
  DT.setkey = wine_dt2[country=='US'& province=='Oregon',],
  DT.dplyr = wine_dt %>% filter(country=='US' & province=='Oregon'),
  DT.setkey.dplyr = wine_dt2 %>% filter(country=='US' & province=='Oregon'),
  DT.setkey.J = wine_dt2[J('US','Oregon'),],
  replications = 100, columns = c('test','elapsed','relative','replications'))
```

``` r
결과
             test elapsed relative replications
1     DT.setkey.J    0.22    1.000          100
2       DT.setkey    0.38    1.727          100
3              DT    0.55    2.500          100
4 DT.setkey.dplyr    0.86    3.909          100
5        DF.dplyr    0.94    4.273          100
6        DT.dplyr    1.00    4.545          100
```

> data.table이 dplyr보다 약 4배 정도 빠르다.

### 다양한 조건을 걸 때

J()는 부등호 조건식과 같이 쓰일 수 없어 subset을 두 번 처리해야 한다.

``` r
setkey(wine_dt2, country, points, price)
benchmark(
  DF.dplyr = wine_df %>% filter(country=='US' & points>90 & price<20),
  DT = wine_dt[country=='US'&points>90 & price<20,],
  DT.setkey = wine_dt2[country=='US'&points>90 & price<20,],
  DT.dplyr = wine_dt %>% filter(country=='US' & points>90 & price<20),
  DT.setkey.dplyr = wine_dt2 %>% filter(country=='US' & points>90 & price<20),
  DT.setkey.J = wine_dt2[J('US')][points>90 & price<20,],
  replications = 100, columns = c('test','elapsed','relative','replications'))
```

``` r
결과
             test elapsed relative replications
1       DT.setkey    0.36    1.000          100
2              DT    0.54    1.500          100
3 DT.setkey.dplyr    0.84    2.333          100
4        DF.dplyr    0.91    2.528          100
5        DT.dplyr    1.05    2.917          100
6     DT.setkey.J    1.45    4.028          100
```

> data.table이 dplyr보다 약 2배 정도 빠르다. J는 다양한 조건식에선 오히려 느리다.

### data.table:: [ , by] ㅣVSㅣ dplyr:: group_by & summarise

``` r
setkey(wine_dt2, points, price)
benchmark(
  DF.dplyr = wine_df %>% filter(points>80 & price<20) %>% group_by(country) %>% summarise(mean(price), mean(points)),
  DT = wine_dt[points>80 & price<20,.(mean(price),mean(points)),by=.(country)],
  DT.setkey = wine_dt2[points>80 & price<20,.(mean(price),mean(points)), by=.(country)],
  DT.dplyr = wine_dt %>% filter(points>80 & price<20) %>% group_by(country) %>% summarise(mean(price), mean(points)),
  DT.setkey.dplyr = wine_dt2 %>% filter(points>80 & price<20) %>% group_by(country) %>% summarise(mean(price), mean(points)),
  replications = 100, columns = c('test','elapsed','relative','replications'))
```

``` r
결과
             test elapsed relative replications
1       DT.setkey    0.53    1.000          100
2              DT    0.65    1.226          100
3        DF.dplyr    2.53    4.774          100
4 DT.setkey.dplyr    2.90    5.472          100
5        DT.dplyr    3.50    6.604          100
```

> dplyr보다 data.table이 약 5배 정도 빠르다

## join

`data.table::[ , on] ㅣVSㅣ dplyr::join()`

dplyr과 달리 data.table은 join할 열[기준이 되는 열, on = 컬럼] 형태를 취한다.
inner join은 Y[X, on= , nomatch=0 ]

``` r
# join할 열 ( 국가에 번호만 부여함)
X <- data.table(country=unique(wine_dt[,country]), num=sample(1:100, 44, replace = F))
benchmark(
  DF.dplyr = wine_df %>% left_join(X,by='country'),
  DT = X[wine_dt, on=.(country)],
  DT.dplyr = wine_dt %>% left_join(X,by='country'),
  DT.setkey = X[wine_dt2, on=.(country)],
  DT.setkey.dplyr = wine_dt2 %>% left_join(X,by='country'),
  replications = 100, columns = c('test','elapsed','relative','replications'))
```

``` r
결과
             test elapsed relative replications
1       DT.setkey    1.44    1.000          100
2              DT    1.66    1.153          100
3        DF.dplyr    3.83    2.660          100
4 DT.setkey.dplyr    3.94    2.736          100
5        DT.dplyr    4.04    2.806          100
```

> dplyr보다 data.table이 약 2배 정도 빠르다.

## Sampling

13만 개의 row에서 50%를 샘플링해보는 테스트를 진행했다.

```r
benchmark(
  DF = wine_df[sample(nrow(wine_df), nrow(wine_df)*0.5),],
  DF.dplyr = wine_df %>% sample_n(nrow(wine_df)*0.5),
  DT = wine_dt[sample(nrow(wine_df),nrow(wine_df)*0.5),],
  DT.dplyr = wine_df %>% sample_n(nrow(wine_dt)*0.5),
  replications = 100, columns = c('test','elapsed','relative','replications'))
```

```r
결과
      test elapsed relative replications
1       DT    2.16    1.000          100
2       DF    3.24    1.500          100
3 DF.dplyr    3.55    1.644          100
4 DT.dplyr    4.99    2.310          100
```

> data.table이 data.frame보다 약 1.5배 빠르다.

### 주의사항

> data.table 자체는 속도가 빠르지만 dplyr과 결합하면 매우 느려진다는 점을 주의해야 한다.
