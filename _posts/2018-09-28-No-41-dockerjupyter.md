---
layout: post
title: docker에서 실행한 Jupyter를 PC 브라우저와 연동하기
date: 2018-09-28 02:00:00 pm
permalink: posts/41
description: docker에서 실행한 jupyter를 로컬 PC 브라우저와 연동할 수 있다.
categories: [Dev, DevOps]
tags: [Docker, Jupyter] 
---

> docker에서 실행한 jupyter를 로컬 PC 브라우저와 연동할 수 있다.

[anaconda3 docker image](https://hub.docker.com/r/continuumio/anaconda3){:target="_blank"}를 활용하여 테스트하였다.

container 생성 시, jupyter 실행 포트와 로컬 PC의 포트를 이어주는 설정을 반드시 해야 한다.

(주의 : 한 번 container 생성 후에는 설정이 불가능하다.)

``` python 
docker pull continuumio/anaconda3
# 로컬 PC의 8889 포트와 jupyter 기본 포트인 8888을 연결한다.
# jupyter 포트는 나중에 변경가능하기 때문에 원하는 포트로 설정해도 상관은 없다.
docker run -it -p 8889:8888 continuumio/anaconda3 /bin/bash
```

container 생성 시 미리 포트 설정만 해두면 직접 우분투 이미지부터 anaconda를 설치해도 상관없다.

`jupyter lab`을 활용하였지만 jupyter notebook도 동일하다.

먼저, jupyter 기본 환경설정 파일을 생성한다.

``` python
jupyter lab(notebook) --generate-config
```
![docker_jupyter1]({{site.baseurl}}/assets/img/linux/docker_jupyter1.png)

생성한 파일을 docker에 맞게 수정해야 한다.

``` python
nano /root/.jupyter/jupyter_notebook_config.py
```
우리가 수정해야 할 부분은 크게 4가지이다.

``` python
c.NotebookApp.ip = '*' 또는 '0.0.0.0' # ip 설정
c.NotebookApp.allow_root = True# root 계정에서 jupyter 사용 설정 ( 특히, docker의 경우)
c.NotebookApp.open_browser = False # jupyter 실행 시 브라우저 자동 실행 여부
c.NotebookApp.password = 아래 설명 참고 # 비밀번호 설정
```

![docker_jupyter2]({{site.baseurl}}/assets/img/linux/docker_jupyter2.png)

기본적으로 jupyter는 로그인하기 위해 token값을 요구한다. token값은 자동으로 생성되며, 로컬 PC에서는 브라우저가 자동으로 실행되기 때문에 따로 입력하지는 않는다. 

docker의 jupyter는 그럴 수 없기 때문에 token 값을 터미널에서 복사해서 입력해야 하는 불편함이 있다. 비밀번호를 직접 설정하는 편이 사용하기 편하다. 

![docker_jupyter5]({{site.baseurl}}/assets/img/linux/docker_jupyter5.png)

비밀번호 설정의 경우, 직접적으로 입력할 수 없고 해시 알고리즘을 통해 나온 값을 입력해야 한다.

터미널에서 python을 실행하여 passwd()를 실행하면 암호를 입력받고 hash결과를 출력해준다. 이를 복사해서 붙여넣으면 된다.

![docker_jupyter3]({{site.baseurl}}/assets/img/linux/docker_jupyter3.png)

![docker_jupyter4]({{site.baseurl}}/assets/img/linux/docker_jupyter4.png)

이제 docker에서 jupyter lab(notebook)을 실행하고 브라우저에서 `localhost:8889` ( 8889는 미리 설정한 포트 )를 실행하면 docker의 jupyter와 연결이 된다.


