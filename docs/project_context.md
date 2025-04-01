# 项目上下文说明

## 项目概述
这是一个基于 Django 5.1.3 开发的论坛系统，主要功能包括用户管理、帖子发布、评论互动、实时通知等。项目采用 Bootstrap 4 构建响应式界面，使用 SQLite 作为数据库。

## 技术架构
- 后端框架：Django 5.1.3
- 前端框架：Bootstrap 4
- 数据库：SQLite
- 消息队列：Redis
- WebSocket：Django Channels
- 部署环境：Gunicorn + Nginx

## 核心功能模块

### 1. 用户系统 (accounts)
- 用户注册、登录、个人资料管理
- 头像上传和编辑
- 用户权限控制

### 2. 帖子管理 (posts)
- 帖子的 CRUD 操作
- 富文本编辑器支持
- 点赞功能
- 帖子分类和搜索

### 3. 评论系统
- 评论和回复功能
- 评论通知
- 评论内容格式化

### 4. 通知系统 (notifications)
- 基于 WebSocket 的实时通知
- 点赞、评论、回复等触发通知
- 通知状态管理

### 5. 分类系统 (categories)
- 帖子分类管理
- 分类统计
- 分类导航

## 项目结构
```
forum_project/
├── accounts/            # 用户账户管理
├── categories/          # 分类管理
├── forum_project/       # 核心配置
├── media/              # 媒体文件
├── notifications/      # 通知系统
├── posts/              # 帖子管理
├── static/             # 静态文件
└── templates/          # HTML模板
```

## 部署信息
- 服务器：阿里云 Ubuntu 服务器
- 域名：example.com
- 部署方式：Gunicorn + Nginx
- 数据库：SQLite
- 静态文件：由 Nginx 处理
- WebSocket：由 Daphne 处理

## 开发环境
- Python 3.8+
- Redis 服务
- Node.js（用于前端资源构建）
- 虚拟环境：venv

## 项目进展
- 当前版本：1.0.2
- 最近更新：优化帖子列表默认排序、修复评论换行显示问题
- 计划功能：用户消息系统、帖子草稿功能

## 文档索引
- README.md：项目总览
- deploy.md：部署指南
- api.md：API文档
- CHANGELOG.md：更新日志