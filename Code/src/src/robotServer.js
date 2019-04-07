const io = require('socket.io');
const server = io.listen(8002);

var robot = require('robotjs');

server.on('connection', function (socket) {
    socket.on('typing', function (data) {
        //robot js
        robot.typeString(data);
    });
});