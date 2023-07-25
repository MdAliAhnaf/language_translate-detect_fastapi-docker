#this file routes for web server
from fastapi import FastAPI, BackgroundTasks
#FastAPI to create web-server
#BackgroundTasks to run the translation in the Background
from pydantic import BaseModel, validator
#pydantic to validate the data;input to api
import task_backend
from detection_model.model_detect import predict_pipeline
from detection_model.model_detect import __version__ as model_version

app = FastAPI() #initialize fastapi web-application by creating the app instance of FastAPI class 

class TextIn(BaseModel):
    text: str
    
class PredictionOut(BaseModel):
    language: str
   
#route:1 /
#test if everything working
@app.get("/")
def home():
    return {"health_check": "OK", "model_version of pkl file": model_version}

#route:4/ detect the language
@app.post("/predict", response_model=PredictionOut)
async def predict(payload: TextIn):
    language = predict_pipeline(payload.text)
    return {"language": language}

# with open("lang.txt") as f:
#      languages = f.read().split(", ")
languages = ["English", "French", "Romanian", "German"]
class Translation(BaseModel):
    text: str
    base_lang: str
    final_lang: str

    @validator('base_lang', 'final_lang')
    def valid_lang(cls, lang):
        if lang not in languages:
            raise ValueError("Invalid language")
        return lang

#route:2 /translate
#not going to do translation immediatly in the request
#long translation take a while to process can cause initial web request to time-out
#hence take in a translation request, & store it in the database and return the id of the db model
#in backend run the translation and update it
#return a translation id
#hence the client can query the database using another route to see if the translation is done or not

@app.post("/translate")
#take in t variable corresponding to Translation() model & background_tasks(run translation in bg)
#background_tasks: BackgroundTasks return to the client an ID corresponding to the db entry their translation req
#& be able to queue for processing that translation in bg 
#if translation within the web request is performed; long translation will cause errors
def post_translation(t: Translation, background_tasks: BackgroundTasks):
    #store the translation from task_backend py file -> store_translation function
    t_id = task_backend.store_translation(t)
    #run translation in bg from task_backend py file -> run_translation function
    background_tasks.add_task(task_backend.run_translation, t_id)
    return {"Task_id": t_id} #immediatley return the t_id the client making the request

#route:3 /results
# take in a translation id
# return the translated text
@app.get("/results")
def get_translation(t_id: int):
    return {"Translation": task_backend.find_translation(t_id)}