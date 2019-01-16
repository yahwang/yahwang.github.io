---
layout: post
title: Docker For Windows 설치할 때 생기는 오류 대처하기
date: 2018-02-08 10:00:00 pm
permalink: posts/23
description: Docker For Windows를 설치할 때 생길 수 있는 오류(error)를 정리한다.
categories: [Tech]
tags: [Docker]
---

> Docker For Windows 초기 설치할 때 생기는 오류를 정리한다.

참고 : Docker For Windows는 Hyper-V(가상머신)를 지원하는 Windows 10 pro에서 설치가 가능하다. 

Home 또는 이하 버전은 Docker Toolbox를 설치해야 한다.

### 처음 실행했을 때 발생하는 오류

Docker를 설치 후 처음 실행할 때 다음과 같은 오류가 발생할 수 있다.

![docker_error1]({{site.baseurl}}/assets/img/tech/docker_error1.png)

`해결방법` : 바탕화면에 있는 Docker 바로가기를 우클릭 - 속성 - 호환성 탭을 선택한 후 `관리자 권한`을 설정해준다.

![docker_setting1]({{site.baseurl}}/assets/img/tech/docker_setting1.png)

그 후에 다시 실행했을 때 에러 화면의 아래 reset to factory defaults Docker을 눌러주면 Docker가 정상적으로 실행된다.

### Shared Drives 공유 드라이브 설정 오류

드라이브를 선택 후 apply를 적용했을 때 Firewall detected 오류가 발생할 수 있다.

![docker_error2]({{site.baseurl}}/assets/img/tech/docker_error2.png)

제일 쉬운 방법은 방화벽을 꺼버리는 것이지만, 방화벽을 끄는 것은 위험성이 있다.

`해결방법` : 해당 PC에 설치된 백신프로그램에서 예외규칙을 설정해야 한다.

여기서는 Windows Defender 기준으로 설명한다.

제어판 - 시스템 및 보안 - Windows Defender 방화벽 - (왼쪽)고급설정 - 인바운드 규칙

파일 및 프린터 공유(SMB-In) 중에서 프로토콜 및 포트 탭에 로컬포트 445가 등록되어 있는 것을 찾는다.

해당 메뉴에서 고급 탭 - `에지 통과`를 허용 또는 응용프로그램이 결정으로 선택한다. 

재실행하지 않아도 다시 apply를 하면 정상적으로 처리된다.

![docker_setting2]({{site.baseurl}}/assets/img/tech/docker_setting2.png)