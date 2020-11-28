from flask import Flask, request
from newspaper import Article
import tensorflow as tf
import numpy as np
from flask_cors import CORS

ml = 2500
model_path = 'model/V3/'

# load vocab
dict_vocab = []
try:
	with open(model_path + 'vocab.txt', 'r') as inf:
		for line in inf:
			dict_vocab.append(eval(line))
	vocab = dict_vocab[0]
	print(len(vocab))
except Exception:
	pass

# load model
f = open(model_path + "model.json", "r")
# print(f.read())
model = tf.keras.models.model_from_json(f.read())

# load weight
model.load_weights(model_path + "model.h5")

# preprocess
def getDomain(url):
	p1 = url.find('//') + 2
	p2 = url.find('/', p1)
	return url[p1:p2]

app = Flask(__name__)

def encoder(data):
	res = []
	for i in data:
		k = []
		for j in i.split():
			try:
				k.append(vocab[j])
			except Exception:
				k.append(0);
		res.append(k)
	return res

def pre_progress(data, max_len):
  	# res = np.empty(223, dtype=list)
  	# j = 0
	res = []
	for i in data:
		zeros = [0] * (max_len - len(i))
		res.append(zeros + i)
    # res[j] = zeros + i
    # j += 1
	return np.array(res)

# def RorF(domain, title, content, model):
# 	temp = domain + ' ' + title + ' ' + content
# 	target = pre_progress(encoder(temp), ml)
# 	res = model.predict(target)
# 	return res

def create_predict_data(ddata, tdata, cdata):
  res = []
  for i in range(len(ddata)):
    temp = ddata[i] + ' ' + tdata[i] + ' ' + cdata[i]
    res.append(temp)
  # print(res)
  return pre_progress(encoder(res), ml)

def RorF(domain, title, content, model):
  if type(domain) == list:
    target = create_predict_data(domain, title, content)
  else:
    temp = domain + ' ' + title + ' ' + content
    target = pre_progress(encoder(temp), ml)
  res = model.predict(target)
  return res

@app.route('/cn')
def predict():

	url_target = request.args.get('url')

	article = Article(url_target, language='vi')
	article.download()
	article.parse()
	# print(article.title)

	domain = [getDomain(url_target)]
	title = [article.title]
	content = [article.text]

	return str((RorF(domain, title, content, model))[0][0])
	# return str(RorF(domain, title, content, model))

if __name__ == '__main__':
	CORS(app)
	app.run(debug=True, port=5000)