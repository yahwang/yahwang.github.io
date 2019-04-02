---
layout: post
title: GCP에서 GPU VM Instance 생성하기
date: 2018-12-23 02:00:00 am
permalink: posts/43
description: google cloud console에서 GPU를 포함한 VM instance 생성하는 법을 알아본다.
categories: [Dev, DevOps]
tags: [GCP, GPU]
---

> Google Cloud Console에서 GPU VM instance 생성하는 법을 알아본다.

GCP Instance에서 GPU를 사용하려면 먼저 GPU 한도 승인이 필요하다.

처음 프로젝트를 생성했을 경우, VM 인스턴스 메뉴를 최초 한번 선택해서 Compute Engine 사용준비를 마쳐야한다.

![gcp_gpu0]({{site.baseurl}}/assets/img/tech/gcp_gpu_0.jpg)

### GPU 한도 신청

`IAM 및 관리자 - 할당량 메뉴`를 선택한다.

화면에서 측정항목을 선택하고 gpu를 검색하면 선택메뉴에서 `GPUs( all regions)`를 확인할 수 있다.

처음의 한도는 0으로 되어있다. 어떤 지역에서 GPU를 사용하던지 여기에서 먼저 최종적으로 사용할 모든 GPU 개수를 지정해야 한다.

다른 지역의 GPU는 기본적으로 1로 할당이 되어있는데 all regions의 GPU가 0이기 때문에 사용이 불가능하다. 
GPU를 하나 이상 사용하려면 지역별 GPU도 재할당이 필요할 거 같다.

![gcp_gpu1]({{site.baseurl}}/assets/img/tech/gcp_gpu_1.jpg)

할당량 수정을 클릭하면 메일과 전화번호를 입력하는 창이 먼저 보이고 다음으로 할당량 한도와 요청 설명을 작성해야 한다.

요청 설명은 영어로 1-2 줄로 간단하게 프로젝트를 한다거나 머신러닝 공부를 한다고 하면 된다.

![gcp_gpu2]({{site.baseurl}}/assets/img/tech/gcp_gpu_2.jpg)

왼쪽 화면은 신청이 완료되었을 때 오는 메일이고 오른쪽 화면은 GPU가 승인되었다는 확인메일이다.

GPU 승인메일이 오기까지는 몇 분 걸리지 않았다.

![gcp_gpu3]({{site.baseurl}}/assets/img/tech/gcp_gpu_3.jpg)

### GPU 포함한 Instance 생성

이제 `Compute Engine - VM Instance`에서 GPU를 포함한 가상머신을 생성할 수 있다.

머신유형에서 맞춤설정을 선택하면 화면이 바뀌고 GPU를 설정할 수 있는 창이 생긴다.

GPU의 유형과 개수에 따라 코어와 메모리가 제한된다. 아래 reference URL 참고

참고 : 먼저 코어와 메모리를 낮은 것으로 생성한 뒤에 인스턴스를 중지시키고 늘려주었을 때는 아무런 문제가 생기지 않았다.

![gcp_gpu4]({{site.baseurl}}/assets/img/tech/gcp_gpu_4.jpg)

SSH로 접속해보면 GPU가 설치된 것을 `sudo lshw -C display` 명령어로 확인할 수 있다.

nvidia 그래픽 드라이버가 설치되어 있지 않아서 nvidia-smi로 바로 확인할 수는 없다.

![gcp_gpu5]({{site.baseurl}}/assets/img/tech/gcp_gpu_5.jpg)

`References` :

* [GPU에 따른 머신유형 제한](https://cloud.google.com/compute/docs/gpus/
){:target="_blank"}
