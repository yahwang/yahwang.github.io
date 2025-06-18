---
layout: post
title: Pyspark에서 AWS S3 데이터 읽기
date: 2019-12-09 01:00:00 am
permalink: posts/84
description: Pyspark에서 AWS S3 데이터 읽는 법을 알아본다.
categories: [Data, ETL]
tags: [Pyspark, AWS, S3]
redirect_to: /posts/125
---

> Pyspark에서 AWS S3 데이터 읽는 법을 알아본다.

## Spark에서 S3 데이터를 읽는 방법 설명

Spark는 Hadoop FileSystem API를 통해 데이터를 읽는다.

AWS S3에서는 **S3A FileSystem API**와 **EMR 전용 EMR FileSystem API(EMRFS)**를 제공한다.

EMR을 제외한 다른 Spark 클러스터에서는 모두 S3A FileSystem을 사용해야 한다.

S3A에 대한 정보는 S3, S3N을 거쳐 업그레이드된 버전이고  [S3AFileSystem 슬라이드](https://www.slideshare.net/ssuserca76a5/amazon-s3-best-practice-and-tuning-for-hadoopspark-in-the-cloud/13){:target="_blank"}에서 간단히 확인할 수 있다.

![spark_reads3_1]({{site.baseurl}}/assets/img/etl/spark_reads3_1.png)

출처 : https://www.slideshare.net/ssuserca76a5/amazon-s3-best-practice-and-tuning-for-hadoopspark-in-the-cloud

참고 : EMR의 5.17 버전부터는 **S3Select**를 활용해 필요한 데이터만 추출해서 읽을 수도 있다.

## Spark에서 S3 데이터 읽도록 설정하는 법 (EMR 제외)

먼저, **Hadoop-AWS jar**, **AWS-java-SDK**, **AWS access key** 3가지를 준비해야 한다. 

Hadoop-AWS는 하둡 버전에 맞게 선택해야 하고 그 버전에 맞는 AWS-JAVA-SDK를 선택해야 한다. 

[mvnrepository Hadoop AWS](https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws){:target="_blank"} 여기서 확인할 수 있다. 여기서는 아래 버전을 사용하고 로컬 클러스터에서 테스트했다. ( SPARK 2.4.4 prebuilt for Hadoop 2.7 기준 )

![spark_reads3_2]({{site.baseurl}}/assets/img/etl/spark_reads3_2.png)

    다운로드 링크

``` python
## 버전만 변경하면 원하는 버전 선택 가능

# hadoop-aws 2.7.3
http://central.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.7.3/hadoop-aws-2.7.3.jar
# aws-java-sdk 1.7.4
http://central.maven.org/maven2/com/amazonaws/aws-java-sdk/1.7.4/aws-java-sdk-1.7.4.jar
```

$SPARK_HOME/jars 폴더에 2개 파일을 넣어준다. 'spark.driver.extraClassPath' 옵션에 폴더를 추가하는 방법도 있다.

참고 : [스파크(Spark)에서 S3 이용하기](https://sungminoh.github.io/posts/development/use-s3-for-spark/){:target="_blank"}

### Spark 설정 setting

#### 1. $SPARK_HOME의 conf/spark-defaults.conf에 설정하는 법

 ```
spark.hadoop.fs.s3a.access.key= ACCESS_KEY
spark.hadoop.fs.s3a.secret.key= SECERT_KEY
spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem
```

#### 2. 코드에서 설정하는 법

ACCESS KEY를 인증하는 과정에서 Signature V4가 사용되어 생기는 문제가 있다. 

이를 해결하기 위해 REGION 설정과 V4 설정을 해줘야 한다. (검색과 테스트를 해본 결과)

아직 V2를 지원하는 Region의 경우에는 설정없이 사용해도 된다.

``` python
from pyspark.sql import SparkSession

conf = SparkConf()
# AWS ACCESS KEY 설정 ( conf와 중복으로 할 필요는 없음 )
conf.set("spark.hadoop.fs.s3a.access.key", " ACCESS_KEY   ")
conf.set("spark.hadoop.fs.s3a.secret.key", " SECERT_KEY ")

# S3 REGION 설정 ( V4 때문에 필요 )
conf.set("spark.hadoop.fs.s3a.endpoint", "s3.ap-northeast-2.amazonaws.com")

spark = SparkSession.builder \
    .config(conf=conf) \
    .appName("Learning_Spark") \
    .getOrCreate()

# Signature V4 설정
spark.sparkContext.setSystemProperty("com.amazonaws.services.s3.enableV4", "true")

# s3a:// 사용 예시 
df = spark.read.format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv("s3a:// 파일 위치 ")
```

참고 : [pyspark-local - dockerhub](https://hub.docker.com/r/yahwang/pyspark-local){:target="_blank"} 에서 테스트 image를 다운받아 활용해볼 수 있다.

아래 slideshare 링크를 살펴보면 S3 사용 시 주의사항에 대해 자세한 정보가 나온다.

`References` : 

* [Amazon S3 Best Practice and Tuning for Hadoop/Spark in the Cloud - slideshare](https://www.slideshare.net/ssuserca76a5/amazon-s3-best-practice-and-tuning-for-hadoopspark-in-the-cloud){:target="_blank"}

* [Using Spark to read from S3](https://www.jitsejan.com/using-spark-to-read-from-s3.html){:target="_blank"}


