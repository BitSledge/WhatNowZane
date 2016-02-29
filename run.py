#!/usr/bin/env python
from flask import Flask, request, make_response
from mysql import connector
import md5
import base64

app = Flask(__name__)


KEY = "SupHacker??"
DB = {
    'user': 'haypp_hxar',
    'password': 'dtIwRdKa0T22zoPngQyl7Cf5gcgYPC',
    'host': 'localhost',
    'database': 'oroneisone'
}


def get_users():
    cnx = connector.connect(**DB)
    sql = cnx.cursor()

    _ret = []

    try:
        sql.execute(
            "SELECT id, Username FROM users WHERE id != 1;"
        )

        for _id, _name in sql:
            yield _id, _name

    except:
        return

    finally:
        if cnx:
            cnx.close()


def get_user(i):
    cnx = connector.connect(**DB)
    sql = cnx.cursor()

    _ret = []

    try:
        _sql = "SELECT Username, Password FROM users WHERE id != 1 AND id = {};".format(i)
        print _sql
        sql.execute(_sql)

        for _name, _pass in sql:
            yield _name, _pass

    except:
        return

    finally:
        if cnx:
            cnx.close()


def make_page(title, body):
    return make_response("""
    <html>
        <head>
            <style>
                label {{ width: 80px; display: inline-block; }}
                input {{ width: 120px; display: inline-block }}
                .error {{ color: darkred; }}
            </style>
        </head>
        <body>
            <h1>{0}</h1>
            <div>{1}</div>
        </body>
    </html>
    """.format(title, body))


@app.route('/', methods=['GET'])
def a():
    _table = []

    for _id, _name in get_users():
        _table.append("<tr><td><a href='/user?id={}'>{}<a></td></td>".format(_id, _name))

    return make_page(
        "Please select a user",
        "<table>{}</table>".format("".join(_table))
    )

@app.route('/user', methods=['GET'])
def b():
    try:
        _id = request.args['id']
        _cookie_id = request.cookies.get('id')
        _cookie_checksum = request.cookies.get('cs')

        if _id != '2' and _id != '3' and _id != '4' and _id != '5':
            if _cookie_id is None:
                raise

            if _cookie_checksum is None:
                raise

            if base64.b64decode(_cookie_id) != _id:
                raise

            if md5.new(_cookie_id).hexdigest() != _cookie_checksum:
                raise

    except:
        return make_page(
            "What are you trying to pull?",
            "Go back and click on a user. That will do the trick."
        )

    _table = []

    _the_name = ''
    for _name, _pass in get_user(_id):
        _the_name = _name
        _table.append("<tr><td>Password:</td><td>{}</td></td>".format(_pass))

    _resp = make_page(
        _the_name,
        "<table>{}</table>".format("".join(_table))
    )

    _cookie_id = base64.encodestring(_id).rstrip()
    _cookie_checksum = md5.new(_cookie_id).hexdigest()
    _resp.set_cookie('id', value=_cookie_id)
    _resp.set_cookie('cs', value=_cookie_checksum)

    return _resp


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
