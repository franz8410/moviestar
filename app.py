import os

from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('mongodb://franz8410:test@3.34.48.67/', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbmovie


# HTML
@app.route('/')
def home():
    return render_template('index.html')


# API
@app.route('/api/list', methods=['GET'])
def show_stars():
    stars = list(db.mystar.find({}, {'_id': False}).sort('like', -1))
    return jsonify({'result': 'success', 'msg': stars})


@app.route('/api/like', methods=['POST'])
def like_star():
    star_name = request.form['name']
    star = db.mystar.find_one({'name': star_name})
    next_like_count = star['like'] + 1;
    db.mystar.update_one({'name': star_name}, {'$set': {'like': next_like_count}})
    return jsonify({'result': 'success'})


@app.route('/api/notlike', methods=['POST'])
def not_like_star():
    star_name = request.form['name']
    star = db.mystar.find_one({'name': star_name})
    next_not_like_count = star['like'] - 1;
    db.mystar.update_one({'name': star_name}, {'$set': {'like': next_not_like_count}})
    return jsonify({'result': 'success'})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    star_name = request.form['name']
    db.mystar.delete_one({'name': star_name})
    return jsonify({'result': 'success'})


@app.route('/webhook', methods=['POST'])
def web_hook():
    web_hook_data = request.form
    print(web_hook_data)
    os.system('cd /home/ubuntu/moviestar && git pull')
    return jsonify({'result': 'success!!'})


# push 테스트용

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
