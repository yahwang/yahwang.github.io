---
layout: post
title: redash에 google sheets 연결하기
date: 2020-09-08 00:00:00 am
permalink: posts/94
description: redash DataSource에 google sheets를 연결해본다.
categories: [Data, DataViz]
tags: [redash, google sheets]
---

> redash DataSource에 google sheets를 연결해본다.

redash에서 기본적으로 잘 정리된 문서와 영상을 제공해주지만 정리를 한 번 해둔다.

Data Source에서 Google Sheets를 선택하면 설정 안내 문서를 바로 확인할 수 있다.

### GCP 프로젝트 및 API 설정

![redash-googlesheets_1]({{site.baseurl}}/assets/img/viz/redash-googlesheets_1.png)

API Credentials Page에 접속해서 프로젝트를 먼저 생성하고 서비스 계정을 생성한다.

( 사용자 인증 정보 만들기 - 서비스 계정 만들기 혹은 서비스 계정 관리 메뉴 직접 선택 가능 )

프로젝트 - 뷰어 권한을 통해 Google Sheets 접속 권한을 받을 수 있다.

여기서, 생성한 서비스 계정 ID(e-mail)는 나중에 구글 시트에 공유 권한을 주기 위해 사용된다.

![redash-googlesheets_2]({{site.baseurl}}/assets/img/viz/redash-googlesheets_2.png)

또한, API 및 서비스 - 라이브러리에서 프로젝트의 Google Sheets API 사용을 설정해주어야 한다.

![redash-googlesheets_3]({{site.baseurl}}/assets/img/viz/redash-googlesheets_3.png)

생성한 서비스 계정을 클릭하면 JSON Key를 생성할 수 있다. 다운로드 받은 후 redash에 업로드 하면 된다.

TEST Connection에 성공하면 절반은 성공한 것이다.

![redash-googlesheets_5]({{site.baseurl}}/assets/img/viz/redash-googlesheets_5.png)

### Google Sheets에 공유 권한 부여하기

사용하는 Google Sheets에서 공유를 선택하고 앞에서 생성한 서비스 계정 메일을 추가한다.

![redash-googlesheets_6]({{site.baseurl}}/assets/img/viz/redash-googlesheets_6.png)

redash에서 데이터를 확인하려면 Google Sheets의 URL의 일부를 사용한다.

d/와 **XXXXXXXXX** /edit 이 부분을 쿼리 창에 입력하고 옵션으로 시트 번호를 선택할 수 있다.

![redash-googlesheets_7]({{site.baseurl}}/assets/img/viz/redash-googlesheets_7.png)

Redash의 filter를 활용하려면 현재 쿼리를 단순히 저장 후 QRDS 기능을 통해 활용할 수 있다.

![redash-googlesheets_8]({{site.baseurl}}/assets/img/viz/redash-googlesheets_8.png)

참고 :

The caller does not have permission 오류가 나는 경우, datasource 접속을 다시 설정해보거나 잠시 기다린 후 사용하면 된다.

### QRDS로 활용하기

QRDS는 Query Results Data Source의 약자이며, 쿼리 결과를 다시 데이터 소스로 사용하는 방법이다.

Data Source만 Query Results로 생성하고 저장한 Sheets 쿼리의 URL에서 번호를 파악한 후 활용하면 된다.

![redash-googlesheets_10]({{site.baseurl}}/assets/img/viz/redash-googlesheets_10.png)

![redash-googlesheets_9]({{site.baseurl}}/assets/img/viz/redash-googlesheets_9.png)


`References` : 

* [Google Sheets  redash document](https://redash.io/help/data-sources/querying/google-sheets){:target="_blank"}

* [How to see Google Sheets in Redash - Youtube](https://www.youtube.com/watch?v=eunlC7NFRus&feature=emb_title){:target="_blank"}