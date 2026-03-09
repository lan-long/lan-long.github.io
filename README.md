# 蓝龙的学术主页 - 部署指南

这是基于 **AcademicPages** Jekyll 主题的学术主页。

## 🚀 快速部署步骤

### 步骤 1: Fork 模板

1. 访问 https://github.com/academicpages/academicpages.github.io
2. 点击 **"Use this template"** → **"Create a new repository"**
3. 命名仓库为：`lan-long/lan-long.github.io`

### 步骤 2: 启用 GitHub Pages

1. 进入仓库 **Settings** → **Pages**
2. Source 选择：**GitHub Actions**
3. 等待网站自动构建

### 步骤 3: 上传配置文件

将以下文件上传到你的仓库：
- `_config.yml` - 站点配置
- `about.md` - 主页内容
- `profile.png` - 你的头像照片

### 步骤 4: 添加 CV 和论文 PDF

创建 `files/` 目录，上传：
- `cv.pdf` - 个人简历
- 论文 PDF 文件

### 步骤 5: 自定义域名（可选）

在 Settings → Pages → Custom domain:
- 输入：`lan-long.github.io`
- 保存

---

## 📁 文件结构

```
lan-long.github.io/
├── _config.yml          # 站点配置（已创建）
├── about.md             # 主页内容（已创建）
├── profile.png          # 头像（需上传）
├── files/
│   ├── cv.pdf          # 简历（需上传）
│   └── papers/         # 论文 PDF
├── _publications/       # 论文页面（可选）
├── _talks/             # 演讲页面（可选）
└── images/             # 图片资源
```

---

## 🎨 主题定制

### 更换主题颜色
在 `_config.yml` 中修改：
```yaml
site_theme: "default"  # 可选："air", "sunrise", "mint", "dirt", "contrast"
```

### 添加更多内容

**论文页面** - 在 `_publications/` 目录创建 Markdown 文件：
```markdown
---
title: "论文标题"
collection: publications
permalink: /publication/2026-01-01-paper-title
type: "journal"
venue: "TPAMI"
date: 2026-01-01
---
```

**演讲页面** - 在 `_talks/` 目录创建

---

## 🛠️ 本地预览

```bash
# 安装 Jekyll
gem install bundler
bundle install

# 本地运行
bundle exec jekyll serve
# 访问 http://localhost:4000
```

---

## 📝 后续更新

1. **添加新论文** → 编辑 `about.md` 或创建 `_publications/` 文件
2. **更新新闻** → 修改 `_config.yml` 中的 `news` 部分
3. **更换头像** → 替换 `profile.png`

---

## 🔗 有用的链接

- [AcademicPages 文档](https://academicpages.github.io/markdown/)
- [Jekyll 文档](https://jekyllrb.com/docs/)
- [GitHub Pages 文档](https://docs.github.com/en/pages)

---

**有问题？** 直接在 GitHub 上提 issue 或联系我！
