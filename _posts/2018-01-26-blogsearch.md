---
layout: post
title: github 블로그에 검색 도구 만들기(TipueSearch)
date: 2018-01-26 05:00:00 pm
permalink: posts/21
description: Jekyll Template을 활용하여 Github pages 블로그를 만든다. # Add post description (optional)
img: thumbnail/githubpage.png  # Add image post (optional)
categories: [Note, Blog]
tags: [Jekyll, Githubpages] # add tag
---

> Tipue Search is a site search jQuery plugin. It's free, open source, responsive and fast.

Tipue search는 내부 JS 알고리즘을 통해 검색결과를 보여주는 기술이다. 검색은 내부 글을 포함한 모든 텍스트를 대상으로 이루어진다.

[tipue search 데모 SearchBox](http://www.tipue.com/search/demos/static/){:target="_blank"} - 박스 안에 검색하면 결과가 화면에 나온다.

![tipue_ex]({{site.baseurl}}/assets/img/note/tipue_ex.png)

Github 블로그에 적용시키기 위해 잘 정리된 [jekyll-tipue-search](https://github.com/jekylltools/jekyll-tipue-search){:target="_blank"} repository를 기반으로 검색 도구를 만들었다.

### 주요 파일

폴더는 [jekyll-tipue-search](https://github.com/jekylltools/jekyll-tipue-search){:target="_blank"}에서 다운받을 수 있다. 

기본적으로 assets 폴더 내에 tipuesearch 폴더를 넣고 search.html은 메인 폴더 내에 위치하면 된다.

![tipue_file]({{site.baseurl}}/assets/img/note/tipue_file.png)

`search.html` : 검색 화면을 보여줄 html

`tipuesearch_set.js` : search attribute(속성)를 설정한 JS

`tipuesearch_content.js` : search에 활용할 posts를 구성한다. ( include, exclude를 설정한 posts를 검색 대상에서 제외한다.)

검색 대상을 정리한 뒤 tipuesearch라는 변수를 만들어  min.js로 넘기는 역할을 한다.

`tipuesearch_min.js` : search function과 결과 화면을 구현한 JS

### head에 추가할 속성

``` python
<!-- tipuesearch -->
<link rel="stylesheet" href="/assets/tipuesearch/css/tipuesearch.css">
# 조건식은 search.html에 접속할 경우 tipuesearch JS를 불러온다. 
"{"% if page.tipue_search_active %"}"
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>   
<script src="/assets/tipuesearch/tipuesearch_content.js"></script>
<script src="/assets/tipuesearch/tipuesearch_set.js"></script>
<script src="/assets/tipuesearch/tipuesearch.min.js"></script>
"{"% endif %"}"
```

### 검색 도구 search box 구성

form 태그를 search.html이든 다른 원하는 레이아웃에 삽입하면 된다.

``` python
<!-- search box -->
<form action="{{ site.baseurl }}/search">
  <div class="tipue_search_box">
    <img src="{{ "/assets/tipuesearch/search.png" | relative_url }}" class="tipue_search_icon">
    <input type="text" name="q" id="tipue_search_input" pattern=".{3,}" title="최소 3글자 이상" required></div>
  <div style="clear: both;"></div>
</form>
```

### 검색 결과 search.html 구성

``` python
---
title: Search
description: "Search this site"
layout: main
permalink: /search/
tipue_search_active: true # tipuesearch function을 실행하라는 의미
exclude_from_search: true # tipuesearch 검색대상에서 제외하라는 의미
---
<div id="tipue_search_content"></div> # 이 부분은 search_content.js가 담당한다.
<script>
$(document).ready(function() {
  $('#tipue_search_input').tipuesearch({
    'wholeWords' : false, 
    'showTime' : false  });
});
</script>
```

`wholeWords` : 단어 검색 여부 한글 검색을 위해서는 false가 필수이다.

`showTime` : 검색 결과에 걸린 시간 표시 여부

그 외에 다양한 속성은 Tipue search 메인 페이지에서 확인할 수 있다.

### _config.yml 구성

이 설정이 content.js에서 tipuesearch 변수를 구성하는 데 영향을 준다.

``` python
# 기본적으로 posts에 들어있는 게시글은 자동으로 선택된다.
tipue_search:
  include: # 포함할 url을 선택한다.
    pages: false # posts 폴더 이외에 다른 문서 선택 여부 (true일 경우 모든 url이 포함된다.)
    collections: []
  exclude: # 제외시킬 url을 선택한다.
    files: [search.html, index.html, tags.html]
    categories: []
    tags: []
```

공식사이트에서 다양한 설정에 대해 더 알아볼 수 있다.

`Link` : 

* [Tipue search](http://www.tipue.com/search/){:target="_blank"}
