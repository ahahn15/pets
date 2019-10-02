import logging
import time
import flask
from flask import request, jsonify
from pydblite import Base


def _create_db():
    try:
        app.db = Base('pets.pdl')
        app.db.create('name', 'type', 'age', 'sex', 'description', 'owner_email', 'image_url')
    except IOError:
        app.db.open()
        print('Base db already exists')


logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

app = flask.Flask(__name__)
_create_db()


@app.route("/health")
def health():
    return "ok"


@app.before_request
def before_request():
    flask.g.requestStart = time.time()
    flask.g.extra_fields = {}


@app.after_request
def after_request(response):
    if flask.request.path == '/health':
        return response

    ms = (time.time() - flask.g.requestStart) * 1000
    level = 'error' if response.status_code > 299 else 'info'

    extra = ''
    query_string = flask.request.query_string.decode("utf-8")
    if len(query_string) > 0:
        extra = 'params="{0}"'.format(query_string)
    for key in flask.g.extra_fields:
        extra += ' ' + key + '=' + str(flask.g.extra_fields[key])
    logging.info('duration_ms=%d status_code=%d path=%s method=%s level=%s %s', ms, response.status_code,
                 flask.request.path, flask.request.method, level, extra)
    return response


@app.route("/pet", methods=["POST"])
def create_pet():
    pets_to_create = request.get_json()
    ids = []
    for pet in pets_to_create:
        new_id = app.db.insert(name=pet["name"], type=pet["type"], age=pet["age"], sex=pet["sex"],
                      description=pet["description"], owner_email=pet["owner_email"], image_url=pet["image_url"])
        ids.append(new_id)
    app.db.commit()
    return jsonify(ids)


@app.route("/pet", methods=["PUT"])
def update_pet():
    pets_to_update = request.get_json()
    for pet in pets_to_update:
        record = app.db[pet['id']]
        attributes = _get_attributes(pet, record)
        app.db.update(record, name=attributes["name"], type=attributes["type"], age=attributes["age"],
                      sex=attributes["sex"], description=attributes["description"],
                      owner_email=attributes["owner_email"], image_url=attributes["image_url"])
    app.db.commit()
    return 'ok'


@app.route("/pet", methods=["DELETE"])
def delete_pet():
    pets_to_delete = request.get_json()
    for pet_id in pets_to_delete:
        del app.db[pet_id]
    return 'ok'


@app.route("/pet", methods=["GET"])
def get_pet():
    filters = request.get_json()
    records = _filter_results(filters)
    return jsonify(records)


def _filter_results(filters):
    records = app.db
    if 'name' in filters:
        records = [rec for rec in records if rec['name'] == filters['name']]
    if 'type' in filters:
        records = [rec for rec in records if rec['type'] == filters['type']]
    if 'age' in filters:
        records = [rec for rec in records if rec['age'] == filters['age']]
    if 'sex' in filters:
        records = [rec for rec in records if rec['sex'] == filters['sex']]
    if 'description' in filters:
        records = [rec for rec in records if rec['description'] == filters['description']]
    if 'owner_email' in filters:
        records = [rec for rec in records if rec['owner_email'] == filters['owner_email']]
    if 'image_url' in filters:
        records = [rec for rec in records if rec['image_url'] == filters['image_url']]

    return records


def _get_attributes(new_values, original_values):
    for key, value in new_values.items():
        original_values[key] = value

    return original_values


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)