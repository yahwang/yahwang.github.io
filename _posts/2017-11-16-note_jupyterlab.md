---
layout: post
title: JupyterLab
date: 2017-11-16 05:30:00 pm
description: # Add post description (optional)
img: jupyterlab.png  # Add image post (optional)
tags: [Note, Jupyter] # add tag
---

> Jupyter notebook이 발전한 Jupyter Lab

#### PyData Seattle 2017 유튜브 영상을 바탕으로 작성한 노트

### 기본 기능

* 화면 분할
* notebook 내 code block 숨기기
* code block drag&drop

### 대용량 파일 Load 가능

엑셀에서 소화하지 못하는 파일을 볼 수 있다.

스크롤하면 데이터를 계속 볼 수 있다.

영상에서는 trillion rows & cols 로드가 가능함을 보여주었다.

### 구글 드라이브와 연동 가능 (설치 필요)
* 구글 Docs처럼 여러 사용자와 Live 코딩도 가능하다. (아직 해보지는 않음)
* [@jupyterlab/google-drive](https://github.com/jupyterlab/jupyterlab-google-drive)

### Markdown

* preview 기능(실시간 반영) cf) 이미지는 보이지 않는다.
* console에서 코드 결과 출력 (Shift + Enter)

사용방법 : 마크다운 파일 내에서 우클릭

![jupyterlab_md]({{site.baseurl}}/assets/img/jupyterlab(md).png)

### JSON 파일 실행 및 수정

* .plotly [@jupyterlab/plotly-extension](https://github.com/jupyterlab/jupyter-renderers/tree/master/packages/plotly-extension)

![jupyterlab_json]({{site.baseurl}}/assets/img/jupyterlab(plotly).png)

* .geojson [@jupyterlab/geojson-extension](https://github.com/jupyterlab/jupyter-renderers/tree/master/packages/geojson-extension)

![jupyterlab_json]({{site.baseurl}}/assets/img/jupyterlab(geojson).png)

**링크 :**
* [PyData Seattle 2017](https://www.youtube.com/watch?v=u3gU2brTaVI)