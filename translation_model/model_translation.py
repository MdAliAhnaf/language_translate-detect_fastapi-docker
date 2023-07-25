#interact with database & creating a sqlitedatabase to store data
from peewee import Model, SqliteDatabase, CharField, TextField
# create SqliteDatabase for the right tables
# CharField, TextField two field types; store data to the db

# peewee is a object relational mapper & enables to interact with a database more easily; rather than writing raw sql

db = SqliteDatabase('translations.db')

#TranslationModel class inherits from model
class TranslationModel(Model): #TranslationModel class define a db table and the columns in that table
   
    text = TextField() #text column; text to translate
    base_lang = CharField() #base language; translate from
    final_lang = CharField() #translate to
    #client fields
    
    translation = TextField(null=True) #the translation
    #creation of first db record translation will be empty; will be generated later 
    #generate this in the backend

    class Meta: # use db, database to store this model
        database = db

#create table because it doesnt exist & passing the name of the table TranslationModel; which will be created
db.create_tables([TranslationModel])