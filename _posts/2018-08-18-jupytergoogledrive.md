---
layout: post
title: JupyterLab과 GoogleDrive 연동하기 (Ubuntu 기준)
date: 2018-08-18 09:00:00 pm
permalink: posts/38
description: JupyterLab에서 GoogleDrive와 연동가능한 모듈을 설치한다.
categories: [Dev, DevOps]
tags: [Ubuntu, Jupyter, googledrive]
---

> jupyterlab에서 작업한 파일들을 Google Drive에 저장하기 위해 만들어진 모듈이다.

`Github :` [jupyterlab-google-drive](https://github.com/jupyterlab/jupyterlab-google-drive){:target="_blank"}

### @jupyterlab/google-drive 기본 설치

설치하기 위해서는 nodejs를 먼저 설치해야 한다.

``` python
sudo apt-get install npm
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs
```

![install_node]({{site.baseurl}}/assets/img/python/nodeversion.jpg)

jupyter 명령어로 @jupyterlab/google-drive 모듈을 설치한다.

``` python
jupyter labextension install @jupyterlab/google-drive
```
그 후 jupyterlab을 실행하면 google drive를 확인할 수 있다.

![google-drive]({{site.baseurl}}/assets/img/python/drive.jpg)

### Google API 설정

기존에는 로그인하면 바로 실행이 가능했지만 API 사용권한이 변경되어 추가로 작업이 필요하다.

![driveerror]({{site.baseurl}}/assets/img/python/driveerror.jpg)

[Google API Console](https://console.cloud.google.com/apis){:target="_blank"}에 접속한다.

먼저, 프로젝트를 만들어야 한다.

![googleapi1]({{site.baseurl}}/assets/img/python/googleapi1.jpg)

다시 API Console에 접속하여 라이브러리를 선택하고 `Drive API`를 사용하도록 설정한다.

![googleapi2]({{site.baseurl}}/assets/img/python/googleapi2.jpg)

사용자 인증 정보를 선택하고 OAuth 동의 화면을 선택한다.

![googleapi3]({{site.baseurl}}/assets/img/python/googleapi3.jpg)

그 다음, OAuth 클라이언트 ID를 만든다.

제한사항 - 자바스크립트에 `localhost:8888`을 입력해야 한다. ( jupyterlab 기본 서버 주소 )

![googleapi4]({{site.baseurl}}/assets/img/python/googleapi4.jpg)

만들고 나면 클라이언트 ID를 복사할 수 있다.

![googleapi5]({{site.baseurl}}/assets/img/python/googleapi5.jpg)

JupyterLab에서 Settings Editor를 선택하면 Google Drive 옵션을 설정할 수 있다.

![googleapi6]({{site.baseurl}}/assets/img/python/googleapi6.jpg)

User Overrides에 복사한 clientID를 붙여넣고 realtime은 false로 설정 후 저장한다.

오타가 나거나 제대로 입력하지 않으면 저장버튼이 활성화되지 않는다.

(realtime 기능은 API가 바뀐 후로 현재 지원하지 않고 있다.)

![googleapi7]({{site.baseurl}}/assets/img/python/googleapi7.jpg)

Google Drive를 다시 로그인하거나 새로고침하면 새로운 오류가 나타날 수 있다.

jupyterlab이 verified되지 않았다는 오류인데 advanced를 눌러 무시할 수 있다.

![googleapi8]({{site.baseurl}}/assets/img/python/googleapi8.jpg)

제대로 실행이 된다면 로그인한 표시와 폴더를 확인할 수 있다.

![googleapi9]({{site.baseurl}}/assets/img/python/googleapi9.jpg)

### 기능

* 직접 파일 생성 및 수정 가능
* 드래그를 통한 파일 업로드 가능
* 우클릭으로 로컬환경에 파일 다운로드 가능

#### 다만, ipynb 파일에서 한글을 읽지 못하는 단점이 있다.

`References` : 

* [Google API SETUP](https://github.com/jupyterlab/jupyterlab-google-drive/blob/master/docs/setup.md){:target="_blank"}

* [Troubleshooting](https://github.com/jupyterlab/jupyterlab-google-drive/blob/master/docs/troubleshooting.md){:target="_blank"}
