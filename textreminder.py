import json
from conversion import convert
from flask import Flask, redirect, render_template, request, url_for
from messaging import send_message


app = Flask(__name__)


@app.route('/')
def main():
    with open('gateways.json') as f:
        gateways = json.load(f)
    return render_template('index.html',
                           entries=sorted(gateways.keys()))


@app.route('/task', methods=['POST'])
def register_task():
    form = request.form
    target = convert(form['number'], form['carrier'])
    send_message(form['message'], target)
    return redirect(url_for('main'))
