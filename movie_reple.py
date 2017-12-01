from bs4 import BeautifulSoup
import re
import random
from time import sleep
import math
import requests

# point : 점수 / reple : 댓글 / count : 댓글 총 건수
while 1:
    movieName = input("영화제목 입력 : ")
    queryUrl = "https://search.naver.com/search.naver?ie=utf8&query=" + movieName
    soup_queryUrl = BeautifulSoup(requests.get(queryUrl).content, 'html.parser')
    movieTag = soup_queryUrl.find('div', class_="movie_info section")
    if movieTag:
        codeTag = movieTag.find('a', href=re.compile("code"))
        break
    else:
        print("검색결과가 없습니다.")
# 숫자로 이루어진 정규식
condition = re.compile('\d+')
# 영화코드값을 찾는다.
code = condition.findall(codeTag['href'])[0]
print("영화코드 : " + code)
baseUrl = "http://movie.naver.com/movie/bi/mi"

# 기본 사이트는 /point (기본 추출용도)
# codeUrl = "%s/point.nhn?code=%s" % (baseUrl, code)

# infoUrl 댓글참여건수 추출용
infoUrl = "%s/pointWriteFormList.nhn?code=%s&type=after" % (baseUrl, code)
soup_infoUrl = BeautifulSoup(requests.get(infoUrl).content, 'html.parser')
count = list(soup_infoUrl.find('strong', class_="total").children)[3].get_text()
print("리뷰 참여건수 : %s" % count)
# count를 int로 변환 후 계산값 올림처리 ceil : 올림함수
pageNum = math.ceil(int(count.replace(",", ""))/5)
print("총 페이지수 : %d" % pageNum)
# 정렬 기준 order -> highest : 평점 높은 순 lowest : 평점 낮은 순 newest : 최신순 sympathyScore : 호감순
while 1:
    orderNum = int(input('정렬 기준(숫자) 호감순(1) 최신순(2) 평점 높은 순(3) 평점 낮은 순(4) : '))
    if orderNum == 1:
        order = "sympathyScore"
        break
    elif orderNum == 2:
        order = "newest"
        break
    elif orderNum == 3:
        order = "highest"
        break
    elif orderNum == 4:
        order = "lowest"
        break
    else:
        print("다시 입력하세요.")
# 평점/댓글 주소는 /pointWriteFormList
# 관람객 평점만 보기 onlyActualPointYn=Y or N
repleUrl = "%s/pointWriteFormList.nhn?code=%s&type=after&order=%s&onlyActualPointYn=N&page=" % (baseUrl, code, order)
# 원하는 페이지 수를 입력받는다. 페이지당 5개 출력
pages = int(input('페이지수를 입력(1page에 5개) : '))+1
# txt 파일로 저장하기 위해 파일 생성
file = open('C://users/ambition/desktop/movie_review.txt', 'w', encoding='utf-8')
#
repleSum = 0
# 입력한 page수 만큼 반복
for page in range(1, pages):
    # 기본 url과 페이지 수를 합친다.
    URL = repleUrl+str(page)
    soup_repleUrl = BeautifulSoup(requests.get(URL).content, "html.parser")
    # score_result 태그를 찾는다.
    items = soup_repleUrl.find('div', {'class': 'score_result'})
    # 모든 li 태그(평점+댓글)를 찾는다.
    tags = items.findAll('li')
    for tag in tags:
        # 점수 태그를 찾아서 string으로 변환
        point = tag.find('div', class_="star_score").find('em').get_text(strip=True)
        # 댓글 태그를 찾는다.
        reple_tag = tag.find('div', class_="score_reple")
        # 시간 태그는 dt 태그 안에 존재한다. dt의 children을 list화 한 후 세번째 값이 시간
        time = list(reple_tag.find('dt').children)[3].get_text()
        # 댓글 텍스트 태그(p)를 string으로 변환
        reple = str(reple_tag.find('p').get_text(strip=True))
        # 관람객 제거
        if "관람객" in reple:
            reple = reple.replace("관람객", "")
        # BEST 제거
        if "BEST" in reple:
            reple = reple.replace("BEST", "")
        repleSum += 1
# 결과 출력용
# print("%s - %s -%s-" % (point, reple, time))
        # 댓글을 txt파일에 입력
        # file.write(reple + '\n')
        file.write("평점: %s\n" % point)
        file.write("댓글: %s\n" % reple)
    # 크롤링을 위한 delay 마지막엔 합계 출력
    # 2에서 7초 사이 랜덤으로 시작
    waitNum = int(random.randint(2, 7))
    if page == (pages-1):
        file.write("리뷰합계 : %d \n" % repleSum)
        print("리뷰합계 : %d" % repleSum)
    else:
        print("%d page 기다리는 중 %d초 %d page 남음" % (page+1, waitNum, pages-1-page))
        sleep(waitNum)
# 파일 닫기
file.close()
