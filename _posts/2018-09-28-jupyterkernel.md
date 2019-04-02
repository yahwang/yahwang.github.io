---
layout: post
title: Jupyter에서 kernel 다루기 (+ 다중커널)
date: 2018-09-28 03:00:00 pm
permalink: posts/42
description: jupyter에서 kernel관련 발생할 수 있는 오류와 다중커널에 대해 다룬다.
categories: [Dev, DevOps]
tags: [Ubuntu, Jupyter] 
---

> Jupyter에서 kernel이라 부르는 환경에 대해 알아본다.

Jupyter에서는 프로그래밍 언어의 실행환경을 `kernel`이라고 부른다. 

Jupyter는 Python 뿐만 아니라 R, Julia 등 많은 언어를 지원한다. 여기서는 Python만 활용하여 kernel에 대해 알아본다. 

Python을 여러 버전을 설치할 경우, kernel 개수를 확장하여 다른 환경의 Jupyter를 사용할 수 있다. 보통 다른 버전의 Python은 가상환경을 새로 만들어서 사용하기 때문에 가상환경에 kernel을 설정할 수 있다.

anaconda3가 설치된 docker에서 테스트를 진행했다.

#### kernel 확인

다음 명령어를 사용하면 현재 kernel에 대해 알 수 있다. 기본 커널은 현재 가상환경에 맞는 python 버전을 연결해주는 역할을 한다.

``` python
jupyter kernelspec list
```

![jupyter_kernel1]({{site.baseurl}}/assets/img/linux/jupyter_kernel1.png)

## kernel을 하나로 사용하는 경우 ( 일반적인 경우 )

python2 버전 가상환경을 새로 생성하여 사용하는 경우, Python2 커널이 자동으로 생성된 것을 확인할 수 있다. 다시 Python3 환경으로 넘어가면 Python2 커널은 자동으로 사라진다.

![jupyter_kernel3]({{site.baseurl}}/assets/img/linux/jupyter_kernel3.png)

문제는 Python3나 2 내에서 버전이 약간 다른 경우, kernel이 버전을 제대로 인식하지 못하는 경우가 있다.

예를 들면, anaconda3로 3.6버전을 설치한 상태이고 Python3.5 가상환경을 새로 만들었다. 이 때 kernel이 Python3.5가 아닌 여전히 Python3.6으로 인식할 수 있다.

이 때는 다음과 같은 명령어로 해결한다. 가상환경을 종료했다가 다시 실행하면 다음부터는 제대로 작동하는 것을 확인할 수 있다.

``` python
ipython kernel install --user
또는 python -m ipykernel install --user
```

![jupyter_kernel2]({{site.baseurl}}/assets/img/linux/jupyter_kernel2.png)

## 다중커널 만들기

jupyter는 서로 다른 가상환경도 같은 kernel 환경을 공유한다. 자동으로 인식하는 kernel 외에 새로 kernel을 추가하면 어떤 환경에서도 사용할 수 있다.

매번 다른 가상환경의 Python을 사용하기 위해 환경을 옮겨다닐 필요 없이 다중커널을 설정하면 하나의 가상환경에서 모두 활용할 수 있다. 

### 명령어 사용하는 법

display-name은 브라우저 상에서 표시되는 커널명으로 아래는 예시일 뿐 자유롭게 바꿔도 상관없다.

``` python
# 각각의 가상환경 내에서 실행한다.
ipython kernel install --user --name 가상환경 --display-name "Python(가상환경)"
또는 python -m ipykernel install --user --name 가상환경 --display-name "Python(가상환경)"
```

![jupyter_kernel4]({{site.baseurl}}/assets/img/linux/jupyter_kernel4.png)

### 직접 만드는 법 ( 명령어 방법이 안 통하는 경우)

위의 방법이 안되는 경우, 직접 kernel을 새로 생성할 수 있다.

jupyter kernelspecl list에서 확인가능한 기본 kernel의 폴더에서 수정하면 된다. 보통 ~/.local/share/jupyter/kernels 구조이다.

기본 Python3 커널 폴더를 보면 kernel.json이 있는데 이 파일만 수정하면 새로운 커널을 만들 수 있다.

![jupyter_kernel7]({{site.baseurl}}/assets/img/linux/jupyter_kernel7.png)

먼저, 기본 커널을 복사하여 새로운 폴더이름(추가할 가상환경)으로 만든다.

![jupyter_kernel8]({{site.baseurl}}/assets/img/linux/jupyter_kernel8.png)

그 다음 kernel.json을 편집기를 사용해 수정하면 된다.

![jupyter_kernel10]({{site.baseurl}}/assets/img/linux/jupyter_kernel10.png)

display_name과 python이 들어간 부분을 가상환경에 맞게 바꿔줘야 한다. 가상환경에서 `which python` 명령어를 통해 경로를 확인하고 수정해주면 된다.

이런 식으로 kernel 폴더를 새로 생성하고 kernel.json만 수정하게 되면 바로 kernel이 적용된 것을 확인할 수 있다.

![jupyter_kernel9]({{site.baseurl}}/assets/img/linux/jupyter_kernel9.png)



kernel 2개를 직접 추가하여 만든 모습이다.

![jupyter_kernel5]({{site.baseurl}}/assets/img/linux/jupyter_kernel5.png)

jupyter lab에서는 다음과 같이 확인할 수 있다.

![jupyter_kernel6]({{site.baseurl}}/assets/img/linux/jupyter_kernel6.png)

#### jupyter kernel 삭제

``` python
jupyter kernelspec uninstall kernel명
```
