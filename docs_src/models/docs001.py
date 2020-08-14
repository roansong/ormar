import databases
import sqlalchemy

import orm

database = databases.Database("sqlite:///db.sqlite")
metadata = sqlalchemy.MetaData()


class Course(orm.Model):
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    name = orm.String(length=100)
    completed = orm.Boolean(default=False)