---
layout: post
title: 연금복권 당첨번호를 확인하는 프로그램 만들기
date: 2017-12-01 05:30:00 pm
description: # Add post description (optional)
img: lotto_main.png # Add image post (optional)
tags: [Project, Python] # add tag
---

> cx_Freeze를 활용하여 exe실행파일을 만든다. with python3.6 --  

[cx_Freeze 다운로드](https://pypi.python.org/pypi/cx_Freeze){:target="_blank"}

windows 10에서 실행오류가 해결된 최신버전을 활용한다. (5 버전은 문제가 있는 듯)

설치방법 : 파일을 다운받은 후 `pip install cx_Freeze파일.whl`

conda는 아직 python3.6버전을 지원하지 않는 듯 하다.

`setup.py를 구성한 후 build를 하면 python을 설치하지 않아도 실행가능한 exe파일을 만들 수 있다.`

![lotto]({{site.baseurl}}/assets/img/lotto.png)

### setup.py

``` python
import sys
from cx_Freeze import setup, Executable
# packages : 실행파일에 포함된 모듈 ( 여기서는 2개 )
# excludes 'tkinter'은 기본 설정
# multiprocessing과 idna.idnadata는 윈도우에서 실행하기 위해 필요하다.
build_options = dict(
    packages=['multiprocessing','idna.idnadata','bs4','requests',],
    excludes= ['tkinter'] )
# 윈도우는 콘솔창에서 실행되도록 설정
base = 'Console' if sys.platform=='win32' else None
# setup 설정
setup(
    name = "LottoFinder",
    version = "1.0",
    author = "YaHwang",
    description = "find lotto number program",
    options = {'build_exe': build_options},
    # 실행할 py파일 지정, targetName : 생성될 exe파일 이름
    executables = [Executable('lotto.py', base = base, targetName = 'lotto.exe')] )
```

### exe파일 생성

같은 폴더 내 setup.py와 실행할 py파일이 위치해야 한다.

해당 폴더로 접근해 실행하면 build 폴더 안에 exe파일이 만들어진다.

``` python
python setup.py build
```

### lotto.py

``` python
from bs4 import BeautifulSoup as bs
import requests

# 해당 페이지 회차번호 또는 추첨날짜를 추출하는 함수
def info(soup, tag):
    return soup.select('h3.result_title')[0].find(tag).get_text()

baseUrl = "http://nlotto.co.kr/gameResult.do?method=win520"
soup = bs(requests.get(baseUrl).content, 'html.parser')

recent = info(soup, 'strong')
print('연금복권 1등 당첨번호 찾기\n')
print('최근 %s' % info(soup, 'span'))
print('********%s회********\n' % recent)

while True:
    while True:
        try:
            lotto_round = int(input('회차를 입력하세요 : '))
            if lotto_round <0 or lotto_round> int(recent):
                print('\n해당 회차가 존재하지 않습니다')
                continue
            break
        except ValueError:
            print("\n숫자만 입력해야 합니다")

    lottoUrl = baseUrl + '&Round=' + str(lotto_round)
    soup = bs(requests.get(lottoUrl).content, 'html.parser')
    # 첫번째 번호
    no1_1 = soup.find("ul", class_="no1_1").select("li")
    no1_1 = [number.get_text(strip=True) for number in no1_1]
    # 두번째 번호
    no1_2 = soup.find("ul", class_="no1_2").select("li")
    no1_2 = [number.get_text(strip=True) for number in no1_2]

    print('\n%s회 당첨번호\n' % info(soup, 'strong'))
    print(info(soup, 'span')+'\n')
    print(' '.join(no1_1))
    print(' '.join(no1_2))

    a = input('\n다시 하려면 r 을 입력하세요 ')
    if a in ['r', 'R', 'ㄱ', 'ㄲ']:
        continue
    else:
        break
```

`Link` :

* [연금복권](http://nlotto.co.kr/gameResult.do?method=win520){:target="_blank"}