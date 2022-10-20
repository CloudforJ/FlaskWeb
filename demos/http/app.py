import os

from flask import Flask, request, redirect, url_for, abort, make_response, json, jsonify, session

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')



colors = ['blue', 'red', 'white']

@app.route('/colors/<any(%s):color>' % str(colors)[1:-1])
def three_colors(color):
    return '<p>Love is ....</p>'

@app.route('/404')
def not_found():
    abort(404)

@app.route('/goback/<int:year>')
def go_back(year):
    return 'Welcome to year %d' % year
@app.route('/hi')
def hi():
    return redirect(url_for('hello'))

@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name == None:
      name = request.cookies.get('name', 'Human')
    # name = request.args.get('name', 'Flask')
    response = '<h1>Hello, %s</h1>' % name
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response

@app.route('/foo')
def foo():
    response = make_response("Hello world")
    response.mimetype = 'text/plain'
    return response

@app.route('/foo_json')
def foo_json():
    data = {
        'name': 'zhangsan',
        'gender': 'male'
    }
    response = make_response(json.dumps(data))
    response.mimetype = 'application/json'
    return response

@app.route('/foo_jsonify')
def foo_jsonify():
    return jsonify(name = 'zhangsan', age = 15)

@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response

@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))


@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    else:
        return 'welcome to admin homepage'

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))

if __name__ == '__main__':
    app.run()
