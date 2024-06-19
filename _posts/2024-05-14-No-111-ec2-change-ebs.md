---
layout: post
title: EC2의 EBS 볼륨 사이즈 줄이기(교체)
date: 2024-05-14 01:00:00 am
permalink: posts/111
description: EC2의 EBS 볼륨 사이즈 줄이는 방법에 대해 알아본다.
categories: [Dev, DevOps]
tags: [EC2, EBS]
---

> EC2의 EBS 볼륨 사이즈 줄이는 방법에 대해 알아본다.

## EBS는 축소 불가

EBS는 기본적으로 볼륨 확장은 가능하지만 축소는 불가능하다. 

스냅샷은 할당된 볼륨 모두를 백업하기 때문에 볼륨 축소하는 데 사용할 수 없다.

따라서, 데이터를 복사한 EBS로 교체해야 한다.

![ec2_change_volume_1]({{site.baseurl}}/assets/img/devops/ec2_change_volume_1.jpg)

## EBS 교체 방법

EBS 교체 방식은 다음과 같다.

1. 새로운 EC2와 EBS 생성

2. 기존 EC2에서 새로운 EC2로 데이터 복사 ( scp )

    2-1. 새로운 EC2에서 ssh-keygen으로 키를 생성

    2-2. 생성된 ~/.ssh/id_rsa.pub key를 기존 EC2의 ~/.ssh/authorized_keys에 복사

    2-3. scp로 데이터 복사

3. 새로운 EC2와 기존 EC2 중지

4. 각각 EBS 볼륨 선택 후 새로운 EC2 및 기존 EC2와 볼륨 분리

5. 새 EBS 볼륨 선택 후 기존 EC2에 볼륨 연결

    루트 볼륨용으로 예약된 이름을 선택하면 된다.

6. 새로운 EC2와 기존 EBS 삭제

`볼륨 분리`

![ec2_change_volume_2]({{site.baseurl}}/assets/img/devops/ec2_change_volume_2.jpg)

`볼륨 연결`

![ec2_change_volume_5]({{site.baseurl}}/assets/img/devops/ec2_change_volume_5.jpg)

## 참고: 루트 볼륨 대체

루트 볼륨 대체 설정에 들어가보면 3가지 복원 방법이 있다.

다만, 이는 루트 볼륨 사이즈를 변경할 수는 없고 볼륨 내부를 초기화하거나 기존 스냅샷으로 복구를 선택할 수 있다.

**스냅샷의 경우, 현재 EC2와 연결된 볼륨에서 생성된 스냅샷만 복원이 가능하다.**

데이터를 복사한 새로운 볼륨으로 생성한 스냅샷으로 교체를 시도해보았으나 지원하지 않는다는 오류가 발생했다.

![ec2_change_volume_3]({{site.baseurl}}/assets/img/devops/ec2_change_volume_3.jpg)

![ec2_change_volume_4]({{site.baseurl}}/assets/img/devops/ec2_change_volume_4.jpg)

