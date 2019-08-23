from flask import Flask, render_template

app = Flask(__name__)  

"""This is our home page."""
@app.route('/') 
def home():
    return render_template('home.html')

"""This is our about page."""
@app.route('/about')
def about():
    return render_template('about.html')

"""Instead of having to run from the command line, 
we create this conditional."""
if __name__ == '__main__':
    app.run(debug=True, port=5000)
