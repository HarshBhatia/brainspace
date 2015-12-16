from flask import Flask, render_template, request, session
import random
import sqlite3
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
conn = sqlite3.connect('high_scores4.db',check_same_thread=False)
c = conn.cursor()

with open("commonwords.txt") as word_file:
	english_words = list(set(word.strip().lower() for word in word_file))


@app.route('/')
def index():
	session['score'] = 0
	return render_template("index.html",jword =	shuffle(random.choice(english_words)))

def shuffle(word):
	shuffled = ''.join(random.sample(word, len(word)))
	return shuffled

@app.route('/data_post', methods=['POST','GET'])
def data_post():
	answer = request.form['answer'].lower()
	jword = request.form['jword']
	if (answer in english_words) and (len(answer)==len(jword)) and (set(jword)==set(answer)):
		data = {"correct":True,"score":incr_score(),"jword":generate_word()}
		return json.dumps(data)
	else:
		data = {"correct":False,"page":render_template("final.html",score=session['score'])}
		return json.dumps(data)
@app.route('/score_post', methods=['POST','GET'])
def score_post():
	if request.method == 'GET':
		return get_high_scores()
	name = request.form['name']
	score = int(request.form['score'])

	insert_high_score(name, score)
	return get_high_scores()


def incr_score():
	session['score'] += 10
	return session['score']

def generate_word():
	return shuffle(random.choice(english_words))

def insert_high_score(name,score):
	c.execute("""INSERT INTO SCORES(name,score) VALUES('{}',{})""".format(name,score))
	conn.commit()

def get_high_scores():
	l = []																																																																																																																																																																																																																																																																																																																																																																																																									
	for i in c.execute("""SELECT * FROM SCORES ORDER BY score DESC LIMIT 10"""):
		l.append(i)
	return render_template("score_table.html",scores = l)
	# return l


def high_scores_init():
	c.execute('''CREATE TABLE SCORES(name CHAR(200),score INT)''')
	print "Init Succesful!"
	# c.close()

if __name__ == "__main__":
	app.debug = True
	# insert_high_score('Harsh Bhatia', 50)
	# get_high_scores()
	app.run(host='0.0.0.0',port=5000)
