## store translation task
## translation request and save it to the db

## run translation 
##run a pretrained deep learning model

##find_translation
##retrieve a translation from the db

from translation_model.model_translation import TranslationModel #from models.py import TranslationModel
from transformers import T5Tokenizer, AutoTokenizer, AutoModelForSeq2SeqLM,T5ForConditionalGeneration
#Tokenizer trasnsform text into numbers [for dl algo to process]
#T5ForConditionalGeneration generate translation based on those input numbers

# Use t5-base or t5-small for a smaller download size, t5-large for more accuracy
#tokenizer = T5Tokenizer.from_pretrained("t5-small", model_max_length=512) 
tokenizer = AutoTokenizer.from_pretrained("t5-small",model_max_length=512, legacy=False) #maximum length of an input to the tokenizer

#"t5-small" a dl model trained by google <<translate few different languages>>
#translator = T5ForConditionalGeneration.from_pretrained("t5-small")
translator = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

#from main.py taking in t an instance of the translation() class with our validated data
#storing validated data to the database
def store_translation(t):
    model = TranslationModel(text=t.text, base_lang=t.base_lang, final_lang=t.final_lang)
    model.save()
    return model.id #to reference our model; to run & query the translation

#run a pretrained dl model
#take in the database id model that will be translated
def run_translation(t_id: int):
    #return single translation request
    model = TranslationModel.get_by_id(t_id) #query the database for that certain unique id for each translation request

    #T5 works f"translate English to French: Hello world!"
    #change data to that T5 format
    prefix = f"translate {model.base_lang} to {model.final_lang}: {model.text}"
    #prefix will return a string with the full translation to be passed into t5

    #for tokenization-> split it up into sort of words then to numbers
    input_ids = tokenizer(prefix, return_tensors="pt").input_ids #getting input ids

    #outputs = translator.generate(input_ids, max_new_tokens=512)
    outputs = translator.generate(input_ids, max_new_tokens=512)
    #decode number outputs to string words
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True) #skip_special_tokens is skipping tokens that have been used internally by the model
    model.translation = translation
    model.save()

#find the translation
#retrieve the translation from the database
def find_translation(t_id: int):
    model = TranslationModel.get_by_id(t_id)
    translation = model.translation
    if translation is None:
        translation = "Processing, check back later!"
    return translation