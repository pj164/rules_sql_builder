import inspect
import json

from sqlalchemy import create_engine
# -------------- Creating connection & session ---------------#
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import models

Base = declarative_base()
con_url = 'postgres://postgres@dev:5432/rules'
engine = create_engine(con_url, pool_recycle=3600)

# Set up the session
session_maker = sessionmaker(bind=engine, autoflush=True, autocommit=False, expire_on_commit=True)
session = scoped_session(session_maker)
session = scoped_session(session_maker)

from sqlalchemy_json_querybuilder.querybuilder.search import Search

def generate_sql(control):
    search = Search(session, 'models', (get_model(control['control_name']),), filter_by=control['rules'])
    query = search.query()
    return str(query.statement.compile(compile_kwargs={"literal_binds": True}))


def generate():
    control_sqls = {}
    with open('controls.json', mode='r') as controls_file:
        controls = json.load(controls_file)
        for control in controls:
            control_sqls[control['control_name']] = generate_sql(control)
    with open('control_sqls.json', 'w') as sqls_file:
        json.dump(control_sqls, sqls_file)


def get_model(class_name):
    for m in inspect.getmembers(models, inspect.isclass):
        if m[1].__module__ == 'models' and m[0] == class_name:
            return m[1]


generate()
