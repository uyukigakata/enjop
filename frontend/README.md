# SecHack365_4C_enjo Frontend

このディレクトリは、SecHack365の表現駆動コース チーム4Cのフロントエンドのディレクトリです。

### セットアップ方法

```bash
# まずはnode.jsをインストール
# Install nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
# Install node.js version 23 
nvm install 23
node -v
npm -v
# Install pnpm
curl -fsSL https://get.pnpm.io/install.sh | sh -
```

### プロジェクトのセットアップ

```bash
pnpm install
pnpm install vuex
pnpm install axios
# Run Development Server


pnpm dev
# Type-Check, Compile and Minify for Production
pnpm build
# Lint
pnpm lint
```

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).