# 数据库管理应用

这是一个简单的数据库管理Web应用，使用Node.js和MySQL构建，可以部署到AWS AppRunner上。

## 功能
- 查看数据库中的数据
- 添加新数据
- 编辑现有数据
- 删除数据
- 搜索数据

## 部署到AWS AppRunner

1. 将代码上传到GitHub仓库
2. 在AWS AppRunner控制台创建新服务
3. 选择源代码部署方式
4. 配置构建命令和启动命令
5. 设置环境变量（数据库连接信息）
6. 部署应用

## 环境变量
- `DB_HOST`: 数据库主机地址
- `DB_USER`: 数据库用户名
- `DB_PASSWORD`: 数据库密码
- `DB_NAME`: 数据库名称
- `PORT`: 应用端口（默认为3000）

## 数据库表结构
```sql
CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
