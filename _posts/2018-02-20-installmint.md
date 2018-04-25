---
layout: post
title: 윈도우10 & Mint 듀얼부팅 구현을 위한 LVM 활용기
date: 2018-02-20 02:00:00 pm
permalink: posts/25
description: 리눅스 공부를 위해 Ubuntu를 기반으로 한 Linux Mint를 활용한다.  # Add post description (optional)
img: thumbnail/mint.png  # Add image post (optional)
categories: [Tech, Linux]
tags: [LVM, fdisk] # add tag
---

> LVM(Local Volume Management)는 디스크나 대용량 저장장치를 유연하고 확장이 가능하게 다룰 수 있는 기술이다.

물리 디스크는 기본적으로 파티션이라는 단위로 용량을 나눌 수 있다.

### LVM의 이해

이미지 출처 : https://www.lesstif.com/pages/viewpage.action?pageId=20775667

![before]({{site.baseurl}}/assets/img/linux/lvm1.png)

LVM 이전의 방식은 파티션당 특정 디렉토리를 일치시켜야 한다. 

이 방식의 문제점은 특정 디렉토리에 연결된 파티션의 용량이 가득 차 용량을 증가시키고 싶을 경우, 새로운 파티션을 만들어 기존 파티션의 내용을 모두 복사한 후 기존 파티션을 삭제하는 방식을 처리해야 한다.

![lvm]({{site.baseurl}}/assets/img/linux/lvm2.png)

LVM은 파티션 대신 볼륨이라는 단위를 사용한다. 파티션을 물리 볼륨(Physical Volume)을 지정한 뒤 볼륨 그룹(Volume Group)을 지정한다. 볼륨 그룹 내에 할당된 용량 내에서 논리 볼륨(Logical Volume)을 생성하여 용량을 유연하게 관리한다.

### LVM을 테스트해보는 차원에서 128GB SSD 하나에만 적용해보았다.

**두 개의 파티션을 생성해서 하나의 볼륨 그룹으로 묶고 다시 2개의 논리 볼륨으로 나누는 작업을 한다.**

![lvm적용]({{site.baseurl}}/assets/img/linux/lvmapply.png)

### fdisk로 파티션 생성

먼재 새로운 파티션을 생성하기 위해서 `fdisk`를 활용한다. 다음 명령어를 통해 내 SSD의 logical name을 확인할 수 있다.

![fdisk1]({{site.baseurl}}/assets/img/linux/fdisk1.png)

Terminal에서 `sudo fdisk /dev/sda(logical name)`를 실행 후 n을 입력하면 partition을 만들 수 있다. 자세한 생성방법은 [링크](https://chrismckee.co.uk/creating-mounting-new-drives-in-ubuntu-azure/){:target="_blank"}에서 확인할 수 있다.

아래 그림은 partition 생성 예시이다. 용량을 설정할 때는 +숫자G 를 입력하면 되고 마지막에는 w를 입력해야 설정이 반영된다.

참고 : LVM없이 partition을 활용하려면 `mkfs -t ext4 /dev/파티션` & `mount /dev/파티션 /폴더`를 입력하면 된다.

![fdisk2]({{site.baseurl}}/assets/img/linux/fdisk2.png)

여기서 주의할 점은 파티션 타입에서 primary partition과 extended partition이 존재한다. 저장장치에 따라 다르지만 primary partition을 4개까지 지원하는 경우가 많다.

![gparted]({{site.baseurl}}/assets/img/linux/gparted.png)

Mint의 gparted를 통해 살펴보면 sda2는 윈도우가 설치되어 있고 sda1과 sda3은 윈도우 복구용으로 총 3개의 primary partition이 이미 생성되어 있다.

따라서 하나의 primary partition만 만들 수 있다. 이를 해결하기 위해서는 `extended partition`을 먼저 생성하면 primary partition을 여러 개 만들 수 있다.

[extended partition 설명](https://www.symantec.com/ko/kr/security_response/glossary/define.jsp?letter=e&word=extended-partition){:target="_blank"}

**sda4를 extended partition으로 생성하고 sda5와 sda6를 primary 파티션으로 생성하였다.**

### LVM 적용

먼저 생성한 파티션을 물리 볼륨(Physical Volume)으로 지정해야 한다.

`sudo pvcreate /dev/sda5 /dev/sda6`

그 다음 볼륨 그룹을 생성한다. 볼륨 그룹이름을 mint로 설정하고 생성한 물리 볼륨을 포함시켰다.

`sudo vgcreate mint /dev/sda5 /dev/sda6`

마지막으로 논리 볼륨(Logical Volume)을 생성하면 된다.

20G를 /home 디렉토리를 위한 볼륨으로 생성하고, 

`sudo lvcreate -L 20G -n lv_home mint`

남은 용량은 모두 /(root) 디렉토리를 위한 볼륨으로 생성했다.

`sudo lvcreate -l 100%FREE -n lv_root mint`

### 결과 확인

물리 볼륨 2개와 mint 볼륨 그룹의 논리 볼륨이 각각 생성된 것을 확인할 수 있다.

![lvmdiskscan]({{site.baseurl}}/assets/img/linux/lvmdiskscan.jpg)

듀얼 부팅 설치는 아래 [링크](http://deneb21.tistory.com/349){:target="_blank"}를 참고해서 마운트 위치를 각각 /(root)와 /home으로 지정해서 설치를 하면 된다.

`References` : 

* [fdisk로 파티션 생성하기](https://chrismckee.co.uk/creating-mounting-new-drives-in-ubuntu-azure/){:target="_blank"}

* [LVM 적용하기](https://www.digitalocean.com/community/tutorials/how-to-use-lvm-to-manage-storage-devices-on-ubuntu-16-04#create-or-extend-lvm-components){:target="_blank"}

* [윈도우 & Mint 듀얼부팅 설치하기](http://deneb21.tistory.com/349){:target="_blank"}