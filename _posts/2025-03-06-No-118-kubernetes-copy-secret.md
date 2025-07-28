---
layout: post
title: kubernetes 네임스페이스 간 secret 간단히 복사하기
date: 2025-03-06 02:00:00 am
permalink: posts/118
description: kubernetes 네임스페이스 간 secret 간단히 복사하는 법을 알아본다.
categories: [Dev, k8s]
tags: [k8s, reflector]
---

> kubernetes 네임스페이스 간 secret 간단히 복사하는 법을 알아본다.

## 개요

Kubernetes 클러스터 내에서 네임스페이스는 리소스를 논리적으로 격리하는 단위로 설계되었기 때문에, 독립적인 환경처럼 동작한다. 

Secret, ConfigMap 등 대부분의 리소스는 네임스페이스에 종속적이며, 다른 네임스페이스와 직접 공유되지 않는다.

docker registry와 같은 모든 네임스페이스에 공통적으로 필요한 secret을 수동으로 관리하기엔 번거로움이 있어 

자동화할 방법에 대해 알아보았다.

## 1. 다른 네임스페이스의 secret을 불러와서 적용하기

```sql
kubectl get secret [시크릿] -n [기존 네임스페이스] -o yaml | grep -v "creationTimestamp\|resourceVersion\|uid" | \
sed "s/namespace: .*/namespace: [네임스페이스]/" | kubectl apply -f -
```

기존에 생성한 secret이 있는 경우, 가장 간단하게 처리할 수 있는 방법이다.

( 불필요한 정보 제거하고 namespace만 변경 )

예시

```sql
kubectl get secret my-secret -n common -o yaml | grep -v "creationTimestamp\|resourceVersion\|uid" | \ 
sed "s/namespace: .*/namespace: new-space/" | kubectl apply -f -
```

## 2. kubernetes-reflector

[https://github.com/emberstack/kubernetes-reflector](https://github.com/emberstack/kubernetes-reflector){:target="_blank"}

reflector는 소스가 되는 secret, configmap 등 한 네임스페이스의 리소스를 기준으로 

다른 네임스페이스에 같은 이름의 리소스를 복사해서 생성해주고 **동기화**까지 해주는 기능이 있다.

설치는 위 github 링크를 참고하면 helm으로 바로 설치할 수 있다. ( 네임스페이스는 어디에 있든 상관없음 )

리소스에 **annotation**만 설정하면 쉽게 사용할 수 있다.

참고: helm chart를 살펴보면 동기화 실패를 할 경우를 대비해 보조 수단으로 [cron 작업](https://github.com/emberstack/kubernetes-reflector/blob/v9.0.318/src/helm/reflector/values.yaml){:target="_blank"}을 실행할 수 있기도 하다.

`reflection-allowed` 

이 리소스를 소스로 정의하겠다는 의미

`reflection-allowed-namespaces`

네임스페이스 허용 범위 ( A,B ) , 단위로 구분하고 정규식도 일부 가능한 듯 보임 

모든 네임스페이스에 적용할 경우, 생략하거나 공백문자로 처리

**아래 auto 관련 설정은 optional이나 사용하지 않으면 리소스 동기화가 되지 않기 때문에 사실상 필수이다.**

`reflection-auto-enabled`

자동으로 다른 네임스페이스에 반영하겠다는 의미

`reflection-auto-namespaces`

reflection-allowed-namespaces에 정의한 네임스페이스 중에서 사용해야 한다.

자동으로 적용할 네임스페이스 범위 ( A,B ) , 단위로 구분하고 정규식도 일부 가능한 듯 보임 

모든 네임스페이스에 적용할 경우, 생략하거나 공백문자로 처리

참고: namespace에 prefix 규칙을 두면 무분별하게 리소스가 생기는 것을 방지할 수 있어보인다.

( kube-system 이런 네임스페이스에 굳이 secret을 등록하지 않아도 되기 때문 )

`소스가 되는 시크릿 예시`

```sql
apiVersion: v1
kind: Secret
metadata:
  name: source-secret
  annotations:
    reflector.v1.k8s.emberstack.com/reflection-allowed: "true"
    reflector.v1.k8s.emberstack.com/reflection-allowed-namespaces: ""
    reflector.v1.k8s.emberstack.com/reflection-auto-enabled: "true"
    reflector.v1.k8s.emberstack.com/reflection-auto-namespaces: ""
data:
 ...
```

기존 common 네임스페이스의 my-secret에 위 annotation을 적용하면 다음처럼 모든 네임스페이스에 secret이 생성된다.

![k8s_copy_secret_1]({{site.baseurl}}/assets/img/devops/k8s_copy_secret_1.jpg)

POD의 로그를 보면 common/my-secret의 reflection이며, **Created**라는 로그가 찍히는 것을 확인할 수 있다.

![k8s_copy_secret_2]({{site.baseurl}}/assets/img/devops/k8s_copy_secret_2.jpg)

소스 시크릿인 common/my-secret의 값을 변경하면 **Patched**라는 로그가 찍히는 것을 확인할 수 있다.

![k8s_copy_secret_3]({{site.baseurl}}/assets/img/devops/k8s_copy_secret_3.jpg)

### 네임스페이스 생성 시

새로운 네임스페이스 생성 시에는 최초 한 번 기존 시크릿과 같은 이름으로 생성해야 한다. 그 이후에 동기화는 적용된다. 

빈 시크릿을 생성하고 annotation을 통해 시크릿을 복사한다.

```sql
kubectl create secret generic [시크릿] -n [네임스페이스] && \ 
kubectl annotate secret [시크릿] -n [네임스페이스] reflector.v1.k8s.emberstack.com/reflects=[소스 네임스페이스]/[시크릿]
```

예시

```sql
kubectl create secret generic my-secret -n new-space && \ 
kubectl annotate secret my-secret -n new-space reflector.v1.k8s.emberstack.com/reflects=common/my-secret
```

> reflector를 활용하면 namespace가 많은 k8s 클러스터에서 공통 secret의 변경이 필요할 때 유용하게 사용할 수 있을 것으로 보인다.

`References` : 

* [Easily Replicate your TLD TLS Certificate using Reflector - in Medium](https://medium.com/@lior.dux/easily-replicate-your-tld-tls-certificate-using-reflector-e65047dfcc77){:target="_blank"}

* [Let's encrypt w/ Cert-manager를 통해서 자동으로 갱신되는 TLS 인증서 사용하기 - in SKT Enterprise](https://www.sktenterprise.com/bizInsight/blogDetail/dev/11880){:target="_blank"}