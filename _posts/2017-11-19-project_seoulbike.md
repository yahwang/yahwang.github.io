---
layout: post
title: 서울자전거 따릉이 대여소 크롤링
date: 2017-11-19 05:30:00 pm
description: # Add post description (optional)
img: seoulbike.png  # Add image post (optional)
tags: [Project, Python] # add tag
---

> Selenium 라이브러리를 활용한 따릉이 대여소 크롤링

서울 열린 데이터 광장에 업로드된 파일은 업데이트가 되지 않아 활용할 수 없다.

### 크롤링에 필요한 라이브러리

``` python
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import random
import pandas as pd
import time
```
### chrome을 컨트롤하기 위한 드라이버 로딩

``` python
driver = webdriver.Chrome('chromedriver(win).exe')
```

``` python
# 대여소 정보를 담을 List
locations=[]
# 총 187페이지
for num in range(1,188):
    driver.get('https://www.bikeseoul.com/app/station/moveStationSearchView.do?currentPageNo=' + str(num))
    soup = bs(driver.page_source, 'html.parser')
    # 페이지 로딩을 위한 wait time 설정 (여기서는 불필요할 수도)
    driver.implicitly_wait(3)
    # 데이터가 있는 table 태그에 접근
    loc_table = soup.find('table', class_='psboard1').find('tbody').find_all('tr')
    for row in loc_table:
        loc_info = []
        # <번호. 대여소명>에서 번호를 지우고 대여소명만 추출
        loc_name = row.select('td.pl10')[0].get_text(strip=True)
        if '.' in loc_name:
            loc_info.append(loc_name.split('.')[-1].lstrip())
        else:
            loc_info.append(loc_name)
        # 상태
        loc_info.append(row.select('td.pl10')[1].get_text(strip=True))
        # 주소
        loc_info.append(row.select('td.mhid')[0].get_text(strip=True))
        # 위도, 경도 좌표
        loc_geo = row.find('a')['param-data'].split(',')
        loc_info.append(loc_geo[0])
        loc_info.append(loc_geo[1])
        # 리스트에 location 추가
        locations.append(loc_info)
    # 트래픽 속도 조절을 위한 random time 설정    
    time.sleep(random.randint(1,3))   
```

### Tableau로 분석을 하기 위해 CSV파일로 추출한다.

``` python
# List를 데이터프레임으로 변환
df = pd.DataFrame.from_records(locations, columns=['대여소','상태','주소','위도','경도'])
# csv파일로 추출
df.to_csv('seoulbike.csv', index=False)
```
### 935개의 row를 추출하였다.

![df_seoulbike]({{site.baseurl}}/assets/img/df_seoulbike.png)

**링크 :**
* [따릉이 대여소 조회](https://www.bikeseoul.com/app/station/moveStationSearchView.do?currentPageNo=1)
