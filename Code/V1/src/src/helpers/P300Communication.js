import io from "socket.io-client";
const uuid_v1 = require("uuid/v1");

export function sendTrainingFlashEvent(client_socket, p300) {
    let uuid = uuid_v1();
    let timestamp = Date.now() / 1000.0;

    let json = {
        'uuid': uuid,
        'timestamp': timestamp,
        'p300': p300
    }

    client_socket.emit("train", JSON.stringify(json), console.log);
}