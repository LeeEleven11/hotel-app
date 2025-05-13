# 使用Python官方镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到工作目录
COPY . .

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用端口
EXPOSE 8080

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 运行应用
CMD ["python", "app.py"]