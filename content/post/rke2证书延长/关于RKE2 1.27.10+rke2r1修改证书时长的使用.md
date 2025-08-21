---
date: '2025-08-20T13:57:10+08:00'
title: '关于RKE2 1.27.10+rke2r1修改证书时长的使用'
---

## 关于RKE2 1.27.10+rke2r1修改证书时长的使用

### 基于RKE2 v1.27.10+rke2r1进行代码修改并重新编译项目修改了以下的功能
- 可以通过修改`/etc/default/rke2-server` 相关配置修改证书自定义时长 **客户端|CA证书**
- 修复在rke2 v1.27.10中的使用 `rke2 certificate rotate` 出现的部分客户端证书没有更新的问题
### 具体使用方式
1. 在已有的搭建了rke2 v1.27.10+rke2r1中的集群中 **先关闭集群** 然后将对应架构的二进制文件**替换**原有的二进制文件 同时重新加载服务
2. 启动替换了二进制文件之后rke2集群 并且要**等侯原有集群节点进入Ready状态**（不然会出现一台机器上有多个相同ip的rke2节点）
3. 定义`/etc/default/rke2-server`配置文件，内容介绍如下```
```properties files
CATTLE_NEW_SIGNED_CA_EXPIRATION_YEARS=100 # 自定义客户端证书时长（单位年）
CATTLE_NEW_SIGNED_CERT_EXPIRATION_DAYS=36500 # 自定义CA证书时长 （单位天）
```
4. 使用命令`rke2 certificate rotate`手动更新客户端证书
5. 使用命令`for i in `ls /var/lib/rancher/rke2/server/tls/*.crt`; do echo $i; openssl x509 -enddate -noout -in $i; done` 观察发现证书有效期已经修改至配置的时长
6. 确认集群正常运行
### 目前已知的问题
- 当CA证书到期时应该怎么处理，并且暂时不能在不影响集群的情况下替换CA证书
- 是否在生产环境中自行编译的二进制会有其他不确定的bug，例如镜像问题，部署项目的问题
- 其他未知问题
### 代码仓库
- [FXAZfung/k3s: Lightweight Kubernetes](https://github.com/FXAZfung/k3s)
- [FXAZfung/my-dynamiclistener](https://github.com/FXAZfung/my-dynamiclistener)
- [FXAZfung/my-rke2](https://github.com/FXAZfung/my-rke2)
### 二进制下载地址
- [Releases · FXAZfung/my-rke2](https://github.com/FXAZfung/my-rke2/releases)