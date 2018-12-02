import os
import json
import requests

from flask_migrate import Migrate, MigrateCommand
from flask.cli import FlaskGroup

from app import create_app, db

app = create_app()

migrate = Migrate(app, db)
cli = FlaskGroup(app)
app.cli.add_command('db', MigrateCommand)
cli.load_dotenv = os.getenv('FLASK_LOAD_DOTENV', 'False')

data = json.dumps(dict(name='auth', port='8001'))
headers = {'Content-type': 'application/json'}
requests.post('http://localhost:5000/instance', headers=headers, data=data)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()
