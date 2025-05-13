const express = require('express');
const router = express.Router();
const config = require('../config');
const rds = require('../rds');

router.get('/', function(req, res, next) {
    const [pool, rdsUrl] = rds();
    pool.getConnection(function(err, con) {
        if (err) {
            return next(err);
        }
        const queries = [
            'CREATE DATABASE IF NOT EXISTS hotel;',
            'USE hotel;',
            'CREATE TABLE IF NOT EXISTS rooms(id int NOT NULL, floor int, hasView boolean, occupied boolean, comment varchar(60), PRIMARY KEY(id));'
        ];

        const executeQueries = (index) => {
            if (index === queries.length) {
                con.release();
                return res.render('create', { menuTitle: config.app.hotel_name, url: rdsUrl });
            }
            con.query(queries[index], function(error, result, fields) {
                if (error) {
                    con.release();
                    return next(error);
                }
                executeQueries(index + 1);
            });
        };

        executeQueries(0);
    });
});

module.exports = router;