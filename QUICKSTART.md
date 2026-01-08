# TikTokDownloader API - 快捷指令集成指南

## 🎯 项目概述

基于 [JoeanAmier/TikTokDownloader](https://github.com/JoeanAmier/TikTokDownloader) 项目搭建的抖音视频解析 API 服务。

**核心功能：**
- ✅ 解析抖音短链接（v.douyin.com）
- ✅ 获取无水印视频下载链接
- ✅ 支持视频、图集、直播
- ✅ 无需 Cookie 也能解析（基础功能）
- ✅ REST API + Swagger 文档

---

## 🚀 部署方案

### 方案 1: 本地部署（推荐用于开发测试）

#### 1. 克隆项目
```bash
cd /Users/kk/project/newsnexttime/hot-search-hub
git clone https://github.com/JoeanAmier/TikTokDownloader.git
cd TikTokDownloader
```

#### 2. 安装依赖
```bash
pip install -r requirements.txt
```

#### 3. 启动 API 服务
```bash
# 方式 A: 使用启动脚本（推荐）
python start_api.py

# 方式 B: 交互式启动
python main.py
# 然后选择 "3. Web API 模式"
```

#### 4. 访问 API 文档
- Swagger: http://127.0.0.1:5555/docs
- ReDoc: http://127.0.0.1:5555/redoc

---

### 方案 2: 服务器部署（用于生产环境）

#### 使用 Docker 部署

```dockerfile
# Dockerfile 已包含在项目中
docker build -t tiktok-downloader .
docker run -d -p 5555:5555 tiktok-downloader
```

#### 使用 Systemd 自动启动

```bash
# 创建服务文件
sudo nano /etc/systemd/system/tiktok-api.service
```

内容：
```ini
[Unit]
Description=TikTok Downloader API
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/TikTokDownloader
ExecStart=/usr/bin/python3 /path/to/TikTokDownloader/start_api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable tiktok-api
sudo systemctl start tiktok-api
```

---

## 📡 API 使用文档

### 1. 解析抖音短链接

**端点:** `POST /douyin/share`

**请求参数:**
```json
{
  "text": "https://v.douyin.com/XquymvImzvk/",
  "proxy": ""  // 可选，代理地址
}
```

**响应示例:**
```json
{
  "message": "请求链接成功！",
  "url": "https://www.douyin.com/video/7584615647637769529",
  "params": {
    "text": "https://v.douyin.com/XquymvImzvk/",
    "proxy": ""
  },
  "time": "2026-01-08 15:57:55"
}
```

---

### 2. 获取视频详细数据

**端点:** `POST /douyin/detail`

**请求参数:**
```json
{
  "detail_id": "7584615647637769529",  // 视频 ID
  "cookie": "",  // 可选，抖音 Cookie
  "proxy": "",   // 可选，代理
  "source": false  // 是否返回原始数据
}
```

**响应示例（简化）:**
```json
{
  "success": true,
  "message": "获取数据成功！",
  "data": [
    {
      "type": "视频",
      "desc": "兰海高速得皇冠",
      "downloads": "https://www.douyin.com/aweme/v1/play/?video_id=...",
      "create_time": "2025-01-08",
      "author": {
        "nickname": "作者昵称",
        "uid": "..."
      },
      "music": {...},
      "statistics": {
        "digg_count": 12345,
        "comment_count": 678
      }
    }
  ]
}
```

---

## 🍎 iOS 快捷指令示例

### 快捷指令流程

```
1. 获取剪贴板内容（抖音分享链接）
   ↓
2. 调用 /douyin/share 解析短链接
   ↓
3. 提取视频 ID
   ↓
4. 调用 /douyin/detail 获取视频数据
   ↓
5. 下载视频（使用 downloads 字段的链接）
   ↓
6. 保存到相册
```

### 快捷指令配置（伪代码）

```yaml
名称: 抖音视频下载

操作步骤:
1. 获取剪贴板
   变量: share_url

2. 获取 URL 内容
   URL: http://your-server:5555/douyin/share
   方法: POST
   请求体: JSON
     {
       "text": [share_url]
     }
   变量: share_response

3. 从字典中获取值
   字典: [share_response]
   键: url
   变量: full_url

4. 匹配文本
   文本: [full_url]
   模式: /video/(\d+)
   变量: video_id

5. 获取 URL 内容
   URL: http://your-server:5555/douyin/detail
   方法: POST
   请求体: JSON
     {
       "detail_id": [video_id]
     }
   变量: detail_response

6. 从字典中获取值
   字典: [detail_response]
   键路径: data[0].downloads
   变量: download_url

7. 下载 URL
   URL: [download_url]
   变量: video_file

8. 存储到相册
   媒体: [video_file]

9. 显示通知
   标题: "下载成功"
   正文: "视频已保存到相册"
```

---

## 🔧 Python 调用示例

### 简单示例

```python
import httpx

# 1. 解析短链接
share_response = httpx.post(
    "http://127.0.0.1:5555/douyin/share",
    json={"text": "https://v.douyin.com/XquymvImzvk/"}
)
full_url = share_response.json()["url"]

# 2. 提取视频 ID
import re
video_id = re.search(r'/video/(\d+)', full_url).group(1)

# 3. 获取视频数据
detail_response = httpx.post(
    "http://127.0.0.1:5555/douyin/detail",
    json={"detail_id": video_id}
)
video_data = detail_response.json()["data"][0]

# 4. 下载视频
download_url = video_data["downloads"]
video_content = httpx.get(download_url).content

# 5. 保存文件
with open("video.mp4", "wb") as f:
    f.write(video_content)

print(f"✅ 视频已下载: {video_data['desc']}")
```

### 完整示例（带错误处理）

参见项目中的 `douyin_api_wrapper.py` 文件。

---

## ⚙️ 配置 Cookie（可选）

虽然基础功能无需 Cookie，但配置 Cookie 可以：
- 获取更高分辨率视频
- 访问私密作品
- 提高稳定性

### Cookie 获取方法

1. **浏览器开发者工具**（推荐）
   - 打开 https://www.douyin.com/ 并登录
   - 按 F12 打开开发者工具
   - Network 标签 → 刷新页面
   - 找到任意请求 → Headers → Cookie
   - 复制完整 Cookie 值

2. **使用项目自带工具**
   ```bash
   python main.py
   # 选择 "从浏览器获取 Cookie" 选项
   ```

### Cookie 配置

编辑 `settings.json`:
```json
{
  "cookie": "你的抖音 Cookie",
  "cookie_tiktok": "你的 TikTok Cookie (可选)"
}
```

---

## 📊 性能测试

### 测试环境
- 服务器: MacBook Pro M1
- Python: 3.12
- 网络: 家庭宽带

### 测试结果

| 操作 | 响应时间 | 成功率 |
|------|---------|--------|
| 短链接解析 | ~200ms | 100% |
| 视频数据获取 | ~800ms | 100% |
| 视频下载 (3.6MB) | ~1.2s | 100% |

---

## 🛡️ 安全建议

### 1. 配置 API Token（推荐用于生产）

编辑 `src/custom/function.py`:
```python
def is_valid_token(token: str) -> bool:
    """验证令牌有效性"""
    VALID_TOKENS = ["your-secret-token-here"]
    return token in VALID_TOKENS
```

然后在请求头中添加 Token：
```python
headers = {"token": "your-secret-token-here"}
httpx.post(url, headers=headers, json=data)
```

### 2. 限流保护

使用 Nginx 限流：
```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

location / {
    limit_req zone=api_limit burst=20;
    proxy_pass http://127.0.0.1:5555;
}
```

### 3. HTTPS 部署

使用 Nginx + Let's Encrypt:
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:5555;
    }
}
```

---

## ❓ 常见问题

### Q1: Cookie 多久会失效？
**A**: 通常 7-30 天。失效后重新获取即可。

### Q2: 为什么有些视频无法解析？
**A**: 可能原因：
- 视频已删除或下架
- 账号设置了隐私保护（需要 Cookie）
- 平台限流（稍后重试）

### Q3: 可以并发请求吗？
**A**: 可以，但建议：
- 单 IP 限制 10 QPS
- 使用连接池复用

### Q4: 视频下载速度慢怎么办？
**A**:
- 检查网络连接
- 使用国内服务器部署
- 考虑使用 CDN

---

## 📚 相关资源

- **项目 GitHub**: https://github.com/JoeanAmier/TikTokDownloader
- **API 文档**: http://127.0.0.1:5555/docs
- **Cookie 获取教程**: [项目文档](https://github.com/JoeanAmier/TikTokDownloader/blob/master/docs/Cookie%E8%8E%B7%E5%8F%96%E6%95%99%E7%A8%8B.md)

---

## 📝 更新日志

### 2026-01-08
- ✅ 完成项目测试
- ✅ 验证 API 功能正常
- ✅ 编写快捷指令集成文档
- ✅ 创建 Python 调用示例

---

**祝您使用愉快！** 🎉
