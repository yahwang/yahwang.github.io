---
layout: post
title: S3와 AWS Aurora MySQL 간 데이터 주고받기 (업로드 & 다운로드)
date: 2021-04-04 21:00:00 pm
permalink: posts/97
description: S3와 AWS Aurora MySQL 간 데이터를 주고받는 방법을 알아본다.
categories: [Data, ETL]
tags: [RDS, S3]
---

> S3와 AWS Aurora MySQL 간 데이터를 주고받는 방법을 알아본다.

Aurora MySQL에는 대용량 데이터를 쉽고 빠르게 S3와 주고받을 수 있는 기능이 있다.

## Aurora MySQL에 S3 액세스 권한 부여하기

Aurora MySQL이 S3와 데이터를 주고받으려면 DB 클러스터에 S3 액세스 권한이 있는 역할을 부여해야 한다.

여기서는 간단하게 S3 Full access를 가진 **rds-load-s3**라는 역할을 생성해서 사용한다.

특정 버킷에 대한 권한만 가진 role을 만들려면 옆 링크를 참고할 수 있다. [Aurora MySQL — Export data to S3](https://anand086.medium.com/aurora-mysql-export-data-to-s3-8c2323be1cb9){:target="_blank"}

콘솔에서 RDS 클러스터를 선택한 후 RDS에 생성한 역할을 부여한다.

파라미터 그룹 메뉴에서 Aurora MySQL에 설정된 클러스터 파라미터를 확인해보면 Role이 적용된 걸 알 수 있다. 

그렇지 않다면 수동으로도 역할 ARN 값을 등록할 수 있다.

![rds_s3_1]({{site.baseurl}}/assets/img/aws/rds_s3_1.png)

또는 *SELECT @@GLOBAL.aurora_select_into_s3_role;* 명령어로도 적용된 것을 알 수 있다.

### (Optional) DB USER에게 권한 부여하기

master(admin)에게는 default로 S3 명령어 권한이 부여된다. 다른 user들에게는 권한을 부여해야 한다.

```sql
-- export
GRANT SELECT INTO S3 ON *.* TO 'user'@'domain-or-ip-address'

-- upload
GRANT LOAD FROM S3 ON *.* TO 'user'@'domain-or-ip-address'
```

## Aurora MySQL -> S3로 데이터 다운로드하기

설정한 URI에 .part_xxxx 와 같은 파일명이 추가된다. OVERWRITE ON을 설정해야 여러 번 실행해도 URI를 그대로 재사용할 수 있다.

기본적으로 TEXT 포맷이 적용되고 CSV 포맷도 지원한다. **데이터 용도에 따라 포맷을 정하면 된다.**

다시 Aurora에 업로드를 위한 것이라면 TEXT 포맷을.

Pandas 같은 데이터 분석을 위해 데이터를 추출하는 것이라면 CSV 포맷을 추천한다.

### TEXT 포맷

```sql
SELECT * FROM [테이블명] INTO OUTFILE S3 's3:/ bucket / xxxx'
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' OVERWRITE ON;
```

### CSV 포맷

```sql
SELECT * FROM [테이블명] INTO OUTFILE S3 's3:/ bucket / xxxx'
FORMAT CSV OVERWRITE ON;
```

문자열은 " "이 포함되고 숫자는 그대로 나타난다.

    TEXT 포맷과 CSV 포맷 데이터 비교

![rds_s3_1]({{site.baseurl}}/assets/img/aws/rds_s3_2.png)

## S3 -> Aurora MySQL로 데이터 업로드하기

### TEXT 파일 ( Aurora MySQL에서 추출)

Aurora MySQL에서 다운로드한 파일은 .part_xxxx 명이 추가로 붙기 때문에 PREFIX를 활용하면

편리하게 데이터를 업로드 할 수 있다.

```sql
LOAD DATA FROM S3 PREFIX 's3:// bucket / xxxx' INTO TABLE [테이블명] 
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'
( 컬럼1, 컬럼2, ...);
```

### CSV 파일

header 컬럼이 있는 파일이라면 IGNORE 1 lines를 사용한다. 특정 컬럼 값만 업로드하려면 제일 아래에 ()안에 컬럼명을 추가한다.

```sql
LOAD DATA FROM S3 's3:// bucket /xxx.csv' INTO TABLE [테이블명] 
FIELDS TERMINATED by ',' LINES TERMINATED BY '\n' IGNORE 1 lines
( 컬럼1, 컬럼2, ...);
```

    참고

아래 명령어를 실행하면 LOAD DATA FROM S3를 실행한 기록을 확인할 수 있다.

```
SELECT * FROM mysql.aurora_s3_load_history ORDER BY load_timestamp DESC;
```

`References` : 

* [Loading data into an Amazon Aurora MySQL DB cluster from text files in an Amazon S3 bucket - AWS](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Integrating.LoadFromS3.html){:target="_blank"}

* [Saving data from an Amazon Aurora MySQL DB cluster into text files in an Amazon S3 bucket - AWS](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Integrating.SaveIntoS3.html){:target="_blank"}

* [Bulk Load Data Files in S3 Bucket into Aurora RDS](http://ramblingsofraju.com/technology/bulk-load-data-files-in-s3-bucket-into-aurora-rds/){:target="_blank"}

* [Aurora MySQL — Export data to S3](https://anand086.medium.com/aurora-mysql-export-data-to-s3-8c2323be1cb9){:target="_blank"}


