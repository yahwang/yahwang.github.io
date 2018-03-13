---
layout: post
title: Jupyter(notebook & Lab)에서 R 실행하기(Windows10 & Ubuntu)
date: 2018-02-22 02:00:00 pm
permalink: posts/27
description: Jupyter(notebook & Lab)에 R 커널(kernel)을 설정하여 R을 실행한다.  # Add post description (optional)
img: thumbnail/r_note.png  # Add image post (optional)
categories: [Tech, R]
tags: [Jupyter, IRkernel] # add tag
---

> 파이썬만 설치된 Jupyter(notebook & Lab)에 R 커널을 추가하여 R을 실행할 수 있다. 

Jupyter를 설치한 경우 파이썬만 kernel로 설정되어 있다. Jupyter에서 R을 활용하기 위해서는 `R kernel`을 설정해야 한다.

R을 실행하기 위해서 두 가지의 경우로 생각해 볼 수 있다.

* Anaconda를 통해 R 설치
* R을 개별적으로 설치한 경우

### Anaconda 환경에서 R 설치

conda를 활용하여 R과 IRkernel을 동시에 설치한다.

``` python
conda install r-irkernel
```

이 설치만으로 R을 바로 Jupyter에서 사용할 수 있다.

### R을 개별적으로 설치

R에서 실행해야할 코드는 Rstudio가 아닌 R 자체에서 사용해야 한다.

#### Windows 10

``` r
install.packages('devtools')
devtools::install_github('IRkernel/IRkernel')
IRkernel::installspec()
```

IRkernel::installspec() 실행 시 다음과 같은 오류가 생길 수 있다.

*Error in IRkernel::installspec() :*

*jupyter-client has to be installed but “jupyter kernelspec --version” exited with code 127.*

**이럴 경우에는 환경변수 PATH에 anaconda를 추가해야 한다.**

내 PC - 우클릭 - 속성 - 고급 시스템 설정 - 환경 변수 - 시스템 변수 중 Path 편집

Anaconda(Miniconda) 설치 경로 + @ 총 3가지를 지정해준다.

![anacondapath]({{site.baseurl}}/assets/img/r/anacondapath.png)

다시 IRkernel::installspec()을 실행하면 된다. 

참고 : 환경변수를 지정하고 나면 anaconda prompt가 아닌 cmd에서도 conda 명령어를 사용할 수 있다.

#### Ubuntu(Mint 18.3을 사용)

우분투에서는 먼저 터미널을 활용해 다음 명령어를 실행한다.

``` r
sudo apt-get install libcurl4-openssl-dev # curl 설치를 위해
sudo apt-get install libzmq3-dev # pbdZMq 설치를 위해
```

그 후에 터미널에서 R을 실행하고 다음 코드를 입력한다.

``` r
install.packages(c('repr', 'IRdisplay', 'evaluate', 'crayon', 'pbdZMQ', 
'devtools', 'uuid', 'digest'))
devtools::install_github('IRkernel/IRkernel')
IRkernel::installspec()
```

#### 설정 완료 시 

kernelspec list를 보면 R이 추가된 것을 확인할 수 있다. 이제 Jupyter에서 R을 선택해서 실행할 수 있다.

![kernelspec]({{site.baseurl}}/assets/img/r/kernelspec.jpg)

`Link` : 

* [IRkernel Github](https://github.com/IRkernel/IRkernel){:target="_blank"}

* [Install IRkernel](https://irkernel.github.io/installation/){:target="_blank"}