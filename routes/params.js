const express = require('express');
const router = express.Router();
const config = require('../config');

/* display room list */
router.get('/', function(req, res, next) {
    const secret = JSON.parse(config.secret.db_secret);
    secret.password = "Shhhh! It's a secret";
    res.render('param-list', { menuTitle: config.app.hotel_name, infraParams: config.infra, appParams: config.app, secretParams: secret });
});

module.exports = router;