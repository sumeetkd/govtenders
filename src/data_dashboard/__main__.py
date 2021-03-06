from flask import Flask, render_template
import pandas as pd
from src.collect_tenderinfo.data import data_entry
import json
app = Flask(__name__)
app.jinja_env.filters['zip'] = zip

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

@app.route('/search/<term>')
def search_results(term):
    results = []
    names   = []
    for name, data in load_site_data():
        df = pd.DataFrame.from_dict(data)
        filtereddf = df[df['Title'].str.contains(term, case=False, regex=True)]
        site_results = filtereddf[
            ['Organisation Chain', 'Tender ID', 'Tender Type', 'Title', 'Work Description', 'Bid Submission End Date',
             'Tender Value in ₹ ', 'EMD Amount in ₹ ']].to_html()
        results.append(site_results)
        names.append(name)
    return render_template('results.html',results=results, namelist = names)

@app.route('/categories/<term>')
def product_category(term):
    results = []
    names   = []
    for name, data in load_site_data():
        df = pd.DataFrame.from_dict(data)
        filtereddf = df[df['Title'].str.contains(term, case=False, regex=True)]
        site_results = filtereddf[
            ['Organisation Chain', 'Tender ID', 'Tender Type', 'Title', 'Work Description', 'Bid Submission End Date',
             'Tender Value in ₹ ', 'EMD Amount in ₹ ']].to_html()
        results.append(site_results)
        names.append(name)
    return render_template('product_category.html',results=results, namelist = names)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
