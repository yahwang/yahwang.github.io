---
layout: post
title: github 블로그에 페이지 나누기 설정(Pagination)
date: 2018-01-27 02:00:00 am
permalink: posts/22
description: Jekyll Template을 활용하여 Github pages 블로그를 만든다. # Add post description (optional)
img: thumbnail/githubpage.png  # Add image post (optional)
categories: [Note]
tags: [Blog, Jekyll, Githubpages] # add tag
---

> pagination은 페이지당 게시글 수를 조절하여 페이지를 넘버링할 수 있다.

`주의할 사항` : jekyll-paginate는 index.html에서만 사용이 가능하다.

Github pages는 jekyll-paginate는 기본으로 지원하기 때문에 설치없이 _config.yml을 수정하면 된다.

Local에서 확인하기 위해서는 [jekyll-paginate Github](https://github.com/jekyll/jekyll-paginate) installation을 따라하면 된다.

### _config.yml 설정

``` python
plugins:
  - jekyll-paginate # 플러그인 사용을 의미한다.(Jekyll 3)
# pagination settings
paginate: 10 # 한 페이지당 보여줄 posts 수
# :num은 페이지마다 번호를 각각 부여한다.
paginate_path: "/posts/page/:num" # 다음 페이지에 해당하는 URL
```

jekyll-paginate는 `paginators`라는 변수를 선언해주어서 pagination 구현을 편리하게 해준다.

Pagination이 잘 구현된 Kakao.github.io에서 [pagination.html](https://github.com/kakao/kakao.github.io/blob/master/_includes/pagination.html){:target="_blank"}을 가져왔다.

이 파일을 _includes에 저장하고 index.html의 마지막 부분에 삽입하였다.

### index.html 설정

`paginator.posts` : 페이지마다 할당된 posts 리스트를 의미한다. 

paginate: 10을 설정했다면 paginator.posts에 10개의 posts가 들어있다. 

다음 페이지로 이동하면 자동으로 다음 10개의 posts가 들어간다.

``` python
"{"% for post in paginator.posts %"}"
<article class="post">
  <div class="post-content">
    <h2 class="post-title"><a href="{{post.url | prepend: site.baseurl}}">{{post.title}}</a></h2>
    <p>{{ post.content | strip_html | truncatewords: 13 }}</p>
    <span class="post-date">{{post.date | date: '%Y/%m/%d'}}&nbsp;&nbsp;&nbsp;</span>
  </div>
</article>
"{"% endfor %"}"
# pagination 알고리즘 구현한 html 파일
"{"% include pagination.html %"}"
```
아래 링크에 들어가면 주요 키워드에 대한 설명이 한글로 잘 설명되어 있다. pagination.html 알고리즘을 이해하는 데 많은 도움을 준다.

`References` : 

* [페이지 나누기(한글버전)](https://jekyllrb-ko.github.io/docs/pagination/){:target="_blank"}
