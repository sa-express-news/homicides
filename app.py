import csv
from itertools import groupby
from flask import Flask
from flask import render_template

app = Flask(__name__)

csv_path = './static/07-08-test.csv'
#csv_path = './static/test.csv'
csv_obj = csv.DictReader(open(csv_path, 'r'))
csv_list = list(csv_obj)

murders_by_year = {}
murders_by_year_grpd = {}
# murder_list = []

for key, group in groupby(csv_list, lambda t: t['app_year']):
    murders_by_year[key] = list(group)

for key, value in murders_by_year.iteritems():
    murders_by_year_grpd[key] = dict([[o['HomicideNbr'],o] for o in value])

@app.route("/")
def index():
    return render_template('index.html',
        object_list = csv_list,
    )
    
@app.route('/<year>/')
def year_index(year):
    murder_list = []  

    for key, value in murders_by_year_grpd[year].iteritems():
        murder_list.append(value)
        murder_list  

    return render_template('year_index.html', 
        object_list = murder_list,
        )


@app.route('/<year>/<number>/')
def detail(year, number):
    return render_template('detail.html',
        object = murders_by_year_grpd[year][number],
    )


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8000,
        use_reloader=True,
        debug=True,
    )