#!/usr/bin/env node
// Reads the tmp101 temperature sensor.

var i2c     = require('i2c-bus');
var fs      = require('fs');
var request = require('request');
var util    = require('util');

var filename = "./keys_tmp101.json";

var bus = 2;
var tmp101 = [0x48, 0x49];
var tmp006 = 0x40;
var time = 1000;    // Time between readings

var sensor = i2c.openSync(bus);

var keys = JSON.parse(fs.readFileSync(filename));
// console.log("Using: " + filename);
console.log("Title: " + keys.title);
console.log(util.inspect(keys));

var urlBase = keys.inputUrl + "?private_key=" + keys.privateKey
                + "&temp1=%s&temp2=%s&temp3=%s";

var temp = [];

// Read the temp sensors
var tmp101s = tmp101.length;
for(var i=0; i<tmp101s; i++) {
    temp[i] = sensor.readByteSync(tmp101[i], 0x0);
    // temp[i] = Math.random();
    console.log("temp: %dC, %dF (0x%s)", temp[i], temp[i]*9/5+32, tmp101[i].toString(16));
}

temp[tmp101s] = (sensor.readWordSync(tmp006, 0x1));
temp[tmp101s] = ((temp[tmp101s] & 0xFF) << 8) | ((temp[tmp101s] >> 8) & 0xFF);
temp[tmp101s] = temp[tmp101s] >> 2;
temp[tmp101s] = temp[tmp101s] / 32;
console.log("temp: %dC, %dF (0x%s)", temp[tmp101s], temp[tmp101s]*9/5+32, tmp006.toString(16));

// Substitute in the temperatures
var url = util.format(urlBase, temp[0], temp[1], temp[2]);
console.log("url: ", url);

// Send to phant
request(url, function (err, res, body) {
    if (!err && res.statusCode == 200) {
        console.log(body);
    } else {
        console.log("error=" + err + " response=" + JSON.stringify(res));
    }
});
