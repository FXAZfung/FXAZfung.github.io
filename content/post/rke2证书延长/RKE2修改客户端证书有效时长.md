
---
title: 'RKE2修改客户端证书有效时长'
---

通过查阅 [https://github.com/rancher/rke2/pull/4324](https://github.com/rancher/rke2/pull/4324) 可知，RKE2 官方已支持通过配置服务器端环境变量来自定义客户端证书的有效期。具体方法如下：

在 `/etc/default/rke2-server` 文件中添加以下参数：

```bash
CATTLE_NEW_SIGNED_CERT_EXPIRATION_DAYS=36500
```

该参数设置客户端证书的有效期为 36500 天（约 100 年）。

---

**测试环境：**

- 操作系统：Ubuntu 22.04 x86_64
    
- RKE2 版本：v1.32.6+rke2r1
    
- 配置：2 核 4G
    

---

**测试步骤与结果：**

1. 修改 `/etc/default/rke2-server` 文件后安装 RKE2，或在安装完成后修改该文件并执行证书轮换命令：
    
    ```bash
    systemctl stop rke2-server
    rke2 certificate rotate
    systemctl start rke2-server
    ```
    
2. 执行证书检查命令确认证书生效时间：
    
    ```bash
    rke2 certificate check --output table
    ```
    
    
    
3. 修改系统时间为 `2034-01-01 10:00:00`，执行：
    
    ```bash
    date -s "2034-01-01 10:00:00"
    kubectl get nodes
    ```
    
    结果：集群运行正常，证书有效。
    
    
    
4. 再次修改系统时间为 `2124-01-01 10:00:00`，执行相同命令后发现集群报错，提示证书已过期。
    
    
    

---

**初步结论：**

- 通过配置 `CATTLE_NEW_SIGNED_CERT_EXPIRATION_DAYS` 参数，可以成功延长客户端证书的有效期；
    
- 该参数仅控制由 CA 签发的新证书的过期时间，**CA 根证书的有效期并未改变**；
    
- 当系统时间超过 CA 根证书的有效期时，依旧会出现证书过期问题，导致集群不可用。
    

---

**注意事项：**

- 最好在安装 RKE2 前配置该参数，以确保所有证书在初始化时即使用自定义的有效期；
    
- 若在安装后配置该参数，需通过 `rke2 certificate rotate` 命令手动触发证书轮换；
    
- **若希望整个集群长期运行，仍需考虑如何延长或轮换 CA 根证书的有效期**，否则即便客户端证书有效期延长，也会因 CA 证书失效而失效。
    