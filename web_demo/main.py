from flask import Flask, send_from_directory, request
from db_service import get_districts, get_sum

app = Flask(__name__, static_folder='www')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('./www', path)


@app.route('/api/districts')
def districts():
    return get_districts()


@app.route('/api/sum')
def _sum():
    return get_sum(request.args.get('location'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8078, debug=True)

