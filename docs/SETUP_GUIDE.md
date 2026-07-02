# 百度网盘API设置指南

## 1. 注册百度网盘开放平台账号

1. 访问 [百度网盘开放平台](https://pan.baidu.com/union/doc/0ksg0sbig)
2. 使用百度账号登录
3. 完成开发者认证

## 2. 创建应用

1. 进入"应用管理"
2. 点击"创建应用"
3. 填写应用信息：
   - 应用名称：如"BaiduDownloader"
   - 应用类型：选择"移动应用"或"Web应用"
   - 应用描述：简要说明应用用途

## 3. 获取API凭证

创建应用后，你会获得：
- `APP_ID`: 应用ID
- `APP_KEY`: API Key
- `SECRET_KEY`: 密钥

## 4. 获取Access Token

### 方式一：OAuth认证（推荐）

1. 构造授权URL：
```
https://openapi.baidu.com/oauth/authorize?
response_type=code&
client_id=YOUR_APP_ID&
redirect_uri=YOUR_REDIRECT_URI
```

2. 用户授权后获取授权码
3. 使用授权码换取Access Token：
```bash
curl -X POST "https://openapi.baidu.com/oauth/token" \
  -d "grant_type=authorization_code" \
  -d "code=AUTHORIZATION_CODE" \
  -d "client_id=YOUR_APP_ID" \
  -d "client_secret=YOUR_SECRET_KEY" \
  -d "redirect_uri=YOUR_REDIRECT_URI"
```

### 方式二：使用API Key

某些情况下可以直接使用API Key，具体参考百度官方文档。

## 5. 配置工具

将获取的凭证填入 `.env` 文件：

```bash
BAIDU_APP_ID=your_actual_app_id
BAIDU_APP_KEY=your_actual_app_key
BAIDU_SECRET_KEY=your_actual_secret_key
BAIDU_ACCESS_TOKEN=your_actual_access_token
```

## 6. 测试配置

运行工具测试配置是否正确：

```bash
dupan-download https://pan.baidu.com/s/test 0000 --verbose
```

## 常见问题

### Q: Access Token过期怎么办？
A: Access Token通常有有效期（如30天），过期后需要重新获取。

### Q: 如何提高API调用限额？
A: 联系百度网盘开放平台申请更高的API调用限额。

### Q: OAuth认证太复杂，有简化方案吗？
A: 可以使用百度官方提供的SDK简化认证流程。
