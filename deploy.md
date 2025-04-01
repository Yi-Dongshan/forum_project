# Django + Gunicorn + Nginx + SQLite 部署指南

适用于 Ubuntu 服务器，Django 项目根目录为 `/forum_project`，数据库使用 SQLite。

---

## ✅ 0. 使用 SSH 和 SCP 连接远程主机

### 🖥️ 使用 SSH 私钥连接远程服务器

```bash
# 快捷连接（需要配置 SSH config）
ssh dkserver

# 或使用 PEM 私钥连接
ssh -i ~/.ssh/DKServer.pem root@8.217.248.64
```

---

### 📤 使用 SCP 上传项目到远程主机

```bash
scp -i ~/.ssh/DKServer.pem -r "D:\My Workspace\forum_project" root@8.217.248.64:/
```

---

### 📥 使用 SCP 从远程主机拉取项目到本地

```bash
scp -i ~/.ssh/DKServer.pem -r root@8.217.248.64:/forum_project/ "D:\My Workspace\"
```

---

## ✅ 1. 项目准备

```bash
cd /forum_project

# 创建虚拟环境并激活
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

---

## ✅ 2. 修改 Django 配置

编辑 `settings.py`：

```python
DEBUG = False
ALLOWED_HOSTS = ['ydk7.xyz', 'www.ydk7.xyz']

STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## ✅ 3. 迁移数据库 & 收集静态文件

```bash
python manage.py migrate
python manage.py collectstatic
```

---

## ✅ 4. 设置文件权限（重点）

```bash
# 数据库文件权限
sudo chown www-data:www-data /forum_project/db.sqlite3
sudo chmod 664 /forum_project/db.sqlite3

# 项目目录权限
sudo chown -R www-data:www-data /forum_project
sudo chmod -R 755 /forum_project
```

---

## ✅ 5. 创建 Gunicorn 服务

创建文件 `/etc/systemd/system/gunicorn.service`：

```bash
sudo nano /etc/systemd/system/gunicorn.service
```


```ini
[Unit]
Description=Gunicorn instance to serve forum_project
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/forum_project
ExecStart=/forum_project/venv/bin/gunicorn --workers 3 --bind unix:/forum_project/forum_project.sock forum_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

启用并启动 Gunicorn：

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

---

## ✅ 6. 配置 Nginx

创建文件 `/etc/nginx/sites-available/forum_project`：

```bash
sudo nano /etc/nginx/sites-available/forum_project
```

文件内容

```nginx
server {
    listen 80;
    server_name ydk7.xyz www.ydk7.xyz;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /forum_project/staticfiles/;
    }

    location /media/ {
        alias /forum_project/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/forum_project/forum_project.sock;
    }
}
```

启用配置并重启 Nginx：

```bash
sudo ln -s /etc/nginx/sites-available/forum_project /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## ✅ 7. 配置 HTTPS（可选）

使用 Certbot 自动申请 SSL：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d ydk7.xyz -d www.ydk7.xyz
```

---

## ✅ 8. 常见问题排查

### 🔒 数据库错误：readonly database

修复：

```bash
sudo chown www-data:www-data /forum_project/db.sqlite3
sudo chmod 664 /forum_project/db.sqlite3
```

### 🧱 Gunicorn 启动失败

查看日志：

```bash
sudo journalctl -u gunicorn -n 50
```

### 🧩 Nginx 报错

查看：

```bash
sudo tail -n 100 /var/log/nginx/error.log
```

---

## ✅ 9. 检查运行状态

```bash
# 查看 Gunicorn 是否运行
ps aux | grep gunicorn

# 查看监听的 socket 文件
ls -l /forum_project/forum_project.sock

# 访问网站测试
curl http://localhost
```

---

## 🎉 部署完成！

浏览器访问：

```
https://ydk7.xyz/
```

如果你需要支持 PostgreSQL、Docker、CI/CD 等部署方式，可以在此基础上扩展。

👋 再见啦，工程师朋友！愿你代码如诗，生活如歌，愿你未来的项目部署都顺利无比，代码永远优雅，Bug 见你就跑 💻🚀
