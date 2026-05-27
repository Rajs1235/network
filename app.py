import os
import sys
import certifi
from io import BytesIO

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
ce=certifi.where()
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
mongo_db_url=os.getenv("MONGO_DB_URL")
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request,HTTPException,BackgroundTasks
from uvicorn import run as app_run
from fastapi.responses import RedirectResponse, Response
from starlette.responses import JSONResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_obj
client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ce)
from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_DIR_NAME, TARGET_COLUMN
database=client[DATA_INGESTION_DATABASE_DIR_NAME]

app=FastAPI()
origins = ["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
template=Jinja2Templates(directory="./templates")


@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

def run_training_pipeline():
    train_pipeline=TrainPipeline()
    train_pipeline.initiate_training_pipeline()


@app.get("/train")
async def train_route(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(run_training_pipeline)
        return Response("Training started")
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        df=pd.read_csv(BytesIO(contents))
        df = df.drop(columns=[TARGET_COLUMN, "url"], errors="ignore")
        preprocessor=load_obj("final_model/preprocessor.pkl")
        final_model=load_obj("final_model/model.pkl")
        network_model=NetworkModel(preprocessor=preprocessor,model=final_model)
        y_pred=network_model.predict(df)
        df['predicted_label']=y_pred
        df.to_csv("prediction_Data/output.csv",index=False)
        table_html=df.to_html()
        return template.TemplateResponse("table.html",{"request":request,"table":table_html})
    except HTTPException:
        raise
    except Exception as e:
        raise NetworkSecurityException(e,sys)


if __name__=="__main__":
    app_run(app, host="localhost", port=8000)
