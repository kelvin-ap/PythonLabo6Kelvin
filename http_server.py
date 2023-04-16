# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/')

# def index():
#     with app.app_context():
#         return render_template('index.html')

# if __name__ == '__main__':
#     app.run()
from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return 'Hello world'
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')