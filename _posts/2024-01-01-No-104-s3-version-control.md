---
layout: post
title: S3 버킷 버전 관리 간단 정리
date: 2024-01-01 01:00:00 am
permalink: posts/104
description: S3 버킷 버전 관리 사용 시 정보에 대해 간단히 정리해본다.
categories: [Data, ETL]
tags: [AWS, S3]
---

> S3 버킷 버전 관리 사용 시 정보에 대해 간단히 정리해본다.

버킷 생성 시 또는 추후 속성 설정에서 버전 관리를 활성화할 수 있다.

버전 관리가 활성화된 버킷은 콘솔에서는 버전 표시를 선택하면 다음과 같이 확인할 수 있다.

![s3_ver_control_1]({{site.baseurl}}/assets/img/aws/s3_ver_control_1.jpg)

### SDK로 확인

AWS SDK 중 Python용 boto3로 설명한다.

#### list_object_versions

```python
import boto3

sess = boto3.Session(profile_name='yahwang')
s3 = sess.client('s3')
bucket = 'yahwang-bucket'
prefix = 'version_test'
```

`list_object_versions`

boto3의 경우, 이전 버전의 객체를 관리하기 위해서는 **list_object_versions** 함수를 사용해야 한다.

```python
response = s3.list_object_versions(
    Bucket=bucket,
    Prefix=prefix,
)
objects = response.get('Versions', [])
```

`list_objects_v2`

list_objects_v2 함수의 경우, 최신 버전의 객체만 확인할 수 있다.

```python
response = s3.list_objects_v2(
    Bucket=bucket,
    Prefix=prefix,
)
objects = response.get('Contents', [])
```

list_object_versions 함수에서는 VersionId와 **IsLatest** 필드를 확인할 수 있다.

최신 버전은 IsLatest 값이 True이다. 이 필드는 데이터를 관리하는 데 유용하다.

![s3_ver_control_2]({{site.baseurl}}/assets/img/aws/s3_ver_control_2.jpg)

### 삭제 마커

버전 관리 중인 객체를 단순 삭제하는 경우, 삭제 마커(DeleteMarkers) 객체가 생긴다.

삭제 마커로 인해 기존 객체는 보이지 않지만 존재한다는 것을 인지해야 한다.

boto3로 확인해보면 기존 객체의 IsLatest 필드 값이 False로 변경된다.

콘솔에서는 버전을 표시하지 않는 경우, 객체가 마치 없는 것처럼 보인다.

![s3_ver_control_3]({{site.baseurl}}/assets/img/aws/s3_ver_control_3.jpg)

list_object_versions를 통해 삭제 마커를 확인하면, 별 차이점은 보이지 않는다. 단, IsLatest는 True이다.

```python
// DeleteMarkers 키로 확인
response = s3.list_object_versions(
    Bucket=bucket,
    Prefix=prefix,
)
markers = response.get('DeleteMarkers',[])
```

![s3_ver_control_4]({{site.baseurl}}/assets/img/aws/s3_ver_control_4.jpg)

### 주의할 사항( 비용 )

S3는 버전 관리된 모든 객체에 대해 비용이 청구된다. 이전 버전의 객체를 잘 관리(삭제)해야 한다.

콘솔에서 하는 대부분의 작업은 현재 객체를 삭제마커로 표시만 할 뿐 그대로 유지한다. 

콘솔로 객체를 이동시키거나 스토리지 클래스를 변경한 경우에도

기존 객체는 남아있기 때문에 버전 표시 후 삭제하지 않으면 데이터가 2배가 된다. 곧 비용도 2배이다.

#### 삭제

모든 객체를 완전히 삭제하려면 콘솔에서는 버전 표시를 설정한 후에 객체를 삭제해야 한다.

SDK로 삭제하려면 list_object_versions 함수로 객체를 확인한 후 삭제해야 한다.

최신 버전의 객체는 남겨두고 이전 객체만 삭제하려면 **IsLatest** 필드가 False인 경우만 삭제하면 된다.

참고로, 삭제마커는 IsLatest가 True이므로 별도 삭제가 필요하다.

```python
objects = response.get('Versions',[])

del_objs = []
for obj in objects:
  if obj['IsLatest'] == False:
    del_objs.append({'VersionId': obj['VersionId'], 'Key': obj['Key']})

response = s3.delete_objects(
    Bucket=bucket,
    Delete={
        'Objects': del_objs,
        'Quiet': True
    }
)
```

또한, 버킷의 수명 주기 규칙(LifeCycle)로 삭제할 수도 있다. 객체 마커까지 관리해준다.

![s3_ver_control_5]({{site.baseurl}}/assets/img/aws/s3_ver_control_5.jpg)

`References` : 

* [list_objects_v2 - in AWS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_objects_v2.html#list-objects-v2){:target="_blank"}

* [list_object_versions - in AWS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_object_versions.html){:target="_blank"}


