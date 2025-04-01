# 论坛项目 (Forum Project)

这是一个基于Django开发的现代化论坛系统，提供用户注册、发帖、评论、点赞、通知等功能。

## 项目特点

- 用户账户管理系统
- 帖子发布与管理
- 分类系统
- 实时通知功能（基于WebSocket）
- 响应式设计
- 富文本编辑器支持

## 项目文档

- [部署指南](docs/deploy.md) - 详细的项目部署步骤和配置说明
- [API文档](docs/api.md) - 接口说明、请求/响应示例和错误码说明
- [更新日志](docs/CHANGELOG.md) - 项目版本更新记录
- [项目上下文](docs/project_context.md) - 项目背景和技术架构说明

## 技术栈

- **后端**: Django 5.1.3
- **前端**: Bootstrap 4, JavaScript
- **数据库**: SQLite (开发环境)
- **WebSocket**: Django Channels
- **消息队列**: Redis
- **部署**: Gunicorn

---

## 项目结构

forum_project/

├── accounts/            # 用户账户管理应用

├── categories/          # 分类管理应用

├── forum_project/       # 项目核心配置

├── media/              # 用户上传的媒体文件

├── notifications/      # 通知系统应用

├── posts/              # 帖子管理应用

├── scripts/            # 实用脚本

├── static/             # 静态文件

├── templates/          # HTML模板

├── manage.py           # Django管理脚本

└── requirements.txt    # 项目依赖

---

### 快速开始

1. 克隆仓库

```bash
git clone <repository-url>
cd forum_project
```

2. 创建虚拟环境

```bash
python -m venv venv
venv\Scripts\activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 数据库迁移

```bash
python manage.py migrate
```

5. 运行开发服务器

```bash
python manage.py runserver
```

6. 访问网站

- 前台: http://127.0.0.1:8000/
- 管理后台: http://127.0.0.1:8000/admin/

---

## 生产环境部署

1. 修改 settings.py 配置
2. 收集静态文件
3. 配置 Gunicorn
4. 配置 Nginx
5. 配置 SSL 证书

详细的部署步骤请参考 [deploy.md](deploy.md)
