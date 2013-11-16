from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
	return '<h3> Welcome to City 17! </h3>'

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
