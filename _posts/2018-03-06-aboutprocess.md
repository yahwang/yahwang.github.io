---
layout: post
title: Ubuntu에서 Process와 job에 대한 이해
date: 2018-03-06 05:00:00 pm
permalink: posts/28
description: 리눅스(Linux)의 한 종류인 Ubuntu에서 Process와 jobs에 대해 알아본다.  # Add post description (optional)
img: thumbnail/ubuntu.jpg  # Add image post (optional)
categories: [Linux]
tags: [process, job, screen] # add tag
---

> Ubuntu Terminal(CLI)을 통해 process와 job을 관리할 수 있다.

### process VS job

`process`는 큰 개념으로 실행되고 있는 프로그램을 의미한다.

process를 간단히 확인하려면 ps를 활용하고 자세히 실시간으로 보려면 top을 활용할 수 있다.

![process_top]({{site.baseurl}}/assets/img/linux/ps_top.jpg)

`job`은 터미널 명령을 통한 작업만을 의미한다. 

job을 통해 process를 실행할 수 있지만 해당 터미널이 종료되면 해당 job과 함께 process는 종료된다. 또한, job은 각각의 터미널에서 따로 존재한다.

jupyter lab 실행을 통해 비교해보면 다른 터미널에서는 process는 확인되지만 job이 존재하지 않는 것을 확인할 수 있다.

![processVSjob]({{site.baseurl}}/assets/img/linux/process1.jpg)

### job 활용

job을 활용하여 process를 효율적으로 관리할 수 있다.

#### foreground & background 

기본적으로 foreground로 실행하기 때문에 현재 작업이 끝나기 전에 다른 작업을 실행할 수 없다.

`Ctrl+Z`를 통해 현재 작업을 중지(Suspend)하고 빠져나올 수 있다.

![suspended]({{site.baseurl}}/assets/img/linux/suspend.jpg)

`%+번호`를 활용해 해당 job을 명령에 사용할 수 있다.

작업을 다시 불러오려면 `fg`를 활용하면 된다. +가 있는 경우 fg만으로 바로 실행가능하며, 번호를 지정하려면 `fg %1`처럼 활용한다.

background로 작업을 실행시키는 방법은 2가지가 있다.

* 명령어 뒤에 &를 붙이는 경우
* 중지(Suspend)한 후에 bg를 통해 실행시키는 경우(foreground로 실행했을 때)

python 명령을 한 터미널에서 2가지 방법으로 모두 실행하기 위해 bg작업을 fg로 변경해서 다시 bg작업으로 바꿔보았다.

![ps_background]({{site.baseurl}}/assets/img/linux/ps_background.jpg)

강제 종료는 process와 job 모두 `kill + PID(process) or 번호(job)`를 활용하면 된다.

### screen 간단 활용법

screen은 가상 터미널을 생성함으로써 job의 단점인 해당 터미널이 종료되면 job도 사라지는 문제를 해결해준다. session이 생성되기 때문에 작업은 계속 실행된다.

다만, ps나 jobs로 확인되지 않고 `screen -list`로 확인가능하다.

Attached는 터미널에서 현재 실행된 상태, Detached는 background로 나온 상태를 의미한다.

`Ctrl + A + D`로 Detached 상태를 만들 수 있다. 새 터미널을 실행해도 `screen -r sessionID`를 통해 다시 불러올 수 있다. 

(-r 대신 -x를 사용하면 여러 터미널에서 같은 세션을 불러올 수 있다.)

![screen_ex]({{site.baseurl}}/assets/img/linux/screen_ex.jpg)

screen 세션을 종료하려면 Attached 상태에서 작업을 종료하면 된다.











