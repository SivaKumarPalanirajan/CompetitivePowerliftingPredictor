import pandas as pd 
import mlflow
import numpy as np
import pickle
from sklearn.metrics import r2_score,mean_squared_error
import yaml 
from dotenv import load_dotenv
import os 
from src.utils.common import * 
from pathlib import Path 

load_dotenv()

class ModelEvaluation:
    def __init__(self):
        self.params=yaml.safe_load(open('params.yaml'))['evaluate']

    def evaluate(self,lift_no:str,lift_type:str,type_of_prediction:str,TEST_DATA:pd.DataFrame,model_path:str)->None:
        logger.info(f'Started Evaluation for {type_of_prediction}-{lift_type}-{lift_no}')
        if type_of_prediction=='Regression':
            if lift_type=='bench':
                if lift_no=='2':
                    x_test=TEST_DATA[['Gender','Weight','Benchpress1']]
                    y_test=TEST_DATA['Benchpress2']            

                else:
                    x_test=TEST_DATA[['Gender','Weight','Benchpress1','Benchpress2']]
                    y_test=TEST_DATA['Benchpress3']
                    
            elif lift_type=='squat':
                if lift_no=='2':

                    x_test=TEST_DATA[['Gender','Weight','Squat1']]
                    y_test=TEST_DATA['Squat2']
                else:

                    x_test=TEST_DATA[['Gender','Weight','Squat1','Squat2']]
                    y_test=TEST_DATA['Squat3']

            else:
                if lift_no=='2':
    
                    x_test=TEST_DATA[['Gender','Weight','Deadlift1']]
                    y_test=TEST_DATA['Deadlift2']
                else:
    
                    x_test=TEST_DATA[['Gender','Weight','Deadlift1','Deadlift2']]
                    y_test=TEST_DATA['Deadlift3']
                    
        else:
            logger.info("Invalid type of prediction")
            return 
        
        model=LoadModel(Path(model_path))

        y_pred=model.predict(x_test)

        r2=r2_score(y_test,y_pred)
        mse=mean_squared_error(y_test,y_pred)

        mlflow.log_metrics({'R2 Score':r2,'MSE':mse})

        logger.info(f'R2: {r2}')
        logger.info(f'MSE: {mse}')
        logger.info('Logged evaluation metrics of the model')  

    
    def StartEvaluation(self):
        logging.info('------  Model Evaluation Started  ------')

        TEST_DATA_PATH=self.params['test_path']
        MODEL_DIR=self.params['model_dir']
        bench2_model=self.params['bench2_model_path']
        bench3_model=self.params['bench3_model_path']
        deadlift2_model=self.params["deadlift2_model_path"]
        deadlift3_model=self.params["deadlift3_model_path"]
        squat2_model=self.params["squat2_model_path"]
        squat3_model=self.params["squat3_model_path"]
        experiment_no=self.params['experiment_no']

        mlflow.set_experiment(f'Model Evaluation {experiment_no}')

        type_of_prediction=['Regression']
        lift_types=['bench','squat','deadlift']
        lift_nos=['2','3']

        TEST_DATA=pd.read_csv(TEST_DATA_PATH)
        for type in type_of_prediction:
            for lift_type in lift_types:
                for lift_no in lift_nos:
                    with mlflow.start_run(run_name=f'Evaluation-{type}-{lift_type}-{lift_no}'):
                        MODEL_PATH=os.path.join(MODEL_DIR,self.params[f'{lift_type}{lift_no}_model_path'])
                        self.evaluate(lift_no,lift_type,type,TEST_DATA,MODEL_PATH)

        logging.info('------  Model Evaluation completed  ------')
