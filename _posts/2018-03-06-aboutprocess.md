---
layout: post
title: Ubuntu에서 Process와 job에 대한 이해
date: 2018-03-06 05:00:00 pm
permalink: posts/28
description: 리눅스(Linux)의 한 종류인 Ubuntu에서 Process와 jobs에 대해 알아본다.  # Add post description (optional)
categories: [Tech, Linux]
tags: [process, job, screen, cron] # add tag
---

> Ubuntu Terminal(CLI)을 통해 process와 job을 관리할 수 있다.

### process VS job

`process`는 큰 개념으로 실행되고 있는 프로그램을 의미한다.

process를 간단히 확인하려면 ps를 활용하고 자세히 실시간으로 보려면 top 또는 htop을 활용할 수 있다.

htop은 top보다 개선된 기능을 가지고 있다.

![process_htop]({{site.baseurl}}/assets/img/linux/ps_htop.jpg)

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

`screen` 명령어만 실행하면 자동으로 sessionID 생성과 함께 screen이 시작된다.

sessionID는 아래 이미지에 보이는 부분에 제일 앞 숫자를 의미한다.

Attached는 터미널에서 현재 실행된 상태, Detached는 background로 나온 상태를 의미한다.

`Ctrl + A + D`로 Detached 상태(현재 screen을 빠져나오는 것)를 만들 수 있다. 새 터미널을 실행해도 `screen -r sessionID`를 통해 다시 불러올 수 있다. 

(-r 대신 -x를 사용하면 여러 터미널에서 같은 세션을 불러올 수 있다.)

![screen_ex]({{site.baseurl}}/assets/img/linux/screen_ex.jpg)

screen 세션을 종료하려면 Attached 상태에서 작업을 종료하면 된다.

### cron

cron은 특정 시간 또는 주기로 실행할 수 있는 job을 실행시킬 수 있게 해준다.

* crontab : 특정 시간에 실행해야 할 기본 프로그램 [crontab 쉬운 사용법](https://zetawiki.com/wiki/%EB%A6%AC%EB%88%85%EC%8A%A4_%EB%B0%98%EB%B3%B5_%EC%98%88%EC%95%BD%EC%9E%91%EC%97%85_cron,_crond,_crontab){:target="_blank"}

에디터로 시간과 command를 입력하면 시스템 시간에 맞춰 자동으로 실행해준다.

date를 1분마다 기록하는 스케줄을 설정하여 확인하는 모습

![crontab]({{site.baseurl}}/assets/img/linux/crontab.jpg)

* anacron : 주기적으로 반드시 실행해야 할 job에 적합

(오류로 인해 실행이 안 되었을 경우를 체크해 시스템이 정상일 때 못했던 작업을 다시 수행한다는 장점)











