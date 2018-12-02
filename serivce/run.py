import requests
import json

from flask.cli import FlaskGroup
from flask import jsonify
from serivce.app import create_app

app = create_app()


data = json.dumps(dict(name='service', port='8000'))
headers = {'Content-type': 'application/json'}
requests.post('http://localhost:5000/instance', headers=headers, data=data)

cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
