from flask import Flask

app = Flask(__name__)

@app.route('/') #This is our webpage (endpoint).
def hello_world():
    return 'Hello World!'

#This conditional replaces having to run a command in the command line.
if __name__ == '__main__':
    app.run()
    