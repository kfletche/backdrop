class FlaskTestClient(object):
    def __init__(self, flask_app):
        self._client = flask_app.app.test_client()
        self._storage = flask_app.mongo[flask_app.app.config['DATABASE_NAME']]

    def get(self, url):
        return self._client.get(url)

    def post(self, url, **message):
        return self._client.post(url, **message)

    def storage(self):
        return self._storage

    def spin_down(self):
        pass