---
layout: post
title: JupyterLab에서 유용한 extensions
permalink: posts/81
date: 2019-11-02 02:00:00 am
update: 2019-12-31 02:00:00 am
description: JupyterLab 1.0 버전 이후로 유용한 extension을 소개한다.
categories : [Dev, DevOps]
tags: [Jupyter, extensions]
---

> JupyterLab 1.0 버전 이후로 유용한 extension을 소개한다.

### awesome jupyter (jupyter extensions 소개)

- [Awesome Jupyter - Jupyterlab extensions](https://github.com/markusschanta/awesome-jupyter#jupyterlab-extensions){:target="_blank"}

- [Awesome JupyterLab](https://github.com/mauhai/awesome-jupyterlab){:target="_blank"}

### extension 설치방법

jupyterlab extension을 설치하기 위해서는 **nodejs**가 필수로 설치되어 있어야 한다.

`CLI를 통한 설치`

```bash
jupyter labextension install [ extension 명]
```

![jupyter_ext_2]({{site.baseurl}}/assets/img/devops/jupyter_ext_2.png)

`JupyterLab에서 설치`

Settings 설정을 해주면, 원하는 extension을 검색해서 간단히 설치할 수 있다.

![jupyter_ext_1]({{site.baseurl}}/assets/img/devops/jupyter_ext_1.png)

### 0. 일반적인 용도의 extension

| extension 명 |          설     명         |
|--------------|----------------------------|
| [jupyter-widgets/jupyterlab-manager](https://github.com/jupyter-widgets/ipywidgets/tree/master/packages/jupyterlab-manager){:target="_blank"} | ipywidget 실행을 위한 extension |
| [jupyterlab/jupyterlab-toc](https://github.com/jupyterlab/jupyterlab-toc){:target="_blank"} | table of contents 기능을 위한 extension|
| [krassowski/jupyterlab-go-to-definition](https://github.com/krassowski/jupyterlab-go-to-definition){:target="_blank"} | go to definition 기능을 위한 extension |
|[dnanhkhoa/nb_black](https://github.com/dnanhkhoa/nb_black){:target="_blank"}| black formatter 자동적용을 위한 extension|

### 1. jupyterlab-system-monitor

[github.com/jtpio/jupyterlab-system-monitor](https://github.com/jtpio/jupyterlab-system-monitor){:target="_blank"}

    0.4.1 기준

jupyterlab에서 사용하는 메모리 사용량을 확인할 수 있다. 그냥 설치만 하면 단순 사용량만 숫자로 확인 가능하다.

그래프를 보려면 메모리 사이즈 제한을 설정해야 한다. 현재, 실제로 작동하지는 않는다. 그냥 임의의 설정값일 뿐이다.

jupyter_notebook_config.py에 아래 부분을 추가하면 된다.

( config를 그동안 사용하지 않았다면 jupyter lab --generate-config로 먼저 생성한다. )

기본값으로 5초(5000ms)마다 한 번씩 업데이트 되는데 Settings에서 값을 변경할 수 있다.

``` python
#-----------------------------------------------------------
# NotebookApp(JupyterApp) configuration
#----------------------------------------------------------

c.NotebookApp.ResourceUseDisplay.mem_limit= (Size Of GB) *1024*1024*1024
```

![jupyter_ext_5]({{site.baseurl}}/assets/img/devops/jupyter_ext_5.png)

참고 : open_browser=True (default option) 를 사용할 경우, 브라우저 실행 메모리가 포함될 수 있다.

![jupyter_ext_6]({{site.baseurl}}/assets/img/devops/jupyter_ext_6.png)

### 2. jupyterlab-googledrive

[github.com/jupyterlab/jupyterlab-google-drive](https://github.com/jupyterlab/jupyterlab-google-drive){:target="_blank"}

    1.0 기준

구글 드라이브에 파일 업로드 및 수정이 가능하도록 해준다. 노트북 파일을 클라우드에서 관리하는 용도로 유용하다.

![googleapi9]({{site.baseurl}}/assets/img/python/googleapi9.jpg)

아래 Post에서 설치 후 연동하는 방법을 확인할 수 있다.

[Post - JupyterLab과 GoogleDrive 연동하기]({{site.baseurl}}/posts/38){:target="_blank"}

### 3. jupyterlab-github

[github.com/jupyterlab/jupyterlab-github](https://github.com/jupyterlab/jupyterlab-github){:target="_blank"}

    1.0 기준

github에 올린 노트북 파일을 참고하는 용도로 적합하다. github에 업로드 된 파일을 읽을 수 있다. 단, 수정하거나 업로드는 불가하다.

로컬 노트북으로 셀을 복사하고 붙여넣기는 가능하기 때문에 나름 유용하다.

**USER 명/repo 명**으로 검색 가능하다.

![jupyter_ext_3]({{site.baseurl}}/assets/img/devops/jupyter_ext_3.png)

### 4. lckr/jupyterlab_variableinspector

[github.com/lckr/jupyterlab-variableInspector](https://github.com/lckr/jupyterlab-variableInspector){:target="_blank"}

    0.3 기준

```bash
jupyter labextension install @lckr/jupyterlab_variableinspector
```

RStudio처럼 inspector 기능을 구현하려고 하는 extension이다. 휴지통 아이콘으로 변수 삭제를 할 수도 있다.

Name을 클릭하면 array나 dataframe은 value를 테이블 형태로 확인할 수도 있다.

사용방법 : 노트북 파일 빈 공간에서 우클릭 후 Open Variable Inspector를 실행하면 새로 창이 나타난다.

![jupyter_ext_4]({{site.baseurl}}/assets/img/devops/jupyter_ext_4.png)

### 5. pbugnion/jupyterlab-sql

[github.com/pbugnion/jupyterlab-sql](https://github.com/pbugnion/jupyterlab-sql){:target="_blank"}

    0.3.1 기준

    설치방법

``` python
pip install jupyterlab_sql
jupyter serverextension enable jupyterlab_sql --py --sys-prefix
jupyter lab build

# PostgreSQL 연결을 위한 psycopg2 설치
pip install psycopg2-binary

# MySQL 연결을 위한 pymysql 설치
pip install PyMySQL
pip install cryptography
```

설치 후 재실행하면 SQL 아이콘을 선택할 수 있고 연결할 DB 정보를 입력한다.

![jupyter_sql_1]({{site.baseurl}}/assets/img/devops/jupyter_sql_1.png)

``` text
PostgreSQL - postgres://user:password@ip:port/database
MySQL - mysql+pymysql://user:password@ip:port/database
```

연결하면 DB의 테이블이 보이고 더블클릭하면 1000개까지의 row를 확인할 수있다.

![jupyter_sql_2]({{site.baseurl}}/assets/img/devops/jupyter_sql_2.png)

Custom SQL query를 클릭하여 쿼리문을 입력하면(Ctrl+Enter) 결과를 확인할 수 있다.

데이터 복사 등의 추가기능은 현재 없다. 

![jupyter_sql_3]({{site.baseurl}}/assets/img/devops/jupyter_sql_3.png)

DB의 데이터를 간단히 확인할 수 있는 정도인 것 같다. 노트북 파일에서 활용되는 **ipython-sql**이 아직은 더 유용해보인다.


`References` : 

* [SQL Interface within JupyterLab](https://www.datacamp.com/community/tutorials/sql-interface-within-jupyterlab){:target="_blank"}