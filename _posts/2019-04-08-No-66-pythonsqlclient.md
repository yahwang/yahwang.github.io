---
layout: post
title: pymysql(MySQL)과 psycopg2(PostgreSQL) 사용하기
date: 2019-04-08 10:00:00 pm
update: 2021-09-12 00:00:00 am
permalink: posts/66
description: Python SQL client 라이브러리인 pymysql(MySQL)과 psycopg2(PostgreSQL) 사용법을 알아본다.
categories: [Data, SQL]
tags: [pymysql, psycopg2, copy_from, Python, StringIO]
---

> Python SQL client 라이브러리인 pymysql(MySQL)과 psycopg2(PostgreSQL) 사용법을 알아본다.

## 0. 알아두어야 할 내용

pymysql은 순수 python으로만 만들어져 있어 mysql 연결 시 C compiler와 추가 라이브러리 설치를 요구하지 않는다.

psycopg2의 경우, psycopg2-binary로 설치하면 pymysql처럼 추가 설치 없이 PosgresSQL에 연결할 수 있다.

production 환경 또는 성능이 중요한 경우, **mysqlclient**와 **psycopg2**를 사용하기를 권장한다.

## pymysql - mysql client for python

설치 : pip install PyMySQL

### 데이터 읽기

**mysql과 연결된 cursor라는 객체를 통해 SQL을 처리한다.**

#### connection 설정

cursorclass를 DictCursor로 설정 => return값을 dict 형태로 표현한다는 의미


```python
import pymysql
from pymysql.constants import CLIENT
import pandas as pd
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='mysql',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             client_flag=CLIENT.MULTI_STATEMENT
                             )

cursor = connection.cursor() # 객체를 가져오는 함수
```

cursor에서 SQL문을 실행시키고 실행 결과값을 fetch 함수를 통해 가져온다. 

기본적으로 하나의 명령만 수행한다. 세션 변수가 필요하거나 여러 명령을 한 번에 수행하려면 **client_flag** 옵션을 적용하면 된다.

```python
sql = "SELECT Host, User FROM user;"
cursor.execute(sql) # SQL문 실행
# 결과값의 개수가 출력
```

    4


fetch로 return한 값은 cursor 객체에서 값이 사라진다. ( 중복으로 결과를 가져오지 못한다. )

fetchone : 한 개 return  |  fechmany : 지정 개수 return  | fetchall : 모두 return


```python
res = cursor.fetchone()
print(res)
res2 = cursor.fetchone()
print(res2)
```

    {'Host': '%', 'User': 'root'}
    {'Host': 'localhost', 'User': 'mysql.session'}



```python
res3 = cursor.fetchmany(size=4)
```

    [{'Host': '%', 'User': 'root'},
     {'Host': 'localhost', 'User': 'mysql.session'},
     {'Host': 'localhost', 'User': 'mysql.sys'},
     {'Host': 'localhost', 'User': 'root'}]


```python
res = cursor.fetchall()
```

    [{'Host': '%', 'User': 'root'},
     {'Host': 'localhost', 'User': 'mysql.session'},
     {'Host': 'localhost', 'User': 'mysql.sys'},
     {'Host': 'localhost', 'User': 'root'}]


```python
pd.DataFrame(res)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: center;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th></th>
      <th>Host</th>
      <th>User</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>%</td>
      <td>root</td>
    </tr>
    <tr>
      <th>1</th>
      <td>localhost</td>
      <td>mysql.session</td>
    </tr>
    <tr>
      <th>2</th>
      <td>localhost</td>
      <td>mysql.sys</td>
    </tr>
    <tr>
      <th>3</th>
      <td>localhost</td>
      <td>root</td>
    </tr>
  </tbody>
</table>
</div>



일반적인 cursor의 경우, tuple 형태로 값만 출력된다. ( column명에 대한 추가 작업이 필요 )


```python
# cursorclass를 명시하지 않은 경우
connection2 = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='mysql',
                             charset='utf8mb4')
```


```python
cursor2 = connection2.cursor()
cursor2.execute("SELECT Host, User FROM user;")
res2 = cursor2.fetchall()
res2
```

    (('%', 'root'),
     ('localhost', 'mysql.session'),
     ('localhost', 'mysql.sys'),
     ('localhost', 'root'))


```python
# LIST로 타입 변환이 필요
pd.DataFrame.from_records(list(res2), columns=["Host", "User"])
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: center;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th></th>
      <th>Host</th>
      <th>User</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>%</td>
      <td>root</td>
    </tr>
    <tr>
      <th>1</th>
      <td>localhost</td>
      <td>mysql.session</td>
    </tr>
    <tr>
      <th>2</th>
      <td>localhost</td>
      <td>mysql.sys</td>
    </tr>
    <tr>
      <th>3</th>
      <td>localhost</td>
      <td>root</td>
    </tr>
  </tbody>
