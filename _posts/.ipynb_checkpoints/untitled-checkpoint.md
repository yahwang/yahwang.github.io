---
layout: post
title: binder(beta) - Github 내 Jupyter notebook(python)을 설치없이 보는 법
date: 2017-09-12 00:00:00 +0300
description: # Add post description (optional)
img: #binder(main).jpg  Add image post (optional)
tags: #[Jupyter]  add tag
---
> jupyter notebook이 Docker 이미지로 생성되어서 github 내 존재하는 .ipynb 파일들을  열어볼 수 있다.

<https://mybinder.org>
![binder_main]({{site.baseurl}}/assets/img/binder(main).png)

사용 방법은 github주소를 넣고 launch를 누르면 자동으로 Jupyter로 연결된다.

> 공유한 링크로 접속 시 token 문제 해결방법

![binder_token]({{site.baseurl}}/assets/img/binder(token).png)

크롬 개발자도구(F12)를 활용해 token 값을 알아내고 그 값을 입력한다.

![binder_find_token]({{site.baseurl}}/assets/img/binder(token2).png)

### 장점
* 링크 공유를 통해 다른 PC, 핸드폰에서도 볼 수가 있다.

### 단점
* 파일이 많으면 실행하는 데 오래 걸린다.
* custom 모듈을 설치할 수가 없어서 재실행을 할 수 없다.
* 아직 python 언어만 지원하는 듯하다.


