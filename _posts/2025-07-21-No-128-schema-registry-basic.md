---
layout: post
title: Schema Registry 기본 사용법 간단 정리
date: 2025-07-21 01:00:00 am
permalink: posts/128
description: Schema Registry 기본 사용법을 간단하게 정리한다.
categories: [DevOps]
tags: [schema-registry]
---

> Schema Registry 기본 사용법을 간단하게 정리한다. ( 지속 업데이트 예정 )

## Schema Registry 배포

Confluent Schema Registry는 소스 코드만 오픈소스로 공개하고 공식 이미지는 제공되지 않는다.

그래서 bitnami에서 제공하는 Docker 이미지를 사용했고, 실제 배포는 bitnami helm chart로 진행했다.

참고 : [bitnami/schema-registry - Docker Hub](https://hub.docker.com/r/bitnami/schema-registry){:target="_blank"}

kafka-ui에서는 클러스터마다 schema registry를 별도로 설정해야 한다.

    kafka-ui helm chart values.yaml 예시

``` yaml
yamlApplicationConfig:
  kafka:
    clusters:
      - name: dev-kafka-cluster
        bootstrapServers: dev-kafka-cluster-kafka-bootstrap.common.svc:9092
        schemaRegistry: http://dev-schema-registry.common.svc:8081
      - name: prod-kafka-cluster
        bootstrapServers: ...
        schemaRegistry: ...
```

![schema_registry_basic_1]({{site.baseurl}}/assets/img/devops/schema_registry_basic_1.png)

kafka _schemas 토픽을 통해 schema가 관리되는 것을 확인할 수 있다.

![schema_registry_basic_2]({{site.baseurl}}/assets/img/devops/schema_registry_basic_2.png)

## Schema 등록

Schema는 Subject를 기준으로 등록된다. 

구조 예시 ( TopicNameStrategy )

```
Subject: "user-events-value"
├─ Schema v1: {"type": "record", "fields": [{"name": "id", "type": "int"}]}
├─ Schema v2: {"type": "record", "fields": [{"name": "id", "type": "int"}, {"name": "name", "type": "string"}]}
```

**SubjectNameStrategy**라고 subject 이름을 결정하는 전략들이 있는데 아래 내용을 참고하면 도움이 된다.

[Confluent Schema Registry 도입기! - by Yogiyo](https://techblog.yogiyo.co.kr/confluent-schema-registry-%EB%8F%84%EC%9E%85%EA%B8%B0-54d112b9b53f){:target="_blank"}

Schema Registry는 새로운 버전 등록 시 호환성을 검사해준다. 타입에 대해서는 아래 링크를 참고하면 된다.

[Confluent schema registry의 schema 호환성](https://rmcodestar.github.io/kafka/2020/05/24/confluent-schema-registry-%ED%98%B8%ED%99%98%EC%84%B1/){:target="_blank"}

## Schema Type

등록 가능한 Schema Type은 **AVRO, PROTOBUF, JSON**이다.

### JSON

JSON Schema는 [https://json-schema.org/draft-07/schema#](https://json-schema.org/draft-07/schema#){:target="_blank"}를 따른다고 한다.

AI로 생성해 본 예시이다. [schema-registry-json-example.json - GitHub Gist](https://gist.github.com/yahwang/64e654347d36339b4e6e90f8efc7d241){:target="_blank"}

URL로 schema를 조회할 수 있다. 예시 : http://dev-schema-registry.common.svc:8081/subjects/user-events-value/versions/latest

``` python
{
 'subject': 'user-events-value',
 'version': 1,
 'id': 3,
 'schemaType': 'JSON',
 'schema': '{ ... }'
}
```

### AVRO

AVRO는 JSON보다 데이터 크기가 작고, 직렬화/역직렬화 성능이 뛰어나다. 또한 Schema Registry와 쉽게 연동할 수 있어, 

스키마 변화에 유연하게 대응할 수 있는 장점이 있다.

참고 : [4. Schema Registry와 함께 안전하게](https://suwani.tistory.com/155){:target="_blank"}

Kafka Connect를 사용할 경우 자동으로 스키마 변환이 된다고 하는데, 추후 Connect를 사용할 때 직접 확인해볼 예정이다.

### PROTOBUF

기본적으로 PROTOBUF는 Schema Registry의 .proto 정보를 런타임에서 바로 사용할 수 없다.

참고 : Databricks에서는 가능한 것으로 보인다. [Use protobuf with Confluent Schema Registry - Databricks](https://docs.databricks.com/aws/en/structured-streaming/protocol-buffers#use-protobuf-with-confluent-schema-registry){:target="_blank"}

protoc로 컴파일한 뒤 생성된 descriptor 파일을 불러와서 사용해야 한다. pyspark에서는 **from_protobuf** 함수와 함께 사용할 수 있다.

참고 : [Kafka + Protobuf + Spark Stream Processing without Schema Registry - in Medium](https://waytohksharma.medium.com/kafka-protobuf-spark-stream-processing-92281559617b){:target="_blank"}

`References` : 

* [bitnamicharts/schema-registry - Docker Hub](https://hub.docker.com/r/bitnamicharts/schema-registry){:target="_blank"}

* [bitnami/schema-registry Helm Chart Values.yaml](https://github.com/bitnami/charts/blob/schema-registry/25.1.9/bitnami/schema-registry/values.yaml){:target="_blank"}

* [AWS Glue Schema registry - in AWS](https://docs.aws.amazon.com/glue/latest/dg/schema-registry.html){:target="_blank"}

* [from_protobuf - pyspark](https://spark.apache.org/docs/3.5.3/api/python/reference/pyspark.sql/api/pyspark.sql.protobuf.functions.from_protobuf.html){:target="_blank"}
