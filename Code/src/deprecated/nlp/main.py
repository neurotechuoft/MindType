import socketio
from sanic import Sanic

import trie_funcs

sio = socketio.AsyncServer()

# Only if you want to use a custom server; here I want to us Sanic
app = Sanic()
sio.attach(app)


@sio.on('predict')
async def handle_data(sid, data):
    await trie_funcs.autocomplete(data)


if __name__ == '__main__':
    app.run(host='localhost', port=8001)

