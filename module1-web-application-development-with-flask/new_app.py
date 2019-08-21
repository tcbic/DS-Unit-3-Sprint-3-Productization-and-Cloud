from flask import Flask, render_template   #instance of the class

app = Flask(__name__)   #create an instance of Flask

@app.route('/')   #web page (endpoint- this is where our data will go)
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

"""Instead of having to run from the command line, 
we create this conditional."""
if __name__ == '__main__':
    app.run(debug=True, port=5000)
