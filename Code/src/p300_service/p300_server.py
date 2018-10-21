from sanic import Sanic
import socketio
from eeg_stream import EEGStream
from marker_stream import MarkerStream
from ml_stream import MLStream


class P300Service:
    def __init__(self):
        self.sio = socketio.AsyncServer(async_mode='sanic')
        self.app = Sanic()
        self.sio.attach(self.app)
        self.eeg_streams = {}
        self.marker_streams = {}
        self.ml_streams = {}

    async def create_eeg_stream_handler(self, sid):
        self.eeg_streams[sid] = EEGStream(thread_name='EEG_data', event_channel_name='P300')
        print("New eeg stream created.")
        print(self.eeg_streams)
        await self.sio.emit("eeg_stream_created", sid)

    async def create_marker_stream_handler(self, sid):
        self.marker_streams[sid] = MarkerStream()
        print("New marker stream created.")
        print(self.marker_streams)
        await self.sio.emit("marker_stream_created", sid)

    async def create_ml_stream_handler(self, sid, data):
        if sid not in self.eeg_streams:
            raise Exception(f"eeg stream in channel {sid} does not exist")
        if sid not in self.marker_streams:
            raise Exception(f"marker stream in channel {sid} does not exist")
        self.ml_streams[sid] = MLStream(m_stream=self.marker_streams[sid],
                                        eeg_stream=self.eeg_streams[sid],
                                        classifier_path=data['classifier_path'],
                                        test_path=data['test_path'],
                                        analysis_time=data['analysis_time'],
                                        event_time=data['event_time'],
                                        train=data['train'],
                                        train_epochs=data['train_epochs'],
                                        get_test=data['get_test'])
        print("New ml_stream created.")
        print(self.ml_streams)
        await self.sio.emit("ml_stream_created", sid)

    async def eeg_stream_start_handler(self, sid):
        if sid in self.eeg_streams:
            eeg_stream = self.eeg_streams[sid]
        else:
            raise (RuntimeError, "Cannot start EEG stream with sid {}".format(sid))
        eeg_stream.lsl_connect()
        await self.sio.emit("eeg_stream_started", sid, 'eeg')

    async def marker_stream_start_handler(self, sid):
        if sid in self.marker_streams:
            marker_stream = self.marker_streams[sid]
        else:
            raise Exception("Cannot start marker stream with sid {}".format(sid))
        marker_stream.lsl_connect()
        await self.sio.emit("marker_stream_started", sid, 'marker')

    async def ml_stream_start_handler(self, sid):
        if sid in self.ml_streams:
            ml_stream = self.ml_streams[sid]
        else:
            raise Exception("Cannot start ML stream with sid {}".format(sid))
        ml_stream.lsl_connect()
        await self.sio.emit("ml_stream_started", sid, 'ml')

    def initialize_handlers(self):
        self.sio.on("create_eeg_stream", self.create_eeg_stream_handler)
        self.sio.on("create_marker_stream", self.create_marker_stream_handler)
        self.sio.on("create_ml_stream", self.create_ml_stream_handler)
        self.sio.on("start_eeg_stream", self.eeg_stream_start_handler)
        self.sio.on("start_marker_stream", self.marker_stream_start_handler)
        self.sio.on("start_ml_stream", self.ml_stream_start_handler)


if __name__ == '__main__':
    service = P300Service()
    service.initialize_handlers()
    service.app.run(host='localhost', port=8001)
