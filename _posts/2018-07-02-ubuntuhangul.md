---
layout: post
title: Ubuntu에 한글 입력기 설치하기 (uim-byeoru)
date: 2018-07-03 00:00:00 am
permalink: posts/36
description: 리눅스 공부를 위해 Ubuntu에 한글을 설치한다.  # Add post description (optional)
categories: [Dev, DevOps]
tags: [Ubuntu, uim-byeoru, 한글] # add tag
---

> 한글 설치와 활용이 간단한 uim을 통해 한글 입력기를 설치한다.

기존에 dasom에서 확장된 nimf라는 한글입력기를 사용해왔다. 하지만 PPA 서비스가 종료되어서 새로 설치하는 법이 어려워졌다.

fcitx와 ibus-hangul을 활용하는 방법도 있지만 uim-byeoru가 설치가 더 편리하고 오류도 적은 듯하다. 

특히, 우분투 버전에 상관없이 **한/영키 설정**이 잘 된다는 점에서 윈도우 사용자에게 더 메리트가 있다. 

### 기존 키보드 세팅 확인

화면 왼쪽 상단 버튼을 누르거나 윈도우 키를 누르면 검색창이 뜬다. text entry 창을 열 수 있다.

여기서는 **Korean(101/104 ...)** 하나만을 설정한다.

english가 있다면 - 버튼으로 지울 수 있고 101/104 key는 + 버튼을 누르고 korean을 검색하면 찾을 수 있다.

![hangul_1]({{site.baseurl}}/assets/img/linux/hangul_1.png)

### UIM 설치 및 입력기로 설정

먼저 터미널에서 다음 명령어 uim byeoru를 설치한다.

``` python
sudo apt-get install uim uim-byeoru
```

참고 : 18.04의 경우 uim만 install해도 byeoru가 포함되어 있다고 한다.

설치 후, Language Support를 실행한다.

(ubuntu를 처음 설치한 사람이라면 install창이 먼저 나오는데 실행하면 된다.)

**Keyboard input method**를 선택할 수 있는데 여기서 uim을 선택한다.

참고 : 한국어가 보이는 지 확인한다. 만약에 한국어가 없다면 파란 박스 부분을 클릭하면 오른쪽 창이 보이는데 korean 설치여부를 확인한다.

![hangul_2]({{site.baseurl}}/assets/img/linux/hangul_2.png)

### UIM 한글 및 한/영 키 설정

input method를 실행한다.

바로 Global settings 창이 보이는데 default input을 **Byeoru**로 설정한다.

![hangul_3]({{site.baseurl}}/assets/img/linux/hangul_3.png)

메뉴에서 **Byeoru key bindings 1**를 선택하고 Byeoru on과 off에 각각 한/영키(hangul)를 설정한다.

Key 부분을 클릭하고 한/영키를 누르면 자동으로 hangul이라고 뜨고 Add 버튼을 통해 추가하면 된다.

![hangul_4]({{site.baseurl}}/assets/img/linux/hangul_4.png)

설정이 완료되고 재부팅을 하고 나면 한/영키를 사용할 수 있다.

우측 상단에 보이는 입력기 화면에는 영어와 한글 전환이 보이지 않을 수 있지만 사용하기에는 별로 불편함이 없다.