from flask import Flask

from main.routes.route import Student

app = Flask(__name__)
app.register_blueprint(Student)
@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)