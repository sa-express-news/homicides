from flask_frozen import Freezer
from app import app, murders_by_year_grpd
freezer = Freezer(app)


@freezer.register_generator
def year_index():
    for key, value in murders_by_year_grpd.iteritems():
         yield {'year':key}
         
@freezer.register_generator
def detail():
    for key, value in murders_by_year_grpd.iteritems():

        for key_a, value_a in murders_by_year_grpd[key].iteritems():
            yield { 'year': key, 'number': value_a['HomicideNbr'] }

if __name__ == '__main__':
    freezer.freeze()