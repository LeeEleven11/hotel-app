# 构建阶段：安装编译依赖
FROM python:3.9-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    apt-utils \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 运行阶段：只包含运行时必要的组件
FROM python:3.9-slim

WORKDIR /app

# 从构建阶段复制 Python 包
COPY --from=builder /root/.local /root/.local

# 添加用户路径到环境变量
ENV PATH=/root/.local/bin:$PATH

COPY . .

EXPOSE 8080
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["python", "app.py", "--host=0.0.0.0", "--port=8080"]