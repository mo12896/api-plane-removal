from flask import Flask
from flask_restful import Api

from resources import PointCloud

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'mo'
api = Api(app)

api.add_resource(PointCloud, '/pointcloud/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)  
