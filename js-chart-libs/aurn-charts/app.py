from flask import Flask, render_template
import requests


app = Flask(__name__)

# TO DO - make interpolated values instead of '', multiple sites (e.g. MY1, NKENS)
    # 2 sites and multiple pollutants


def chart_data(pollutant, site, days):
    url = 'http://127.0.0.1:5000/data/{0}/{1}/{2}'.format(pollutant, site, start)
    # url = 'http://air-aware.com:8083/data/{0}/{1}/{2}'.format(pollutant, site, start)
    data = requests.get(url).json()
    times = [a['time'] for a in data['data']]
    values = ['' if a['value'] in ['n/a', 'n/m'] else int(a['value']) for a in data['data']]
    return [times, values]


@app.route('/<pollutant>/<site>/<int:days>')
def make_chart(pollutant, site, days, chartID='chart_ID', chart_type='line', chart_height=550,
               chart_width=800):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "width": chart_width}
    data = chart_data(pollutant, site, days)
    series = [{"name": 'gjh', "data": data[1]}]

    # CAN REMOVE NAME FROM SERIES??
    title = {"text": '{} levels at {}'.format(pollutant, site)}
    xAxis = {"title": {"text": 'Time (GMT)'}, "categories": [1,2,3,4]}
    # "categories": data[0]}
    yAxis = {"title": {"text": 'Concentration (ug/m-3)'}}
    return render_template('chart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis)


if __name__ == "__main__":
    app.run(host='127.0.0.2')