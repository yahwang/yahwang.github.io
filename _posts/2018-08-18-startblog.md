---
layout: post
title: github 블로그를 위한 Jekyll 설치 및 실행 ( Ubuntu 기준)
date: 2018-08-18 10:00:00 pm
permalink: posts/39
description: Githubpages 블로그를 위해 Jekyll 설치 후 로컬에서 구동하는 법을 알아본다.
img: thumbnail/githubpage.png 
categories: [Note, Blog]
tags: [Jekyll, Githubpages] 
---

> github 블로그(Github pages)를 위한 Jekyll을 설치하고 로컬에서 실행해본다.

#### Jekyll은 아주 심플하고 블로그 지향적인 정적 사이트 생성기라고 한다.

Github pages는 [Jekyll](https://jekyllrb.com/){:target="_blank"}을 사용하여 만들어야 한다.

Jekyll을 PC에 설치하면 github에 업로드하기 전에 생성된 사이트를 확인하고 수정할 수 있다.

### ruby 설치

먼저, rvm을 통해 ruby를 설치해야 한다. (rvm = ruby version manager)

[https://rvm.io/](https://rvm.io/)에 접속하여 첫번째 gpg 명령을 복사하여 실행한다.

![rvm]({{site.baseurl}}/assets/img/note/rvm.jpg)

다음 명령어를 실행하면 rvm과 ruby가 최신버전으로 자동 설치된다.

``` python
curl -L https://get.rvm.io | sudo bash -s stable --ruby
## --ruby==버전 지정 가능
# ruby install 버전으로 설치도 가능하다.
```

![ruby]({{site.baseurl}}/assets/img/note/ruby.png)

ubuntu에 기본으로 ruby가 설치되어 있다. 하지만, jekyll 최신버전을 사용하기 위해서는 ruby도 최신버전이 필요하다.

시스템의 기본 ruby를 방금 설치한 최신버전으로 변경해야 한다.

![rvmdefault]({{site.baseurl}}/assets/img/note/rvmdefault.png)

`rvm is not a function error`가 발생하는 경우, 터미널에서 Edit - Preferences을 실행하고 

`run command as a login shell`을 체크한다.

![rvmerror]({{site.baseurl}}/assets/img/note/rvmerror.png)

### jekyll 환경 구성

``` python
gem install jekyll bundler
```

jekyll template을 새로 생성하고 실행해보았다.

``` python
jekyll new . # 현재 폴더에 jekyll template 생성
jekyll serve --livereload
# 또는 bundle exec jekyll serve --livereload
```

`http://localhost:4000`을 실행하면 사이트가 생성된 것을 확인할 수 있다.

`--livereload`는 jekyll template 내 파일을 수정하고 저장하면 실시간으로 반영되는 것을 브라우저에서 확인할 수 있다.

![jekyllexec]({{site.baseurl}}/assets/img/note/jekyllexec.jpg)

jekyll site가 실행된 모습

![jekyllsite]({{site.baseurl}}/assets/img/note/jekyllsite.jpg)

만약, 기존에 사용하던 template의 경우, 실행 오류가 생길 수 있다.

`bundle install`을 먼저 실행해서 실행환경을 맞춰줘야 한다.

![jekyllerror]({{site.baseurl}}/assets/img/note/jekyllerror.png)

`References` : 

* [Jekyll 한글 설명](https://jekyllrb-ko.github.io/docs/home/){:target="_blank"}