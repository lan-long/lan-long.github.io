# 🔐 蓝龙的私密学术主页 - Netlify 部署指南

这是**完全私密**版本，只有知道密码的人才能访问。

---

## 🚀 部署到 Netlify（10 分钟搞定）

### 方法 A：直接从 GitHub 部署（推荐）

#### 1. 访问 Netlify
https://app.netlify.com

#### 2. 登录/注册
- 用 GitHub 账号登录（最快）
- 或用邮箱注册

#### 3. 添加新站点
- 点击 **"Add new site"** → **"Import an existing project"**
- 选择 **GitHub**
- 授权 Netlify 访问你的 GitHub 仓库
- 选择 `lan-long/lan-long.github.io`

#### 4. 配置构建设置
- **Build command:** `jekyll build`
- **Publish directory:** `_site`
- 点击 **"Advanced build settings"**
- 添加环境变量：
  - `JEKYLL_ENV` = `production`

#### 5. 部署！
- 点击 **"Deploy site"**
- 等待 2-5 分钟构建完成

#### 6. 设置密码保护 ⭐

**Netlify 免费版密码保护：**

1. 进入站点设置 → **"Identity"**
2. 点击 **"Enable Identity"**
3. 在 **"Registration"** 选 **"Invite only"**
4. 进入 **"Users"** 标签
5. 点击 **"Invite users"**
6. 输入要授权的人的邮箱（包括你自己）
7. 他们会收到邀请邮件，注册后才能访问

**或者用 Netlify Password Protection（更简单）：**

1. 进入站点 → **"Site settings"** → **"Password protection"**
2. 设置一个密码
3. 保存
4. 访问者需要输入密码才能看

---

### 方法 B：手动上传（更快，不用 GitHub）

#### 1. 下载本地文件
```bash
cd /root/.openclaw/workspace/homepage
# 文件都在这里
```

#### 2. 安装 Netlify CLI
```bash
npm install -g netlify-cli
```

#### 3. 登录 Netlify
```bash
netlify login
```

#### 4. 部署
```bash
cd /root/.openclaw/workspace/homepage
netlify deploy --prod
```

- 第一次会问你站点名称 → 输入 `lan-long-academic`
- Publish directory → 输入 `.`

#### 5. 设置密码保护
访问 https://app.netlify.com/sites/lan-long-academic/settings/password

---

## 🔑 密码保护效果

访问者会看到：
```
┌─────────────────────────────────┐
│  🔒 This site is protected      │
│                                 │
│  Enter password to access:      │
│  [________________] [Submit]    │
│                                 │
│  (Only authorized users)        │
└─────────────────────────────────┘
```

---

## 📧 邀请访问者

### Netlify Identity 方式（推荐）

1. 进入 Netlify 站点 → **Identity**
2. 点击 **"Invite users"**
3. 输入邮箱（多个用逗号分隔）
4. 发送邀请
5. 他们收到邮件后注册账号
6. 登录后访问网站自动通过验证

### 密码保护方式（简单）

1. 设置一个强密码（如：`NUDT2026!CVLab`）
2. 把密码告诉需要访问的人
3. 他们输入密码即可访问

---

## 🌐 自定义域名（可选）

如果想用自己的域名：

1. 在 Netlify → **Domain settings**
2. 点击 **"Add custom domain"**
3. 输入你的域名（如 `lan-long.com`）
4. 按提示配置 DNS

---

## 📊 Netlify 免费版限制

- ✅ 无限带宽
- ✅ 无限站点
- ✅ 自动 HTTPS
- ✅ 密码保护
- ✅ 表单收集
- ⚠️ 每月 100GB 流量（学术主页够用）

---

## 🔄 更新内容

### 如果用 GitHub 部署
```bash
# 修改文件后
cd /root/.openclaw/workspace/homepage
git add .
git commit -m "更新内容"
git push
# Netlify 自动重新构建
```

### 如果用手动部署
```bash
netlify deploy --prod
```

---

## 🆘 遇到问题？

- Netlify 文档：https://docs.netlify.com
- 密码保护：https://docs.netlify.com/visitor-access/password-protection/
- Identity 认证：https://docs.netlify.com/visitor-access/identity/

---

**需要我帮你直接部署吗？** 告诉我你选哪个方式！
