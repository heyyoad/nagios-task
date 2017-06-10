var express = require('express');
var router = express.Router();
pg = require('pg');
const path = require('path');
const connectionString = process.env.DATABASE_URL || 'postgres://pg_user:justforfun@127.0.0.1:5432/rss_feeds';


/* GET home page. */
router.get('/', function(req, res, next) {
    res.sendFile('index.html');
});

router.get('/feeds', (req, res, next) => {
    const results = [];
// Get a Postgres client from the connection pool
pg.connect(connectionString, (err, client, done) => {
    // Handle connection errors
    if(err) {
        done();
        console.log(err);
        return res.status(500).json({success: false, data: err});
    }
    // SQL Query > Select Data
    const query = client.query('SELECT * FROM feeds ORDER BY post_date ASC;');
// Stream results back one row at a time
query.on('row', (row) => {
    results.push(row);
});
// After all data is returned, close connection and return results
query.on('end', () => {
    done();
return res.json(results);
});
});
});

module.exports = router;
