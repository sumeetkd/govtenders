from flask import Flask, render_template, request
import src.sqlconnection
import json
app = Flask(__name__)
app.jinja_env.filters['zip'] = zip

sqlconnection = src.sqlconnection.connector
sqlquery = src.sqlconnection.sqlquery

def load_site_data():
    """Testing doc strings
    """
    tender_sites = 'src/collect_tenderinfo/tender_sites.json'
    with open(tender_sites, 'r') as jsonfile:
        tendersites_info = json.load(jsonfile)
        for item in tendersites_info:
            webdata = data_entry(item['name'])
            name = '<a href="'+ item['base'] + '">' + item['name'] + '</a>'
            yield name, webdata.load_latest()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/labequipment')
def lab_equipment():
    with sqlconnection() as connection:
        rows = sqlquery(connection).categorydata()
    return render_template('labequipment.html', result = rows)


@app.route('/search')
def search_form():
    """
    :return:
    """
    return render_template('search.html')

@app.route('/search_results', methods = ['POST'])
def search_results():
    if request.method == 'POST':
        querydict = request.form.to_dict()
        querydict['searchfor'] = '%' + querydict['searchfor'] + '%'
        print(querydict['searchfor'])
        with sqlconnection() as connection:
            rows = sqlquery(connection).searchquery(querydict)
    return render_template('results.html', result = rows)



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
