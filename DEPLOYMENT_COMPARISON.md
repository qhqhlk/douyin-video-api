# Vercel 部署方案对比

## 方案 A: yt-dlp (可行，需要 Cookie)

### 优势
- ✅ 已经写好的代码
- ✅ 依赖包大小在限制内 (~30MB)
- ✅ 执行时间可控

### 劣势
- ❌ **必须配置 Cookie**
- ⚠️ Cookie 会过期，需要定期更新
- ⚠️ 冷启动可能较慢

### 部署配置

`vercel.json`:
```json
{
  "functions": {
    "api/video/parse.py": {
      "runtime": "python3.9",
      "maxDuration": 10
    }
  }
}
```

`.env` (Vercel 环境变量):
```bash
DOUYIN_COOKIE=你的抖音Cookie
```

### 预计成本
- ✅ **完全免费**（Vercel Free Plan）
- 每月 100GB 带宽
- 100 次函数调用/天

---

## 方案 B: TikTokDownloader 简化版 (复杂，不推荐)

### 需要做的工作
1. 提取核心解析逻辑（不使用 FastAPI）
2. 移除 Uvicorn 依赖
3. 改造为无状态函数
4. 重新实现所有端点

### 工作量估算
- ⏱️ 8-12 小时开发时间
- 🐛 大量测试和调试
- 📦 可能仍然超过依赖大小限制

### 结论
❌ **不推荐**，工作量太大，不如直接用 Railway

---

## 推荐方案总结

### 🏆 最佳方案：Railway.app + TikTokDownloader

**理由：**
1. ✅ 无需 Cookie（或 Cookie 可选）
2. ✅ 代码零修改
3. ✅ 5 分钟完成部署
4. ✅ 自动 HTTPS
5. ✅ 稳定可靠

**费用：**
- 免费额度：$5/月
- 预计使用：$0-2/月（轻度使用）

### 🥈 备选方案：Vercel + yt-dlp (需要 Cookie)

**适用场景：**
- 已有 Vercel 项目
- 可以定期更新 Cookie
- 请求量不大

**需要做：**
1. 配置 DOUYIN_COOKIE 环境变量
2. 定期更新 Cookie（7-30天）
3. 处理 Cookie 过期的降级逻辑

---

## 快速部署指南

### Railway 部署（推荐）

```bash
# 1. Fork TikTokDownloader 到你的 GitHub
# 2. 访问 railway.app
# 3. 点击 "New Project"
# 4. 选择 "Deploy from GitHub repo"
# 5. 选择 TikTokDownloader
# 6. 等待自动部署完成
# 7. 复制生成的 URL：https://your-app.railway.app
```

### Vercel 部署（yt-dlp 方案）

```bash
# 1. 确保 api/video/parse.py 存在
cd /Users/kk/project/newsnexttime/hot-search-hub

# 2. 部署到 Vercel
vercel

# 3. 在 Vercel Dashboard 添加环境变量
# DOUYIN_COOKIE=你的Cookie值

# 4. 重新部署
vercel --prod
```

---

## 成本对比

| 平台 | 免费额度 | 月费用（轻度） | 月费用（中度） |
|------|---------|-------------|-------------|
| **Railway** | $5/月 | $0-2 | $5-10 |
| **Vercel** | 100GB/月 | $0 | $0 |
| **Render** | 750h/月 | $0 | $0-7 |
| **Fly.io** | 3 VMs | $0-2 | $5-10 |

---

## 我的建议

**如果你想要最佳效果：**
→ 使用 **Railway + TikTokDownloader**（无需 Cookie，稳定可靠）

**如果你必须用 Vercel：**
→ 使用 **Vercel + yt-dlp**（需要配置和维护 Cookie）

需要我帮你选择并开始部署吗？
