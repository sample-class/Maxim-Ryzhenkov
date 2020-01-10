from flask import Flask, render_template
import json
import os

app = Flask(__name__)


def get_data(data_path):
    data_path = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], data_path))
    with open(data_path, 'rb') as f:
        data = json.load(f)
    return data


@app.route('/')
def main():
    tours = get_data('data/tours.json')
    return render_template('index.html', tours=tours)


@app.route('/direction/<departure>')
def direction(departure):
    tours = get_data('data/tours.json')
    departures = get_data('data/departures.json')

    tours = {k: v for k, v in tours.items() if v['departure'] == departure}

    prices = [tour['price'] for tour in tours.values()]
    nights = [tour['nights'] for tour in tours.values()]

    return render_template('direction.html', direction=departures[departure],
                           prices=prices, nights=nights, tours=tours)


@app.route('/tour/<tour_id>')
def tour(tour_id):
    tour = get_data('data/tours.json')[tour_id]
    departure = get_data('data/departures.json')[tour['departure']]

    return render_template('tour.html', tour=tour, departure=departure)


@app.errorhandler(404)
def not_found(e):
    return render_template('page404.html')


@app.errorhandler(500)
def server_error(e):
    return render_template('page500.html')


if __name__ == '__main__':
    app.run()
