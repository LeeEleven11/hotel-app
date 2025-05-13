const express = require('express');
const router = express.Router();
const config = require('../config');
const rds = require('../rds');

/* Add a new room */
router.post('/', function (req, res, next) {
    const { roomNumber, floorNumber, hasView, occupied, comment } = req.body;
    if (!roomNumber || !floorNumber || typeof hasView === 'undefined') {
        return next(new Error('Missing room id, floor or has view parameters'));
    }

    console.log('New room request received. roomNumber: %s, floorNumber: %s, hasView: %s', roomNumber, floorNumber, hasView);

    const sql = "INSERT INTO hotel.rooms (id, floor, hasView, occupied, comment) VALUES (?, ?, ?, ?, ?)";
    const sqlParams = [roomNumber, floorNumber, hasView, occupied || false, comment || ''];

    const [pool, url] = rds();
    pool.getConnection(function(err, con) {
        if (err) {
            return next(err);
        }
        con.query(sql, sqlParams, function(err, result, fields) {
            con.release();
            if (err) {
                return res.send(err);
            }
            res.render('add', { title: 'Add new room', view: 'No', result: { roomId: roomNumber } });
            if (fields) {
                console.log(fields);
            }
        });
    });
});

router.get('/', function(req, res, next) {
    res.render('add', { title: 'Add new room', menuTitle: config.app.hotel_name, view: 'No' });
});

module.exports = router;