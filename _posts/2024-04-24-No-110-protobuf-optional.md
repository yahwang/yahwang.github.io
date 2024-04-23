---
layout: post
title: optional label과 비용효과적인 Protobuf 처리
date: 2024-04-24 01:00:00 am
permalink: posts/110
description: optional label과 비용효과적인 Protobuf 처리에 대해 알아본다.
categories: [Data, ETL]
tags: [Protobuf, Python, Firehose]
---

> optional label과 비용효과적인 Protobuf 처리에 대해 알아본다.

## 이전 상황

센서 데이터를 protobuf로 형식으로 받아 Kinesis Firehose를 통해 데이터 레이크로 전송하고 있다.

proto에는 많은 필드의 데이터와 repeated, bytes 등 다양한 타입이 포함되어 있다.

protobuf의 [json_format.MessageToDict](https://googleapis.dev/python/protobuf/latest/google/protobuf/json_format.html#google.protobuf.json_format.MessageToDict){:target="_blank"} 함수가 존재하지만 복잡한 형식을 처리하기 위해 stackoverflow에서 알게 된 코드를 활용했다.

[MessageToDict function - in stackoverflow](https://stackoverflow.com/questions/57203347/how-to-serialize-default-values-in-nested-messages-in-protobuf){:target="_blank"}

```python
def MessageToDict(message):
    message_dict = {}
    
    for descriptor in message.DESCRIPTOR.fields:
        key = descriptor.name
        value = getattr(message, descriptor.name)
    
    ...
```

이 함수는 모든 필드를 Dict 형식으로 변환해주지만 단점은 client 쪽에서 보내지 않는 필드 데이터 마저 default value로 변환한다.

예를 들어 특정 상황에서만 client에서 필드 값을 1로 보내는데 그 전에 수신자는 항상 0으로 변환한다.

하지만 모든 default value를 제외하는 것은 실제 데이터까지 제외되는 문제가 생길 수 있었다.

[Application Note: Field Presence - protobuf](https://protobuf.dev/programming-guides/field_presence/){:target="_blank"}

protobuf 3는 기본적으로 implicit presence가 적용되어 default value를 포함한 경우 메시지에 포함하지 않는다. 이로 인해

예를 들어, 수신자 입장에서는 온도 필드가 0인 경우 실제 0도인지 오류로 인해 생긴 0인지 알 수가 없다.

Firehose는 JSON 포맷을 input으로 받고 그 양에 따라 비용이 청구된다. 의미없는 default value와 필드 이름이 비용으로 연결되고 있었다.

protobuf 3.15부터 optional을 명시한 경우, **explicit presence**를 알 수 있다는 것을 알게 되었다.

[ListFields() - protobuf](https://googleapis.dev/python/protobuf/latest/google/protobuf/message.html#google.protobuf.message.Message.ListFields){:target="_blank"} 이 함수를 활용하면 client가 명시적으로 보내는 optional 필드 데이터를 확인할 수 있다.

필드 값 입력 여부는 [HasField(field_name) - protobuf](https://googleapis.dev/python/protobuf/latest/google/protobuf/message.html#google.protobuf.message.Message.HasField){:target="_blank"}를 통해 확인할 수 있다.

## optional 적용 테스트

### proto 정의

`sensor.proto`

```
syntax = "proto3";

message sensorMsg {
  string sensorId = 1;
  int32 state = 2;
  float value = 3;
  string msg = 4;
}
```

`optional_sensor.proto`

```
syntax = "proto3";

message sensorMsg {
  optional string sensorId = 1;
  optional int32 state = 2;
  optional float value = 3;
  optional string msg = 4;
}
```

### protobuf 생성

`sensor`

```python
import sensor_pb2

sensor_msg = sensor_pb2.sensorMsg()

sensor_msg.sensorId = 'sensorA'
sensor_msg.value = 10
sensor_msg.state = 0
```

`optional_sensor`

``` python
import optional_sensor_pb2

optional_sensor_msg = optional_sensor_pb2.sensorMsg()

optional_sensor_msg.sensorId = 'sensorB'
optional_sensor_msg.value = 10
optional_sensor_msg.state = 0
optional_sensor_msg.msg = ''
```

### field presence 확인

optional이 지정되지 않은 경우 필드의 존재를 확인할 수 없다.

``` python
sensor_msg.HasField('value')

=> ValueError: Field sensorMsg.value does not have presence.

optional_sensor_msg.HasField('value')

=> True
```

### ListFields 확인

optional이 아닌 경우, default value를 입력했어도 수신자는 확인할 수 없다.

```python
sensor_msg.ListFields()

[(<google._upb._message.FieldDescriptor at 0x10567d570>, 'sensorA'),
 (<google._upb._message.FieldDescriptor at 0x109d6d470>, 10.0)]
```

```python
optional_sensor_msg.ListFields()

[(<google._upb._message.FieldDescriptor at 0x1085d5430>, 'sensorB'),
 (<google._upb._message.FieldDescriptor at 0x1085d5d30>, 0),
 (<google._upb._message.FieldDescriptor at 0x1085d6230>, 10.0),
 (<google._upb._message.FieldDescriptor at 0x1085d6bf0>, '')]
```

## ListFields 활용

맨 처음 확인했던 MessageToDict를 ListFields를 활용하여 다음처럼 변경하여 사용가능하다.

```python
def MessageToDict(message):
    message_dict = {}
    
    for desc, value in message.ListFields():
        key = desc.name
        # value는 그대로 사용
    ...
```

이 함수를 적용해서 client에서 default 값을 포함하여 명시적으로 보내는 경우만 변환이 가능하였다.

실제로 Firehose 비용이 약 20% 절감되는 효과가 있었다.

`References` : 

* [Version Support - protobuf](https://protobuf.dev/support/version-support/){:target="_blank"}

* [proto3 문법의 optional label (Field presence) - by Ukjae Jeong](https://blog.ukjae.io/posts/optional-label-in-proto3/){:target="_blank"}

* [The Essential Protobuf Guide for Python](https://www.datascienceblog.net/post/programming/essential-protobuf-guide-python/){:target="_blank"}

