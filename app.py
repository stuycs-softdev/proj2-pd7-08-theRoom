from flask import Flask
from flask import request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == "GET":
		return render_template('home.html')

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
