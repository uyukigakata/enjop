# SecHack365_4C_えんじょっぷ

# Backend環境構築

### 仮想環境作成
```bash
python -m venv venv
```
### パッケージ一覧

```bash
pip install openai
pip install google-cloud-vision
pip install google-cloud-speech-to-text
pip install flask
pip install flask_cors
pip install firebase  
pip install firebase-admin
pip install python-dotenv
pip install opencv-python

```

### パッケージインストール一括
```bash
pip install -r requirements.txt
```

### venvの中身を生成
```bash
pip install -r requirements.txt
```

### 実行方法
```bash
python server
```

# frontendの環境構築

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

### パッケージインストール

```bash
pnpm install
pnpm install vuex
pnpm install axios
```

### Run Development Server
```bash
pnpm dev
```
### Type-Check, Compile and Minify for Production
```bash
pnpm build
```
### Lint

```bash
pnpm lint
```
