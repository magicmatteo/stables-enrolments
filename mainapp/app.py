from flask import Flask, render_template
app = Flask(__name__)

dogs = [
    {   'name': 'Winnie',
        'colour': 'Brown',
        'age': 2
    },
    {
        'name': 'Archie',
        'colour': 'cream',
        'age': 3
    }
]

@app.route('/')
def home():
    return render_template('home.html', dogs=dogs)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True)