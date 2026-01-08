# Railway 部署指南 - TikTokDownloader API

## 🚀 快速部署步骤

### 方法 1: 从 GitHub 部署（推荐）

#### 第 1 步：准备 GitHub 仓库

1. **Fork 原项目**
   - 访问 https://github.com/JoeanAmier/TikTokDownloader
   - 点击右上角 "Fork" 按钮
   - Fork 到你的 GitHub 账号

2. **或者上传本地修改后的代码**
   ```bash
   cd /Users/kk/project/newsnexttime/hot-search-hub/TikTokDownloader

   # 初始化 Git（如果还没有）
   git init
   git add .
   git commit -m "Add Railway deployment config"

   # 添加你的 GitHub 仓库
   git remote add origin https://github.com/你的用户名/TikTokDownloader.git
   git branch -M main
   git push -u origin main
   ```

#### 第 2 步：在 Railway 上部署

1. **登录 Railway**
   - 访问 https://railway.app/
   - 点击 "Login" 使用 GitHub 登录

2. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的 TikTokDownloader 仓库
   - 点击 "Deploy Now"

3. **等待构建完成**
   - Railway 会自动检测 Dockerfile
   - 开始构建镜像（大约 3-5 分钟）
   - 构建日志会实时显示

4. **配置公开访问**
   - 部署完成后，点击项目
   - 进入 "Settings" 标签
   - 找到 "Networking" 部分
   - 点击 "Generate Domain"
   - 记录生成的域名（例如：`your-app.up.railway.app`）

5. **完成！**
   - 访问 `https://your-app.up.railway.app/docs` 查看 API 文档
   - 开始使用 API！

---

### 方法 2: 从本地目录部署

#### 使用 Railway CLI

1. **安装 Railway CLI**
   ```bash
   # macOS
   brew install railway

   # 或使用 npm
   npm install -g @railway/cli
   ```

2. **登录 Railway**
   ```bash
   railway login
   ```

3. **初始化项目**
   ```bash
   cd /Users/kk/project/newsnexttime/hot-search-hub/TikTokDownloader
   railway init
   ```

4. **部署**
   ```bash
   railway up
   ```

5. **生成公开域名**
   ```bash
   railway domain
   ```

---

## 🔧 环境变量配置（可选）

如果需要配置 Cookie（用于获取更高质量视频），可以在 Railway 添加环境变量：

1. 进入 Railway 项目面板
2. 点击 "Variables" 标签
3. 点击 "New Variable"
4. 添加以下变量：

```bash
# 抖音 Cookie（可选）
DOUYIN_COOKIE=你的抖音Cookie值

# TikTok Cookie（可选）
TIKTOK_COOKIE=你的TikTok Cookie值
```

**注意：** 基础功能无需 Cookie！

---

## 📊 部署后验证

### 1. 测试健康检查

```bash
curl https://your-app.up.railway.app/
# 应该重定向到 GitHub 仓库
```

### 2. 测试 API 文档

访问：`https://your-app.up.railway.app/docs`

应该看到 Swagger API 文档界面。

### 3. 测试视频解析

```bash
# 解析抖音短链接
curl -X POST https://your-app.up.railway.app/douyin/share \
  -H "Content-Type: application/json" \
  -d '{"text": "https://v.douyin.com/XquymvImzvk/"}'

# 应该返回完整链接
```

### 4. 测试获取视频数据

```bash
curl -X POST https://your-app.up.railway.app/douyin/detail \
  -H "Content-Type: application/json" \
  -d '{"detail_id": "7584615647637769529"}'

# 应该返回视频信息和下载链接
```

---

## 📱 快捷指令配置

部署完成后，在 iOS 快捷指令中使用：

```
API 地址：https://your-app.up.railway.app
```

将所有 `http://127.0.0.1:5555` 替换为你的 Railway 域名。

---

## 💰 费用说明

### Railway 免费额度

- **$5 免费额度/月**
- **500 小时执行时间/月**
- **100GB 出站流量/月**

### 预估使用量（轻度）

假设每天 100 次 API 调用：
- 执行时间：~10 小时/月
- 流量：~5GB/月
- **费用：$0-1/月**（在免费额度内）

### 预估使用量（中度）

假设每天 1000 次 API 调用：
- 执行时间：~100 小时/月
- 流量：~50GB/月
- **费用：$2-5/月**

---

## 🛠️ 故障排除

### 问题 1: 构建失败

**检查日志：**
- 在 Railway 项目面板查看 "Deployments"
- 点击失败的部署查看详细日志

**常见原因：**
- Dockerfile 路径错误
- 依赖安装失败
- start_api.py 文件缺失

**解决方案：**
```bash
# 确保文件都在正确位置
ls -la TikTokDownloader/
# 应该看到 Dockerfile, start_api.py, railway.toml
```

### 问题 2: 服务无法访问

**检查端口：**
- Railway 会自动处理端口映射
- 确保应用监听 `0.0.0.0:5555`

**检查日志：**
```bash
railway logs
```

### 问题 3: API 返回错误

**检查是否需要 Cookie：**
- 基础功能不需要 Cookie
- 如果特定视频需要，添加 DOUYIN_COOKIE 环境变量

---

## 🔄 更新部署

### 方法 1: 通过 GitHub 自动部署

1. 修改本地代码
2. 提交并推送到 GitHub
   ```bash
   git add .
   git commit -m "Update config"
   git push
   ```
3. Railway 会自动检测并重新部署

### 方法 2: 使用 Railway CLI

```bash
cd TikTokDownloader
railway up
```

---

## 📚 相关资源

- **Railway 文档**: https://docs.railway.app/
- **TikTokDownloader GitHub**: https://github.com/JoeanAmier/TikTokDownloader
- **API 文档**: https://your-app.up.railway.app/docs
- **快捷指令集成指南**: 见 QUICKSTART.md

---

## ✅ 部署检查清单

- [ ] 已创建 Railway 账号
- [ ] 已 Fork 或上传代码到 GitHub
- [ ] 已在 Railway 创建项目
- [ ] 构建成功完成
- [ ] 已生成公开域名
- [ ] API 文档可访问（/docs）
- [ ] 测试 API 调用成功
- [ ] 已配置快捷指令（如需要）

---

**祝你部署顺利！** 🎉

如有问题，请查看 Railway 项目日志或提 Issue。
