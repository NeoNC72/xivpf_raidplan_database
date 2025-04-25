from flask import Flask, render_template, g
import sqlite3
import os
from collections import defaultdict

DATABASE = 'raidplans.db'

app = Flask(__name__)
app.config['DATABASE'] = DATABASE

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT duty_name, url FROM raidplans ORDER BY duty_name")
    all_plans = cursor.fetchall()

    grouped_plans = defaultdict(list)
    for plan in all_plans:
        grouped_plans[plan['duty_name']].append(plan['url'])

    return render_template('index.html', grouped_plans=dict(grouped_plans))

if __name__ == '__main__':
    app.run(debug=True)
