from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")
# print(cloud_sql_connection_name)
# cloud_sql_proxy 
# run this on the terminal to open the proxy: ./cloud_sql_proxy -instances=tensorflowdeployment:asia-southeast1:student-tracking=tcp:5432 &
# print(f'postgresql+psycopg2://{db_user}:{db_pass}@localhost:5432/')

# cloud_sql_address on App Engine 
# print(f'postgres+pg8000://{db_user}:{db_pass}@/{db_name}?unix_sock=/cloudsql/{cloud_sql_connection_name}/.s.PGSQL.5432')
# 'sqlite:///site.db'
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_user}:{db_pass}@localhost:5432/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'somekey'
db = SQLAlchemy(app)

from cs_student import routes