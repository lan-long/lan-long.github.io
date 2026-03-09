# 🦞 蓝龙的主页部署清单

## ✅ 已完成

- [x] `_config.yml` - 站点配置文件（包含你的信息、研究兴趣、奖项等）
- [x] `about.md` - 主页内容（简介、新闻、精选论文）
- [x] `navigation.yml` - 导航菜单
- [x] `README.md` - 部署指南

## 📋 接下来你需要做的

### 1️⃣ Fork AcademicPages 模板

访问：https://github.com/academicpages/academicpages.github.io

点击 **"Use this template"** → **"Create a new repository"**

仓库名：`lan-long/lan-long.github.io`

### 2️⃣ 上传配置文件

把 workspace 里的文件上传到 GitHub 仓库：

```bash
cd /root/.openclaw/workspace/homepage

# 初始化 git
git init
git remote add origin https://github.com/lan-long/lan-long.github.io.git

# 添加文件
git add _config.yml about.md navigation.yml README.md

# 提交
git commit -m "Initial commit - Long Lan's academic homepage"

# 推送
git push -u origin master
```

### 3️⃣ 上传头像和简历

- `profile.png` - 你的头像照片
- `files/cv.pdf` - 个人简历 PDF

### 4️⃣ 启用 GitHub Pages

仓库 → Settings → Pages → Source 选 **GitHub Actions**

等待几分钟，网站就会上线！

访问：https://lan-long.github.io

---

## 🎨 主题预览

AcademicPages 主题特点：
- ✅ 左侧边栏个人简介
- ✅ 论文列表自动格式化
- ✅ 支持数学公式 (MathJax)
- ✅ 响应式设计（手机友好）
- ✅ 自动生成 CV 页面

---

## 📞 需要帮助？

有问题随时问我！
