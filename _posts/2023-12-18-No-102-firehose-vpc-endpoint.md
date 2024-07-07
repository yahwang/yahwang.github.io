---
layout: post
title: Kinesis Data Firehose 사용 시 주의할 사항 (with VPC Endpoint)
date: 2023-12-18 01:00:00 am
permalink: posts/102
description: Kinesis Data Firehose 사용 시 주의할 사항에 대해 알아본다.
categories: [Data, ETL]
tags: [AWS, Firehose, VPCEndpoint]
---

> AWS Kinesis Data Firehose 사용 시 주의할 사항에 대해 알아본다.

## AWS VPC 간 통신 비용

보통 보안을 위해 Private subnet에 리소스들을 띄우고 외부와 통신이 필요할 경우 NAT Gateway, ELB 등을 통해 통신한다.

Kinesis Data Firehose는 간단히 말해서 스트리밍 데이터를 안정적으로 전송해주는 AWS 서비스이다.

예를 들어, Private subnet 내에 있는 백엔드 리소스에서 Firehose로 데이터를 전송하여 S3에 데이터를 실시간으로 적재할 수 있다.

AWS SDK의 putRecord 함수를 사용하면 firehose에 데이터를 쉽게 전송할 수 있다. 여기서, 통신 비용에 대해 주의할 사항이 생긴다.

( 비용은 다른 서비스들과 통합되서 청구되기 때문에 어디서 많은 비용이 나오는 지 알기도 어렵기에 미리 아는 것이 큰 도움이 된다. )

`Private subnet에서 AWS 서비스와 통신을 위해 사용되는 방식은 NAT Gateway와 VPC Privatelink이다.`

VPC Privatelink는 VPC Endpoint를 생성해야 적용되는 기술이다. ( 제일 아래 링크 참고)

빨간 선은 VPC Privatelink 통신을 표시하고 회색 선은 NAT Gateway 통신을 표시한다.

| **핵심은 AWS 서비스들은 별도의 VPC 내에 존재한다는 것이다.** |

![firehose_vpcendpoint_3]({{site.baseurl}}/assets/img/etl/firehose_vpcendpoint_3.jpg)

AWS 청구서에서는 데이터 전송 비용에 대한 종류가 여러가지로 나뉘어져 있다.

같은 VPC 메뉴에서 설정했지만 NAT Gateway 요금은 EC2 요금 하위에 보이고 Endpoint는 VPC 요금 하위에 있다.

`VPC Endpoint와 NAT Gateway를 통한 통신 비용의 차이는 약 1/6 이다.` 

Nat Gateway는 이미 생성되어 있을 것이고 Firehose 네트워크 비용이 분리되서 청구되지 않으니 모르고 사용 중일 수도 있다.

데이터 전송 양이 많아질수록 비용절감에 대한 효과가 클 것이다.

![firehose_vpcendpoint_4]({{site.baseurl}}/assets/img/etl/firehose_vpcendpoint_4.jpg)

## VPC Endpoint 생성하기

VPC 메뉴 내 엔드포인트 생성 화면에 들어가면 AWS 서비스를 선택할 수 있다.

여기서 firehose를 검색해 선택해주고 사용하는 VPC와 subnet을 설정해주고 생성하면 된다.

![firehose_vpcendpoint_1]({{site.baseurl}}/assets/img/etl/firehose_vpcendpoint_1.jpg)

생성 후 시간이 지나 모니터링을 확인해보면 데이터가 VPC Endpoint를 통해 전송되는 것이 확인된다. 

( Firehose 서비스에 큰 장애없이 금방 적용되었다. )

![firehose_vpcendpoint_2]({{site.baseurl}}/assets/img/etl/firehose_vpcendpoint_2.jpg)

Firehose 뿐만 아니라 Cloudwatch 등 여러 서비스들에 적용할 수 있다. 

VPC Endpoint 생성만 해도 시간당 비용이 청구되기 때문에 데이터 전송 양이 적은 서비스는 오히려 생성하지 않는 것이 나을 수도 있다.

참고로, S3, Dynamodb의 경우는 Gateway 형태로 생성되며, 통신 비용은 따로 청구되지 않는다.

`References` : 

* [NAT 게이트웨이 (AWS)](https://docs.aws.amazon.com/ko_kr/vpc/latest/userguide/vpc-nat-gateway.html){:target="_blank"}

* [AWS PrivateLink란 무엇인가요? (AWS)](https://docs.aws.amazon.com/ko_kr/vpc/latest/privatelink/what-is-privatelink.html){:target="_blank"}