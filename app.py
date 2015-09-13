import csv
import os
import gspread
import json
import datetime
from itertools import groupby
from flask import Flask
from flask import render_template
from oauth2client.client import SignedJwtAssertionCredentials

app = Flask(__name__)
<<<<<<< HEAD
json_key = json.load(open('secretkey.json'))
=======
json_key = json.load(open('homicides-0218b6fcdc87.json'))
>>>>>>> sa-express-news/master
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

gc = gspread.authorize(credentials)

output_csv = open("./static/master.csv","wb")
output = csv.writer(output_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

all_sheets = gc.open("CrimeTeamHomicideFinalDatabase_working")

sheet = all_sheets.worksheet("master")

raw_sheet = sheet.get_all_values()

for row in raw_sheet:
    new_row = list(map((lambda x: x.encode('ascii', 'ignore').replace('\n', ' ').replace('\r', '')), row))
    output.writerow(new_row)

output_csv.close()

csv_path = './static/master.csv'

csv_obj = csv.DictReader(open(csv_path, 'r'))
csv_list = list(csv_obj)


murders_by_year = {}
murders_by_year_grpd = {}

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

#@app.route('/sitemap.xml')
#def sitemap():
#    today = datetime.date.today().strftime("%Y-%m-%d") 

#    return render_template('sitemap.xml', 
#        object = murders_by_year_grpd,
#        current_date = today,
#        )



if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8007,
        use_reloader=True,
        debug=True,
    )