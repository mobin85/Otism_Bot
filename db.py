from peewee import SqliteDatabase, Model, CharField, IntegerField

db = SqliteDatabase('db.sqlite3')


class BaseModel(Model):
    class Meta:
        database = db


class Video(BaseModel):
    text = CharField()
    video_path = CharField()


class Admin(BaseModel):
    password = CharField()


class IsAdmin(BaseModel):
    user_id = CharField()


class Question(BaseModel):
    answer = IntegerField()
    question = CharField()
    answer_1 = CharField()
    answer_2 = CharField()
    answer_3 = CharField()
    answer_4 = CharField()


db.connect()
if __name__ == '__main__':
    db.create_tables([Video, Admin, IsAdmin, Question])
