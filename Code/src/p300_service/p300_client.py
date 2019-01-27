from socketIO_client import SocketIO


def on_connect():
    print("Connected")


def on_disconnect():
    print("Disconnected")


def on_stream_created(*args):
    def on_type_stream_created(stream_type=args[1], sid=args[0]):
        print('{} stream created, SID: {}'.format(stream_type, sid))
    return on_type_stream_created()


def on_stream_started(*args):
    def on_type_stream_started(stream_type=args[1], sid=args[0]):
        print('{} stream started, SID: {}'.format(stream_type, sid))
    return on_type_stream_started()


def on_retrieve_prediction_results(*args):
    def on_retrieve_results(results=args[1], sid=args[0]):
        print(f'Results: {results}')
    return on_retrieve_results()


class P300Client(object):
    def __init__(self):
        results = []


if __name__ == '__main__':
    socket_client = SocketIO("localhost", 8001)
    socket_client.on("eeg_stream_created", on_stream_created)
    socket_client.on("marker_stream_created", on_stream_created)
    socket_client.on("ml_stream_created", on_stream_created)
    socket_client.on("eeg_stream_started", on_stream_created)
    socket_client.on("marker_stream_started", on_stream_created)
    socket_client.on("ml_stream_started", on_stream_created)
    socket_client.on("retrieve_prediction_results", on_retrieve_prediction_results)
    socket_client.connect()
    socket_client.emit("create_eeg_stream")
    socket_client.emit("create_marker_stream")
    socket_client.emit("create_ml_stream",
                       {'classifier_path': 'classifer.pkl',
                        'test_path': 'test_set.pkl',
                        'analysis_time': 1,
                        'event_time': 0.2,
                        'train': True,
                        'train_epochs': 120,
                        'get_test': True,
                        })
    socket_client.emit("start_marker_stream")
    socket_client.disconnect()
