
---
title: 'RKE2修改CA证书有效时长'
---

## ✅ RKE2 自定义证书有效期的编译与部署流程

### 🧠 背景说明

RKE2 的证书生成逻辑继承自 K3s，而 K3s 又依赖于 [`github.com/rancher/dynamiclistener`](https://github.com/rancher/dynamiclistener) 库来生成 TLS 证书。因此，我们可以通过修改该库来自定义 CA 或客户端证书的有效期。

---

### ✏️ 核心修改点：自定义 CA 证书时长

原始代码（`NewSelfSignedCACert`）使用固定的 `10 年` 有效期：

```go
NotAfter: now.Add(duration365d * 10).UTC()
```

我们将其替换为支持读取环境变量 `CATTLE_NEW_SIGNED_CA_EXPIRATION_YEARS` 的方式，例如：

```go
expiresAt := duration365d * 10
envExpirationYears := os.Getenv("CATTLE_NEW_SIGNED_CA_EXPIRATION_YEARS")
if envExpirationYears != "" {
    if envExpirationYearsInt, err := strconv.Atoi(envExpirationYears); err == nil {
        expiresAt = time.Hour * 24 * 365 * time.Duration(envExpirationYearsInt)
    }
}
NotAfter: now.Add(expiresAt).UTC()
```

这样可通过系统环境变量控制生成证书的有效期。

---

### 📦 编译后部署流程

#### 1. 解压构建产物并安装至系统目录

编译完成后，将产物解压并移动到 `/usr/local`：

```bash
tar -zxvf /root/rke2/dist/artifacts/rke2.linux-amd64.tar.gz -C /usr/local
```

---

#### 2. 导入构建生成的运行时镜像

将运行时镜像移动至 RKE2 默认目录，并使用 `containerd` 的 `ctr` 工具导入与打标签：

```bash
cp /root/rke2/build/images/rke2-runtime.tar /var/lib/rancher/rke2/agent/images/
ctr -n k8s.io images import /var/lib/rancher/rke2/agent/images/rke2-runtime.tar

# 示例：设置镜像 tag（如有需要）
ctr -n k8s.io images tag <原始镜像名> <目标标签>
```

---

#### 3. 设置环境变量配置证书有效期

通过 systemd 支持的方式，将环境变量写入 `/etc/default/rke2-server`（或 `/etc/sysconfig/rke2-server`）：

```ini
CATTLE_NEW_SIGNED_CA_EXPIRATION_YEARS=100
CATTLE_NEW_SIGNED_CERT_EXPIRATION_DAYS=36500
```

确保文件被正确加载（已在 systemd unit 文件中定义）：

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
```

---

#### 4. 启动 RKE2 Server

```bash
systemctl start rke2-server
```

---

#### 5. 设置客户端使用环境变量

```bash
export KUBECONFIG=/etc/rancher/rke2/rke2.yaml
export PATH=/var/lib/rancher/rke2/bin:$PATH
```

---

#### 6. 检查证书有效期

使用 RKE2 提供的内置命令检查当前所有证书的有效时长：

```bash
rke2 certificate check --output table
```




---

#### 7.设置系统时间进行过期测试

⚠️ 测试环境中可使用如下命令模拟证书过期行为：

```bash
timedatectl set-time "2124-01-01 00:00:00"
```

---

### ✅ 总结

通过替换 `dynamiclistener` 并自定义 CA 证书逻辑，你可以在 RKE2 中灵活设置证书时长，无需依赖默认的 10 年限制。配合 systemd 环境变量和镜像导入操作，即可在测试或定制环境中完全控制证书生命周期与集群初始化行为。