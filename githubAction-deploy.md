# CICD部署流程

本项目采用github actions + 阿里云服务器的部署步骤



## 第一步：在 GitHub 仓库中配置秘钥

为了安全，不要在脚本里写明密码。请在 GitHub 仓库页面点击： `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`。

添加以下三个变量：

1. **`REMOTE_HOST`**: 服务器的 IP 地址。
2. **`REMOTE_USER`**: 登录用户名（如 `root`）。
3. **`SERVER_SSH_KEY`**: 你的 SSH 私钥（通常在本地或服务器的 `~/.ssh/id_rsa` 中）。

## 第二步：创建部署脚本

在你的项目根目录下，创建文件[.github/workflows/deploy.yml](./.github/workflows) （注意文件夹层级）



## 第三步：服务器端的准备工作

为了让脚本顺利运行，你的服务器需要完成以下配置：

1. **项目初装**：手动在服务器上 `git clone` 一次你的项目，确保目录结构正确。
2. **免密登录**：确保你把生成的公钥（`.pub`）添加到了服务器的 `~/.ssh/authorized_keys` 中。
3. **服务管理**：建议使用 `systemd`（系统服务）或 `pm2` 来管理 Python/Java 进程，这样脚本里一行 `restart` 命令就能搞定，不会因为 SSH 断开而导致进程关闭。
4. **项目在服务器能运行**：确保有python环境，手动尝试在服务器上运行这个项目，并能正常访问。

## 第四步：写systemd 配置文件

### 4.1 编写内容

在服务器上，以 root 权限创建一个服务文件（以 Python 项目为例，Java 同理）：

```bash
sudo vim /etc/systemd/system/flask-log-test.service
```

填入以下内容（根据你的实际路径修改）：

```Ini, TOML
[Unit]
Description=My Python Project Service
After=network.target

[Service]
# 程序的执行用户，建议不要直接用 root，用你的普通用户名
User=root
# 项目根目录
WorkingDirectory=/app/flask-log-test
# 启动命令：如果是虚拟环境，请指向 venv 里的 python 路径
# 如果是 Java 项目，这里写 ExecStart=/usr/bin/java -jar target/app.jar
ExecStart=/app/flask-log-test/.venv/bin/python -u  app.py

# 自动重启设置：如果程序崩溃，5秒后自动重启
Restart=always
RestartSec=5

# 环境变量（可选）
Environment=PYTHONUNBUFFERED=1
Environment=PORT=5000

[Install]
WantedBy=multi-user.target
```

------

### 4.2 第二步：激活并启动服务

保存文件后，在服务器执行以下命令：

1. **重新加载系统配置**（让系统识别新文件）：

   ```Bash
   sudo systemctl daemon-reload
   ```

2. **启动并设置开机自启**：

   ```Bash
   sudo systemctl enable flask-log-test.service
   sudo systemctl start flask-log-test.service
   ```

3. **查看状态**（确保是绿色的 active）：

   ```Bash
   sudo systemctl status flask-log-test.service
   ```





## 参考资料：

[Gemin 回答](https://gemini.google.com/app/b39799ca7b749a29)

[为什么大佬都在用 Github Actions 做 CICD？](https://www.bilibili.com/video/BV1jNSEBiE6D/?spm_id_from=333.337.search-card.all.click&vd_source=cde31d8f45092d6096e8e5d3b9e22f83)

[Github的王炸功能，但很少人知道怎么用？免费运行程序，流水线编译部署，天气推送 签到薅羊毛 领京豆 CI/CD持续集成持续部署](https://www.bilibili.com/video/BV11e411i7Xx?spm_id_from=333.788.videopod.sections&vd_source=cde31d8f45092d6096e8e5d3b9e22f83)