const express = require('express');
const mysql = require('mysql2/promise');
const app = express();
const port = process.env.PORT || 3000;

// 从环境变量获取数据库配置
const dbConfig = {
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
};

// 中间件
app.use(express.json());
app.use(express.static('public'));

// 数据库连接池
let pool;
async function initDb() {
    pool = mysql.createPool(dbConfig);
    console.log('数据库连接池已创建');
}

// 初始化应用
async function init() {
    await initDb();
    
    app.listen(port, () => {
        console.log(`服务器运行在 http://localhost:${port}`);
    });
}

// 获取所有数据
app.get('/api/data', async (req, res) => {
    const { q } = req.query;
    let sql = 'SELECT * FROM items';
    let params = [];
    
    if (q) {
        sql += ' WHERE name LIKE ? OR description LIKE ?';
        params = [`%${q}%`, `%${q}%`];
    }
    
    try {
        const [rows] = await pool.query(sql, params);
        res.json(rows);
    } catch (error) {
        console.error('查询数据失败:', error);
        res.status(500).json({ error: '查询数据失败' });
    }
});

// 获取单个数据
app.get('/api/data/:id', async (req, res) => {
    const { id } = req.params;
    
    try {
        const [rows] = await pool.query('SELECT * FROM items WHERE id = ?', [id]);
        if (rows.length === 0) {
            return res.status(404).json({ error: '数据不存在' });
        }
        res.json(rows[0]);
    } catch (error) {
        console.error('获取数据失败:', error);
        res.status(500).json({ error: '获取数据失败' });
    }
});

// 创建数据
app.post('/api/data', async (req, res) => {
    const { name, description } = req.body;
    
    if (!name) {
        return res.status(400).json({ error: '名称不能为空' });
    }
    
    try {
        const [result] = await pool.query(
            'INSERT INTO items (name, description) VALUES (?, ?)',
            [name, description]
        );
        res.status(201).json({ id: result.insertId, name, description });
    } catch (error) {
        console.error('创建数据失败:', error);
        res.status(500).json({ error: '创建数据失败' });
    }
});

// 更新数据
app.put('/api/data/:id', async (req, res) => {
    const { id } = req.params;
    const { name, description } = req.body;
    
    if (!name) {
        return res.status(400).json({ error: '名称不能为空' });
    }
    
    try {
        const [result] = await pool.query(
            'UPDATE items SET name = ?, description = ? WHERE id = ?',
            [name, description, id]
        );
        
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: '数据不存在' });
        }
        
        res.json({ id, name, description });
    } catch (error) {
        console.error('更新数据失败:', error);
        res.status(500).json({ error: '更新数据失败' });
    }
});

// 删除数据
app.delete('/api/data/:id', async (req, res) => {
    const { id } = req.params;
    
    try {
        const [result] = await pool.query('DELETE FROM items WHERE id = ?', [id]);
        
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: '数据不存在' });
        }
        
        res.status(204).end();
    } catch (error) {
        console.error('删除数据失败:', error);
        res.status(500).json({ error: '删除数据失败' });
    }
});

// 启动应用
init();