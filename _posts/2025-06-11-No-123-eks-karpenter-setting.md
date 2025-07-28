---
layout: post
title: EKS Karpenter 설치하기 (with Terraform)
date: 2025-06-11 02:00:00 am
permalink: posts/123
description: Terraform으로 EKS에 Karpenter 설치하는 법을 간단히 정리한다.
categories: [Dev, k8s]
tags: [eks, karpenter]
---

> Terraform으로 EKS에 Karpenter 설치하는 법을 간단히 정리한다.

## 개요

[Karpenter](https://karpenter.sh/){:target="_blank"}는 필요한 만큼의 컴퓨팅 자원(노드)을 빠르고 효율적으로 프로비저닝하는 Kubernetes용 오픈소스 노드 오토스케일러이다.

오토스케일러는 대표적으로 Cluster Autoscaler와 Karpenter가 있는데 Karpenter가 프로비저닝 속도도 빠르고 많이 사용하는 것으로 보인다.

[Karpenter vs. Cluster Autoscaler – Kubernetes Scaling Tools](https://spacelift.io/blog/karpenter-vs-cluster-autoscaler){:target="_blank"} 이 글을 통해 둘의 차이를 확인할 수 있다.

현재 EKS OnDemand Node 하나를 생성해서 사용중인 상황이고 Karpenter로 Spot Instance를 프로비저닝하여 배치 작업을 실행하기로 결정하였다.

## eks 테라폼 모듈 일부 ( karpenter 설정을 위한 참고 용도 )

`주요 설정`

**enable_irsa** : IRSA를 활성화

enable_irsa는 aws load balancer controller를 사용할 때 필요해서 이미 활성화되어 있었다.

**node_security_group_tags** : EKS node shared security group에 karpenter 태그를 적용

```python

############
# NODE가 사용할 IAM role
############

module "eks_node_default_role" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-assumable-role"
  version = "5.48.0"

  create_role             = true
  role_name               = "eks-node-default"
  trusted_role_services   = [
    "ec2.amazonaws.com"
  ]

  role_description        = "EKS Node default role"
  role_requires_mfa       = false                                 
  force_detach_policies   = true                                  
  max_session_duration    = 3600                                  

  custom_role_policy_arns = [
    "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
    "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
    "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy", 
    "arn:aws:iam::aws:policy/service-role/AmazonEFSCSIDriverPolicy", 
    "arn:aws:iam::aws:policy/AmazonS3FullAccess"
  ]

  tags = {
    Service     = "eks"
  }
}

##############
# EKS CLUSTER
##############

module "yahwang_eks_cluster" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "yahwang-eks-cluster"
  cluster_version =  "1.31"

  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true
  cluster_endpoint_public_access_cidrs = ["0.0.0.0/0"]

  vpc_id                    = module.yahwang_vpc.vpc_id
  subnet_ids                = [
    module.yahwang_subnets.private_subnet_ids["private-eks-a1"].id,
    module.yahwang_subnets.private_subnet_ids["private-eks-c1"].id
  ]
  control_plane_subnet_ids  = [
    module.yahwang_subnets.private_subnet_ids["private-eks-a1"].id,
    module.yahwang_subnets.private_subnet_ids["private-eks-c1"].id
  ]

  enable_irsa               = true
  authentication_mode       = "API"

  # 자동으로 EKS node shared security group이 생성되며 태그에 적용
  create_node_security_group = true # 기본값
  node_security_group_tags = {
    "karpenter.sh/discovery" = "yahwang-eks-cluster" # 클러스터 이름을 태그로 적용
  }

  eks_managed_node_groups = {
    yahwang_eks_node_group_01 = {
      ami_type       = "AL2023_ARM_64_STANDARD"
      instance_types = ["t4g.medium"]
      use_custom_launch_template = true 
      iam_role_arn = module.eks_node_default_role.iam_role_arn

      min_size     = 1
      max_size     = 1
      desired_size = 1

      update_config = {
        max_unavailable = 1
      }
    }
  }
}
```

또한, eks가 배포되는 subnet에도 태그를 적용해야 한다.

여기서는 private-eks-a1, private-eks-c1 subnet에 태그를 적용한다.

서브넷 구성에 직접 만든 모듈을 사용 중이라 다음처럼 적용하였다. kubernetes.io는 EKS 운영을 위한 기본 태그이다.

```python
private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
    "kubernetes.io/cluster/yahwang-eks-cluster" = "shared"
    "karpenter.sh/discovery" = "yahwang-eks-cluster" # Karpenter 사용을 위한 태그
}
```

## karpenter 모듈 설정

```python
module "karpenter" {
  source = "terraform-aws-modules/eks/aws//modules/karpenter"
  version = "20.36.0"

  cluster_name = module.yahwang_eks_cluster.cluster_name
  enable_irsa = true
  irsa_oidc_provider_arn = module.yahwang_eks_cluster.oidc_provider_arn
  
  # karpenter로 배포될 Node의 IAM role
  create_node_iam_role = false
  node_iam_role_arn    = module.eks_node_default_role.node_iam_role_arn

  # eks 모듈에서 access entry를 생성해주기 때문에 충돌 방지를 위해 False로 설정
  create_access_entry = false
  # access_entry_type = "EC2_LINUX"
}
```

## karpenter helm chart 설정

```python

# helm 배포를 위한 기본 provider 설정
provider "helm" {
  kubernetes {
    host                   = module.yahwang_eks_cluster.cluster_endpoint
    cluster_ca_certificate = base64decode(module.yahwang_eks_cluster.cluster_certificate_authority_data)
    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      command     = "aws"
      args        = ["eks", "get-token", "--cluster-name", module.yahwang_eks_cluster.cluster_name]
    }
  }
}

resource "helm_release" "karpenter" {
  name       = "karpenter"
  namespace  = "karpenter"
  repository = "oci://public.ecr.aws/karpenter"
  chart      = "karpenter"
  version    = "1.4.0"

  create_namespace = true

  # https://github.com/aws/karpenter-provider-aws/blob/v1.4.0/charts/karpenter/values.yaml
  values = [
    yamlencode({
      serviceAccount = {
        name = "karpenter"
        annotations = {
          "eks.amazonaws.com/role-arn" = module.karpenter.iam_role_arn
        }
      }
      settings = {
        clusterName = module.yahwang_eks_cluster.cluster_name
        interruptionQueue = module.karpenter.queue_name
      }
      replicas = 1
      controller = {
        resources = {
          requests = {
            memory = "256Mi"
          }
          limits = {
            cpu    = "1"
            memory = "1Gi"
          }
        }
      }
    })
  ]
}
```

## nodeclass & nodepool

참고: nodeclass와 nodepool은 helm_release.karpenter를 먼저 적용한 이후에 진행했다. ( 같이 적용할 경우, CRD 의존성 오류 발생 )

${path.module} : 현재 .tf 파일의 경로를 나타낸다.

node_ami 버전은 @latest를 사용하지 말라고 권장한다. node_ami_alias에 적용할 버전은 

[https://github.com/awslabs/amazon-eks-ami/releases](https://github.com/awslabs/amazon-eks-ami/releases){:target="_blank"}에서 확인할 수 있다.

자세한 내용은 공식문서 [Managing AMIs - Karpenter](https://karpenter.sh/docs/tasks/managing-amis/#controlling-ami-replacement){:target="_blank"}를 참고하면 된다.

`terraform 코드 일부`

NodePool 별로 태그를 적용하기 위해 NodeClass와 NodePool은 1:1로 생성된다. ( 추후 모니터링 및 비용추적 가능 )

```python

provider "kubernetes" {
  host                   = module.yahwang_eks_cluster.cluster_endpoint
  cluster_ca_certificate = base64decode(module.yahwang_eks_cluster.cluster_certificate_authority_data)

  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", module.yahwang_eks_cluster.cluster_name]
  }
}

#---------------
# 사용자 NodeClass, NodePool 정의
#---------------

locals {
  nodepools = {
    dataops = {
      node_ami_alias      = "al2023@v20250505"
      node_ami_family     = "AL2023"
      nodepool_name       = "dataops-nodepool"
      nodeclass_name      = "dataops-nodeclass"
      nodepool_taint_role = "dataops"
      volume_size         = "20Gi"
      tags = {
        Name = "dataops-nodepool"
        role = "dataops"
      }
    }

    ...
    
  }
}

resource "kubernetes_manifest" "karpenter_nodeclass" {
  for_each = local.nodepools

  manifest = yamldecode(
    templatefile("${path.module}/yamls/karpenter-nodeclass.yaml", {
      node_iam_role_name = module.eks_node_default_role.iam_role_name
      node_ami_family    = each.value.node_ami_family
      node_ami_alias     = each.value.node_ami_alias
      cluster_name       = module.prd_eks_cluster.cluster_name
      nodeclass_name     = each.value.nodeclass_name
      nodepool_name      = each.value.nodepool_name
      volume_size        = each.value.volume_size
      tags               = each.value.tags
    })
  )
}

resource "kubernetes_manifest" "karpenter_nodepool" {
  for_each = local.nodepools

  manifest = yamldecode(
    templatefile("${path.module}/yamls/karpenter-nodepool.yaml", {
      nodepool_name       = each.value.nodepool_name
      nodepool_taint_role = each.value.nodepool_taint_role
      nodeclass_name      = each.value.nodeclass_name
    })
  )

  depends_on = [
    kubernetes_manifest.karpenter_nodeclass
  ]
}
```

그 외 추가 설정은 공식 문서 [NodeClasses](https://karpenter.sh/docs/concepts/nodeclasses/){:target="_blank"}를 참고하면 된다.

### NodeClass yaml 설정

서브넷, IAM role, AMI 등 노드 기본 설정을 정의한다.

여기서 이전에 설정한 node_security_group_tags과 subnet에 설정한 태그를 사용한다.

참고 : 볼륨 최소 크기는 20Gi로 보여진다. ( 낮을 경우, 오류 확인 )

`karpenter-nodeclass.yaml`

```python
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata:
  name: "${nodeclass_name}"
spec:
  role: "${node_iam_role_name}"
  amiFamily: "${node_ami_family}"
  amiSelectorTerms:
    - alias: "${node_ami_alias}"
  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: "${cluster_name}"
  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: "${cluster_name}"
  blockDeviceMappings:
    - deviceName: /dev/xvda
      ebs:
        volumeSize: "${volume_size}"
        volumeType: gp3
        deleteOnTermination: true
  tags:
%{ for key, value in tags ~}
    ${key}: "${value}"
%{ endfor ~}
```

### NodePool yaml 설정

`karpenter-nodepool.yaml`

노드 타입 조정, 삭제 등 노드 관리 방법을 정의한다.

**nodeClassRef** : NodeClass를 참조하여 노드를 생성한다.

**disruption** : 노드 풀이 비어있거나 사용되지 않을 때 노드를 제거하는 설정이다.

이 nodepool은 배치 작업을 위한 설정이기 때문에 taint를 설정하였다. ( k8s 배포 시 toleration을 설정 )

labels의 role을 활용하여 dataops라는 node에만 배치 작업을 할 수 있도록 설정하였다. ( 지정한 노드만 배치 작업을 할 수 있도록 설정 )

```python
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: "${nodepool_name}"
spec:
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 2m
  template:
    metadata:
      labels:
        role: dataops
    spec:
      taints:
        - key: dedicated
          operator: Equal
          value: "${nodepool_taint_role}"
          effect: NoSchedule
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: "${nodeclass_name}"
      requirements:
        - key: kubernetes.io/os
          operator: In
          values: 
            - "linux"
        - key: kubernetes.io/arch
          operator: In
          values: 
            - "arm64"
        - key: karpenter.sh/capacity-type
          operator: In
          values: 
            - "spot"
            - "on-demand"
        - key: node.kubernetes.io/instance-type
          operator: In
          values:
            - "t4g.medium"
            - "t4g.large"
```

그 외 추가 설정은 공식 문서 [NodePools](https://karpenter.sh/docs/concepts/nodepools/){:target="_blank"}를 참고하면 된다.

### SPOT INSTANCE 사용 설정

이 설정이 없으면 spot instance 생성 시 오류가 발생한다.

```python
resource "aws_iam_service_linked_role" "spot" {
  aws_service_name = "spot.amazonaws.com"
}
```

에러 메시지

```sql
{"level":"ERROR","controller":"nodeclaim.lifecycle","controllerKind":"NodeClaim", "name":"dataops-nodepool-42fzv",
 "error":"launching nodeclaim, creating instance, creating nodeclaim, AuthFailure.ServiceLinkedRoleCreationNotPermitted: 
The provided credentials do not have permission to create the service-linked role for EC2 Spot Instances."}  
```

AWS 콘솔에서 생성된 것을 확인할 수 있다. ( 이름은 자동으로 설정된다. )

![karpenter_setting_3]({{site.baseurl}}/assets/img/devops/karpenter_setting_3.png)

## karpenter 동작 확인

`karpenter 테스트로 사용한 yaml`

nodeSelector와 tolerations 모두 적용했다.

```sql
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world-deployment
  labels:
    app: hello-world
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      nodeSelector:
        role: dataops
      tolerations:
      - key: dedicated
        operator: Equal
        value: dataops
        effect: NoSchedule
      containers:
      - name: hello-world-container
        image: busybox
        command: ["/bin/sh", "-c", "echo 'hello world' && sleep 60"]
        resources:
          requests:
            memory: "2Gi"
          limits:
            memory: "2Gi"
```

3개의 파드(Pod)를 배포했지만 2개는 기존 dataops 노드에 배포되고, 부족한 1개는 spot instance로 배포되었다.

실제 노드가 생성되고 동작하는 데 30초 정도 소요되었다.

![karpenter_setting_2]({{site.baseurl}}/assets/img/devops/karpenter_setting_2.png)

`node 생성 시 karpenter 로그`

```sql
{"time":"2025-06-10T18:29:40.847Z","logger":"controller","message":"found provisionable pod(s)","controller":"provisioner",
"Pods":"default/hello-world-deployment-76696597fc-5tgjr","duration":"24.83765ms"}

{"time":"2025-06-10T18:29:40.847Z","logger":"controller","message":"computed new nodeclaim(s) to fit pod(s)",
"controller":"provisioner","nodeclaims":1,"pods":1}

{"time":"2025-06-10T18:29:40.859Z","logger":"controller","message":"created nodeclaim","controller":"provisioner",
"NodePool":{"name":"dataops-nodepool"},"NodeClaim":{"name":"dataops-nodepool-4tww7"},"instance-types":"t4g.medium"}

{"time":"2025-06-10T18:29:43.064Z","logger":"controller","message":"launched nodeclaim","controller":"nodeclaim.lifecycle",
"controllerKind":"NodeClaim","NodeClaim":{"name":"dataops-nodepool-4tww7"},"instance-type":"t4g.medium","capacity-type":"spot"}

{"time":"2025-06-10T18:30:01.143Z","logger":"controller","message":"registered nodeclaim","controller":"nodeclaim.lifecycle",
"controllerKind":"NodeClaim","NodeClaim":{"name":"dataops-nodepool-4tww7"},"Node":{"name":"ip-172-16-...ap-northeast-2.compute.internal"}}

{"time":"2025-06-10T18:30:19.590Z","logger":"controller","message":"initialized nodeclaim","controller":"nodeclaim.lifecycle",
"controllerKind":"NodeClaim","NodeClaim":{"name":"dataops-nodepool-4tww7"},"Node":{"name":"ip-172-16-...ap-northeast-2.compute.internal"}}
```

`node 삭제 시 karpenter 로그`

```sql
{"time":"2025-06-10T18:42:49.595Z","logger":"controller","message":"disrupting node(s)","controller":"disruption","reason":"empty",
"decision":"delete","disrupted-node-count":1,"replacement-node-count":0,"pod-count":0,
"disrupted-nodes":[{"NodeClaim":{"name":"dataops-nodepool-4tww7"},"capacity-type":"spot","instance-type":"t4g.medium"}]}    

{"time":"2025-06-10T18:42:50.522Z","logger":"controller","message":"tainted node","controller":"node.termination",
"NodeClaim":{"name":"dataops-nodepool-4tww7"}, "taint.Key":"karpenter.sh/disrupted","taint.Value":"","taint.Effect":"NoSchedule"}

{"time":"2025-06-10T18:43:32.830Z","logger":"controller","message":"deleted node","controller":"node.termination",
"NodeClaim":{"name":"dataops-nodepool-4tww7"}}

{"time":"2025-06-10T18:43:33.058Z","logger":"controller","message":"deleted nodeclaim","controller":"nodeclaim.lifecycle",
"NodeClaim":{"name":"dataops-nodepool-4tww7"}}
```

실제 배치 작업에 대해서는 spark를 사용하여 추후 다룰 예정이다.

`References` : 

* [terraform-module - karpenter](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest/submodules/karpenter){:target="_blank"}

* [karpenter-provider-aws CRD](https://github.com/aws/karpenter-provider-aws/tree/v1.4.0/charts/karpenter-crd/templates){:target="_blank"}