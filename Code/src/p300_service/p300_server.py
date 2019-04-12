from sanic import Sanic
import socketio
import ml

import numpy as np
from sklearn.model_selection import train_test_split

# for testing
import random

# for database
# from sqlalchemy import create_engine, text
import os
import hashlib
import binascii


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


class P300Service:
    def __init__(self):
        self.sio = socketio.AsyncServer(async_mode='sanic')
        self.app = Sanic()
        self.sio.attach(self.app)

        self.clf = {}
        self.inputs = {}
        self.targets = {}

        self.last_uuid = {}
        self.last_acc = {}

        self.users = {}

    def update_weights(self, sid, accuracy, weights_path):
        engine = create_engine(os.environ['DATABASE_URL'])
        with engine.begin() as connection:
            user_id = connection.execute(
                text('''
                    SELECT
                        u.id
                    FROM auth_user u
                    WHERE u.username = :username
                '''),
                username=self.users[sid]['username']
            ).fetchall()
            if user_id:
                user_id_exists = connection.exceute(
                    text('''
                        SELECT
                            w.id
                        FROM user_weights w
                        WHERE w.user_id = :user_id
                    '''),
                    user_id=user_id[0]
                )
                if user_id_exists:
                    connection.execute(
                        text('''
                            UPDATE user_weights
                            SET
                                accuracy = :accuracy,
                                weights = :weights,
                                last_update = NOW()::date
                            WHERE
                                user_id = :user_id
                        '''),
                        user_id=user_id[0],
                        accuracy=accuracy,
                        weights=weights_path
                    )
                    return True
                else:
                    connection.execute(
                        text('''
                            INSERT INTO user_weights ("user_id", "accuracy", "weights", "last_updated")
                            VALUES (
                                :user_id,
                                :accuracy,
                                :weights,
                                NOW()::date
                            )
                        '''),
                        user_id=user_id[0],
                        accuracy=accuracy,
                        weights=weights_path
                    )
                    return True
            return False

    async def load_classifier(self, sid, args):
        if self.users.get(sid) is not None:
            try:
                self.clf[sid] = ml.load(f'clfs/{self.users[sid]["username"]}')
                return sid, True
            except FileNotFoundError:
                raise Exception(f'Cannot load classifier')

            self.clf[sid] = None
            return sid, False
        else:
            raise Exception(f'User not logged in!')

    async def train_classifier(self, sid, args):
        if self.users.get(sid) is not None:
            uuid, eeg_data, p300 = args

            # initialize if empty
            self.inputs[sid] = self.inputs.get(sid, [])
            self.targets[sid] = self.targets.get(sid, [])

            self.inputs[sid].append(np.array(eeg_data))
            self.targets[sid].append(np.array(p300))

            if len(self.targets[sid]) % 10 == 0 and len(self.targets[sid]) >= 20:
                X = np.array(self.inputs[sid])
                print(X.shape)
                y = np.array(self.targets[sid])

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

                # Note in Barachant's ipynb, 'erpcov_mdm' performed best. 'vect_lr' is the
                # universal one for EEG data.

                # train
                self.clf[sid] = ml.ml_classifier(X_train, y_train, classifier=None, pipeline='vect_lr')
                acc = self.clf[sid].score(X_test, y_test)

                # save classifier
                if not os.path.exists('clfs'):
                    os.makedirs('clfs')
                ml.save(f'clfs/{self.users[sid]["username"]}', self.clf[sid])

                # self.update_weights(sid=sid, accuracy=acc, weights_path=f'clfs/{self.users[sid]["username"]}')

                results = (uuid, acc)
                return sid, results
            return sid, None
        else:
            raise Exception(f'User not logged in!')

    async def retrieve_prediction_results(self, sid, args):
        if self.users.get(sid) is not None:
            uuid, data = args
            data = np.array(data)
            data = np.expand_dims(data, axis=0)

            # load classifier if not already loaded
            if self.clf.get(sid) is None:
                self.clf[sid] = ml.load(f'clfs/{self.users[sid]["username"]}')
            p300 = self.clf[sid].predict(data)
            p300 = p300[0]

            score = 1
            results = (uuid, p300, score)
            return sid, results
        else:
            raise Exception(f'User not logged in!')

    # for testing
    async def retrieve_prediction_results_test(self, sid, args):
        uuid, eeg_data = args
        p300 = random.choice([True, False])
        score = random.random()
        results = (uuid, p300, score)
        return sid, results

    async def train_classifier_test(self, sid, args):
        uuid, eeg_data, p300 = args
        acc = random.random()
        results = (uuid, acc)
        return sid, results

    async def register(self, sid, args):
        username, password, email = args
        engine = create_engine(os.environ['DATABASE_URL'])
        with engine.begin() as connection:
            user_exists = connection.execute(
                text('''
                    SELECT
                        u.username
                    FROM auth_user u
                    WHERE u.username = :username
                '''),
                username=username
            ).fetchall()
            if not user_exists:
                password = hash_password(password)
                connection.execute(
                    text('''
                        INSERT INTO auth_user ("username", "password", "email", "created_on")
                        VALUES (
                            :username,
                            :password,
                            :email,
                            NOW()::date
                        )
                    '''),
                    username=username,
                    password=password,
                    email=email,
                )
                return sid, True
        return sid, False

    async def login(self, sid, args):
        username, password = args
        engine = create_engine(os.environ['DATABASE_URL'])

        with engine.begin() as connection:
            stored_password = connection.execute(
                text('''
                    SELECT
                        u.password
                    FROM auth_user u
                    WHERE u.username = :username
                '''),
                username=username
            ).fetchall()
            if stored_password:
                # query returns list of tuples (tuple of rows for each column)
                verified = verify_password(stored_password[0][0], password)
                if verified:
                    result = connection.execute(
                        text('''
                            SELECT
                                u.username,
                                w.accuracy,
                                w.weights,
                                w.last_updated
                            FROM auth_user u
                            LEFT JOIN user_weights w
                                ON w.user_id = u.id
                            WHERE u.username = :username
                        '''),
                        username=username,
                    ).fetchall()
                    user_details = dict(zip(['username', 'accuracy', 'weights', 'last_updated'], result[0]))
                    user_details['login'] = True
                    self.users[sid] = user_details

                    connection.execute(
                        text('''
                            UPDATE auth_user
                            SET
                                last_login = NOW()::date
                            WHERE
                                username = :username
                        '''),
                        username=username
                    )
                    return sid, True
            return sid, False

    async def logout(self, sid, args):
        # logout
        self.users[sid] = None
        # reset classifier for channel
        self.clf[sid] = None
        return sid, True

    def initialize_handlers(self):
        # login
        self.sio.on("register", self.register)
        self.sio.on("login", self.login)
        self.sio.on("logout", self.logout)

        self.sio.on("retrieve_prediction_results", self.retrieve_prediction_results)
        self.sio.on("train_classifier", self.train_classifier)
        self.sio.on("load_classifier", self.load_classifier)

        # for testing
        self.sio.on("retrieve_prediction_results_test", self.retrieve_prediction_results_test)
        self.sio.on("train_classifier_test", self.train_classifier_test)


if __name__ == '__main__':
    service = P300Service()
    service.initialize_handlers()
    service.app.run(host='localhost', port=8001)
