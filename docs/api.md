# API 文档

## 接口说明

### 帖子相关接口

#### 1. 获取帖子列表
- **URL**: `/api/posts/`
- **方法**: GET
- **参数**:
  - `category`: 分类ID（可选）
  - `search`: 搜索关键词（可选）
  - `sort`: 排序方式（latest/popular）
  - `page`: 页码

#### 2. 获取帖子详情
- **URL**: `/api/posts/<post_id>/`
- **方法**: GET

#### 3. 创建帖子
- **URL**: `/api/posts/create/`
- **方法**: POST
- **权限**: 需要登录

#### 4. 点赞帖子
- **URL**: `/api/posts/<post_id>/like/`
- **方法**: POST
- **权限**: 需要登录

### 评论相关接口

#### 1. 发表评论
- **URL**: `/api/comments/create/`
- **方法**: POST
- **权限**: 需要登录

#### 2. 回复评论
- **URL**: `/api/comments/<comment_id>/reply/`
- **方法**: POST
- **权限**: 需要登录

### 用户相关接口

#### 1. 用户注册
- **URL**: `/api/auth/register/`
- **方法**: POST

#### 2. 用户登录
- **URL**: `/api/auth/login/`
- **方法**: POST

## 请求/响应示例

### 获取帖子列表

请求：
```http
GET /api/posts/?category=1&sort=popular&page=1
```

响应：
```json
{
    "count": 100,
    "next": "http://example.com/api/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "帖子标题",
            "content": "帖子内容",
            "author": {
                "id": 1,
                "username": "作者名"
            },
            "created_at": "2024-03-28T10:00:00Z",
            "likes_count": 10,
            "comments_count": 5
        }
    ]
}
```

### 创建帖子

请求：
```http
POST /api/posts/create/
Content-Type: application/json

{
    "title": "新帖子标题",
    "content": "帖子内容",
    "category": 1
}
```

响应：
```json
{
    "id": 2,
    "title": "新帖子标题",
    "content": "帖子内容",
    "author": {
        "id": 1,
        "username": "当前用户"
    },
    "created_at": "2024-03-28T11:00:00Z"
}
```

## 错误码说明

### HTTP 状态码

- 200: 请求成功
- 201: 创建成功
- 400: 请求参数错误
- 401: 未登录
- 403: 权限不足
- 404: 资源不存在
- 500: 服务器错误

### 业务错误码

- 1001: 用户名已存在
- 1002: 密码格式错误
- 1003: 验证码错误
- 2001: 帖子不存在
- 2002: 分类不存在
- 2003: 无权操作该帖子
- 3001: 评论内容不能为空
- 3002: 评论已被删除
- 4001: 点赞操作失败
- 4002: 重复点赞

### 错误响应格式

```json
{
    "code": 1001,
    "message": "用户名已存在",
    "detail": "该用户名已被注册，请更换其他用户名"
}
```