</table>
</div>

### TABLE 생성

```python
# pymysql sample code
query = "CREATE TABLE users ( \
    id int(11) NOT NULL AUTO_INCREMENT, \
    email varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL, \
    password varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL, \
    PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci \
    AUTO_INCREMENT=1 ;"

cursor.execute(query)
```

    0


```python
cursor.execute("DESCRIBE users;")
pd.DataFrame(cursor.fetchall())
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: center;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th></th>
      <th>Default</th>
      <th>Extra</th>
      <th>Field</th>
      <th>Key</th>
      <th>Null</th>
      <th>Type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>None</td>
      <td>auto_increment</td>
      <td>id</td>
      <td>PRI</td>
      <td>NO</td>
      <td>int(11)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>None</td>
      <td></td>
      <td>email</td>
      <td></td>
      <td>NO</td>
      <td>varchar(255)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>None</td>
      <td></td>
      <td>password</td>
      <td></td>
      <td>NO</td>
      <td>varchar(255)</td>
    </tr>
  </tbody>
</table>
</div>


### 데이터 INSERT

INSERT 후에 cursor객체를 생성한 connection에 commit을 실행시켜야 서버에 저장된다.


```python
# %s를 활용하여 value값만 변경하여 간단히 query를 날릴 수 있다.
insert_query = "INSERT INTO users (email, password) values (%s, %s);"
cursor.execute(insert_query, ("aaa@gmail.com","12345"))
```


    1


**한 번에 여러 데이터 INSERT**

executemany는 multiple row를 insert할 때 유용하다. 데이터를 하나씩 파라미터로 받아 INSERT 쿼리를 반복 실행한다.


```python
# data는 LIST(TUPLE) 형태로
data = (('bbb@gmail.com','asdf'),('ccc@gmail.com','qwer'),('ddd@gmail.com','asd123'))
cursor.executemany(insert_query, data)
```

    3


```python
cursor.execute("SELECT * FROM users;")
pd.DataFrame(cursor.fetchall())
# 객체에만 저장되었을 뿐 DB서버에는 아직 저장되지 않은 상태
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: center;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th></th>
      <th>email</th>
      <th>id</th>
      <th>password</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>aaa@gmail.com</td>
      <td>1</td>
      <td>12345</td>
    </tr>
    <tr>
      <th>1</th>
      <td>bbb@gmail.com</td>
      <td>2</td>
      <td>asdf</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ccc@gmail.com</td>
      <td>3</td>
      <td>qwer</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ddd@gmail.com</td>
      <td>4</td>
      <td>asd123</td>
    </tr>
  </tbody>
</table>
</div>




```python
connection.commit() # 서버에 INSERT한 결과를 저장 ( 반드시 connection 변수를 활용 )
connection.close() # connection 종료
```

## psycopg2 - postgresql client for python

설치 : pip install psycopg2

기본적인 사용법은 pymysql과 동일하다.

```python
import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(database="expert", 
                        host="localhost", 
                        user="yahwang", 
                        password="", 
                        ) # return 값을 dict로
psql_cursor=conn.cursor(cursor_factory=RealDictCursor)
```

참고 : [psycopg2 cursor class](http://initd.org/psycopg/docs/extras.html#connection-and-cursor-subclasses){:target="_blank"}


#### executemany 대신 copy_from

psycopg2에서는 PostgreSQL의 COPY 명령어를 활용하는 copy_from 함수가 존재한다.

executemany는 INSERT를 반복하는 과정에서 소모되는 시간이 존재하는 반면, copy_from은 한 번의 쿼리로 해결가능하고 훨씬 빠르다.

COPY는 파일 데이터를 업로드하는 용도로 사용되기 때문에 StringIO를 통해 데이터를 파일처럼 읽을 수 있게 만든다.

``` python
import io

csv_file_like_object = io.StringIO()

# 데이터를 파일처럼
### List의 경우,
for row in data:
    csv_file_like_object.write(','.join(row) + '\n') # CSV 형태처럼 데이터 입력
### DataFrame의 경우,
df.to_csv(csv_file_like_object, header=False, index=False)

# COPY 실행(공통)
csv_file_like_object.seek(0) # 데이터의 첫 index를 가리킴
cursor.copy_from(csv_file_like_object, TABLE명, sep=',', columns=[ ... ])
```

`References` : 

* [Fastest Way to Load Data Into PostgreSQL Using Python](https://hakibenita.com/fast-load-data-python-postgresql#copy){:target="_blank"}
