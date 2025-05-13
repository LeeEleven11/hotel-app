const express = require('express');
const router = express.Router();
const config = require('../config');
const rds = require('../rds');

/* display room list */
router.get('/', function(req, res, next) {
    const [pool, url] = rds();
    pool.getConnection(function(err, con) {
        if (err) {
            return next(err);
        }
        con.query('SELECT * FROM hotel.rooms', function(error, results, fields) {
            con.release();
            if (error) {
                return res.send(error);
            }
            res.render('room-list', { title: 'Room List', menuTitle: config.app.hotel_name, url: url, rooms: results});
            console.log('displayed %d rooms', results.length);
        });
    });
});

module.exports = router;