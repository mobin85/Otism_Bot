from peewee import SqliteDatabase, Model, CharField

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


# class Question(BaseModel):
#     answers_num = IntegerField()
#     answer = IntegerField()
#     question = CharField()


db.connect()
if __name__ == '__main__':
    db.create_tables([Video, Admin, IsAdmin])
