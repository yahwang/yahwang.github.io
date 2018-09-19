---
layout: post
title: 네이버 카페 게시글 크롤링
date: 2017-11-19 05:30:00 pm
permalink: posts/4
description: # Add post description (optional)
img: thumbnail/navercafe.png  # Add image post (optional)
categories: [Tech, Python]
tags: [Crawling, Selenium] # add tag
---

> Selenium 라이브러리를 활용하여 로그인 session을 유지한다. --

네이버 카페는 기본적으로 카페에 가입한 후 게시글 `읽기 권한`이 필요하다.

이 크롤링 방법은 읽기 권한이 있는 아이디로 로그인하여 크롤링하는 방법이다.

### 크롤링에 필요한 라이브러리

chromedriver를 사용하여 chrome으로 크롤링을 진행한다. chromedriver는 구글에서 검색해 쉽게 다운받을 수 있다.

참고 : chromedriver는 chrome이 설치된 상태에서 진행해야 한다. ( cannot find binary 오류 관련 )

``` python
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
# chromedriver는 다운로드 후 경로 지정을 해줘야 한다. (현재는 같은 폴더 )
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)
```

### 네이버 로그인

로그인 버튼은 css selector로 쉽게 찾을 수 있다.

![naver_login]({{site.baseurl}}/assets/img/python/naver_login.png)

``` python
# 로그인 전용 화면
driver.get('https://nid.naver.com/nidlogin.login')
# 아이디와 비밀번호 입력
driver.find_element_by_name('id').send_keys('아이디')
driver.find_element_by_name('pw').send_keys('비밀번호')
# 로그인 버튼 클릭
driver.find_element_by_css_selector('#frmNIDLogin > fieldset > input').click()
```

## 네이버 카페 크롤링

네이버 카페 게시판은 `iframe`으로 운영되어 주소창에는 아무런 변화가 없다.

크롬 개발자 도구를 활용해 게시판을 보면 `a href` 속성에 실제 주소를 확인할 수 있다.

![naver_cafe_list]({{site.baseurl}}/assets/img/python/naver_cafe_menu.png)

### 카페 크롤링 주요 키워드

`search.clubid` : 카페 별 아이디

`search.menuid` : 게시판 별 아이디

`search.page` : 게시판 페이지 번호

`articleid` : 게시글 아이디

### 게시판 목록으로 접근

iframe 구조로 된 게시판 내부 태그에 접근하기 위해서는 `switch_to_frame`이 필수이다.

``` python
base_url = 'https://cafe.naver.com/카페명/ArticleList.nhn?search.clubid=***'
driver.get(base_url + '&search.menuid=***&search.page=***')
# iframe으로 프레임 전환
driver.switch_to_frame('cafe_main')
```

게시글 크롤링 하는 방법으로는 두 가지를 생각해 볼 수 있다.

* 게시글 아이디를 통한 접속 : 목록에서 게시글 번호를 추출하는 작업이 필요

* a href 링크를 통해 접속하는 방법

여기서는 a href 링크를 활용하는 방법을 사용한다.

![naver_cafe_list]({{site.baseurl}}/assets/img/python/naver_cafe_list.png)

``` python
# href 속성을 찾아 url을 리스트로 저장한다.
article_list = driver.find_elements_by_css_selector('span.aaa > a.m-tcol-c')
article_urls = [ i.get_attribute('href') for i in article_list ]
```

### 게시글로 접근

게시글은` p 태그의 연속`으로 이루어져 있어서 합쳐주는 작업을 해야 한다.

``` python
res_list = []
# Beautifulsoup 활용
for article in article_urls:
    driver.get(article)
    # article도 switch_to_frame이 필수
    driver.switch_to_frame('cafe_main')
    soup = bs(driver.page_source, 'html.parser')
    # 게시글에서 제목 추출
    title = soup.select('div.tit-box span.b')[0].get_text()
    # 내용을 하나의 텍스트로 만든다. (띄어쓰기 단위)
    content_tags = soup.select('#tbody')[0].select('p')
    content = ' '.join([ tags.get_text() for tags in content_tags ])
    # dict형태로 만들어 결과 list에 저장
    res_list.append({'title' : title, 'content' : content})
    # time.sleep 작업도 필요하다.
# 결과 데이터프레임화
cafe_df = pd.DataFrame(res_list)
# csv파일로 추출
cafe_df.to_csv('cafe_crawling.csv', index=False)
```




