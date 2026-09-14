from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from models.predict import model,MODEL_VERSION,predict_output
from schema.predection_response import PredictionResponse



app = FastAPI()


@app.get('/') # For the human
def home():
    return { 
            'Message':'Insurance premium prediciton API'
        }
        
@app.get('/health') # For the machine (such as: AWS etc . . .)
def health_check(): 
    return { 
            'status':'OK!!', 
            'code':'200', 
            'version':MODEL_VERSION, 
            'mode_loaded': model is not None
        }


@app.post('/predict',response_model=PredictionResponse)
def predict_insurance_premium(data:UserInput):
    input_df = {
        'bmi':data.bmi,	
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'city_tier':data.city_tier,
        'income_lpa':data.income_lpa,	
        'occupation':data.occupation
    }
    
    try:
        
        predction = predict_output(input_df)
    
        return JSONResponse(status_code=200,content={
            'Message':'Model predict insurance successfully!!⭐', 
            'response':predction
        })
    except Exception as e: 
        return JSONResponse(status_code=500,content=str(e))