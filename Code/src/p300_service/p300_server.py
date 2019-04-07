from sanic import Sanic
import socketio
import ml

import numpy as np
from sklearn.model_selection import train_test_split

# for testing
import random

# for database
from sqlalchemy import create_engine, text
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

        self.clf = None
        self.inputs = []
        self.targets = []

        self.last_uuid = -1
        self.last_acc = 0.

        self.users = {}

    async def load_classifier(self, sid):
        try:
            self.clf = ml.load(f"tests/data/classifier.pkl")
        except FileNotFoundError:
            raise Exception(f"Cannot load classifier")

    async def train_classifier(self, sid, args):
        uuid, eeg_data, p300 = args
        self.inputs.append(np.array(eeg_data))
        self.targets.append(np.array(p300))

        if len(self.targets) % 10 == 0 and len(self.targets) > 70:
            X = np.array(self.inputs)
            y = np.array(self.targets)

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

            # Note in Barachant's ipynb, 'erpcov_mdm' performed best. 'vect_lr' is the
            # universal one for EEG data.
            self.clf = ml.ml_classifier(X_train, y_train, pipeline='vect_lr')
            acc = self.clf.score(X_test, y_test)
            ml.save(f"tests/data/clf.pkl", classifier)

            self.last_uuid = uuid
            self.last_acc = acc

        results = (self.last_uuid, self.last_acc)
        return sid, results

    async def retrieve_prediction_results(self, sid, args):
        uuid, data = args
        p300 = self.clf.predict(data)
        score = 1
        results = (uid, p300, score)
        return sid, results


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
            ).fetchall()[0]
            if stored_password is not None:
                verified = verify_password(stored_password, password)
                if verified:
                    result = connection.execute(
                        text('''
                            SELECT 
                                u.username, 
                                w.accuracy, 
                                w.weights, 
                                w.last_updated 
                            FROM auth_user u 
                            INNER JOIN user_weights w 
                                ON w.user_id = u.id
                            WHERE u.username = :username
                            AND u.password = :password
                        '''),
                        username=username,
                        password=password
                    ).fetchall()
                    user_details = dict(zip(['username', 'accuracy', 'weights', 'last_updated'], result))
                    user_details['login'] = True
                    self.users[sid] = user_details

                    connection.execute(
                        text('''
                            INSERT INTO auth_user ("last_login")
                            VALUES (NOW()::date)
                        ''')
                    )
                    return sid, True
            return sid, False

    async def update_weights(self, sid, args):
        accuracy, weights = args
        if self.users[sid]['login']:
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
                            weights=weights
                        )
                        return sid, True
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
                            weights=weights
                        )
                        return sid, True
                return sid, False

    def initialize_handlers(self):
        # login and weights
        self.sio.on("register", self.register)
        self.sio.on("login", self.login)
        self.sio.on("update_weights", self.update_weights)

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
