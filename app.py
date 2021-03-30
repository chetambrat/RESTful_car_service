import logging

from flask_restful import Api

import create_app
from views import DealerManager, CarManager

app = create_app.create_app(debug=True)
api = Api(app)

api.add_resource(DealerManager, '/dealers')
api.add_resource(CarManager, '/cars')


if __name__ == '__main__':
    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5000, debug=True)
