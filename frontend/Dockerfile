# Nodeの公式イメージをベースに使用
FROM node:20.10.0-alpine

# 作業ディレクトリを設定
WORKDIR /app

# 依存ファイルをコピーしてインストール
COPY ./frontend/package*.json ./
RUN npm install

# アプリケーションのコードとindex.htmlをコピー
COPY ./frontend/src /app/src
COPY ./frontend/index.html /app
COPY ./frontend/vite.config.ts /app
COPY ./frontend/tsconfig.json /app
COPY ./frontend/tsconfig.node.json /app
COPY ./frontend/tsconfig.app.json /app

# アプリケーションをビルド
RUN npm run build-only

# Nginxを使用してサービスを実行
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
