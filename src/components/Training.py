import pandas as pd 
import mlflow
import numpy as np
import pickle
from sklearn.ensemble import GradientBoostingRegressor
import optuna 
from sklearn.metrics import r2_score,mean_squared_error
from src.utils.common import *
import yaml 
from mlflow.models import infer_signature
from dotenv import load_dotenv
import os 
from pathlib import Path 

load_dotenv()

class ModelTraining:
    def __init__(self):
        self.params=yaml.safe_load(open('params.yaml'))['train']
    
    def training(self,lift_no:str,lift_type:str,type_of_prediction:str,TRAIN_DATA:pd.DataFrame,TEST_DATA:pd.DataFrame,model_path:str,hps:dict)->None:

        logger.info(f'Started training for {type_of_prediction}-{lift_type}-{lift_no}')
        if type_of_prediction=='Regression':
            if lift_type=='bench':
                if lift_no=='2':
                    x=TRAIN_DATA[['Gender','Weight','Benchpress1']]
                    y=TRAIN_DATA['Benchpress2']

                    x_test=TEST_DATA[['Gender','Weight','Benchpress1']]
                    y_test=TEST_DATA['Benchpress2']            

                else:
                    x=TRAIN_DATA[['Gender','Weight','Benchpress1','Benchpress2']]
                    y=TRAIN_DATA['Benchpress3']

                    x_test=TEST_DATA[['Gender','Weight','Benchpress1','Benchpress2']]
                    y_test=TEST_DATA['Benchpress3']
                    
            elif lift_type=='squat':
                if lift_no=='2':
                    x=TRAIN_DATA[['Gender','Weight','Squat1']]
                    y=TRAIN_DATA['Squat2']

                    x_test=TEST_DATA[['Gender','Weight','Squat1']]
                    y_test=TEST_DATA['Squat2']
                else:
                    x=TRAIN_DATA[['Gender','Weight','Squat1','Squat2']]
                    y=TRAIN_DATA['Squat3']

                    x_test=TEST_DATA[['Gender','Weight','Squat1','Squat2']]
                    y_test=TEST_DATA['Squat3']

            else:
                if lift_no=='2':
                    x=TRAIN_DATA[['Gender','Weight','Deadlift1']]
                    y=TRAIN_DATA['Deadlift2']

                    x_test=TEST_DATA[['Gender','Weight','Deadlift1']]
                    y_test=TEST_DATA['Deadlift2']
                else:
                    x=TRAIN_DATA[['Gender','Weight','Deadlift1','Deadlift2']]
                    y=TRAIN_DATA['Deadlift3']

                    x_test=TEST_DATA[['Gender','Weight','Deadlift1','Deadlift2']]
                    y_test=TEST_DATA['Deadlift3']
                    
        else:
            logger.info("Invalid type of prediction")
            return 
        

        def objective(trial):
            loss_hps=hps['loss']
            estimators_hps=hps['n_estimators']
            learning_rate_hps=hps['learning_rate']
            min_samples_leaf_hps=hps['min_samples_leaf']
            max_depth_hps=hps['max_depth']


            hp_space={
                'loss':trial.suggest_categorical('loss',loss_hps),
            "learning_rate":trial.suggest_categorical("learning_rate",learning_rate_hps),
            "n_estimators":trial.suggest_categorical('n_estimators',estimators_hps),
            "max_depth":trial.suggest_categorical('max_depth',max_depth_hps),
            "min_samples_leaf":trial.suggest_categorical('min_samples_leaf',min_samples_leaf_hps)
            }

            regression_model=GradientBoostingRegressor(**hp_space)
            regression_model.fit(x,y)
            y_pred=regression_model.predict(x_test)

            # if trial.should_prune():  # Not required as the number of trials is less
            #     raise optuna.TrialPruned()

            return r2_score(y_test,y_pred)
        
        hp_tuning=optuna.create_study(direction='maximize',pruner=optuna.pruners.MedianPruner())
        hp_tuning.optimize(objective,n_trials=35)
        logger.info('Completed HP Tuning')

        all_trials=hp_tuning.trials

        for i,trial in enumerate(all_trials):
            with mlflow.start_run(run_name=f'HP_Tuning_Trial-{i}',nested=True):
                mlflow.log_params(trial.params)
                mlflow.log_metric('R2-Score',trial.value)
        
        best_params=hp_tuning.best_params
        mlflow.log_params(best_params)

        best_model=GradientBoostingRegressor(**best_params)

        best_model.fit(x,y)
        logger.info('Trained the model with best HPs')

        training_score=best_model.score(x,y)

        y_pred=best_model.predict(x_test)

        r2=r2_score(y_test,y_pred)
        mse=mean_squared_error(y_test,y_pred)

        mlflow.log_metrics({'Training Score':training_score,'R2 Score':r2,'MSE':mse})

        logger.info(f'Training Score: {training_score}')
        logger.info(f'R2: {r2}')
        logger.info(f'MSE: {mse}')
        logger.info('Logged performance metrics of the best performing model')

        signature=infer_signature(x,y)

        if round(r2*100,0)>=90:
            mlflow.sklearn.log_model(best_model,
                                    artifact_path=f'{type_of_prediction}-{lift_type}-{lift_no}',
                                    signature=signature,
                                    input_example=x,
                                    registered_model_name=f'{type_of_prediction}-{lift_type}-{lift_no}')
            logger.info(f'Logged and registered best model for {type_of_prediction}-{lift_type}-{lift_no}')

        else:
            mlflow.sklearn.log_model(best_model,
                                    artifact_path=f'{type_of_prediction}-{lift_type}-{lift_no}',
                                    signature=signature,
                                    input_example=x)
            
            logger.info(f'Logged best model for {type_of_prediction}-{lift_type}-{lift_no}')
            logger.info('Model performance does not meet the required threshold so model is not registered')


        SaveModel(Path(model_path),best_model)
        logger.info(f'Best model for {type_of_prediction}-{lift_type}-{lift_no} has been saved locally')
        return


    def StartTraining(self):

        logging.info('------  Model Training Started  ------')

        DIRNAME=self.params['dir']
        TRAIN_PATH=self.params['train_path']
        TEST_PATH=self.params['test_path']
        bench2_model=self.params['bench2_model_path']
        bench3_model=self.params['bench3_model_path']
        deadlift2_model=self.params["deadlift2_model_path"]
        deadlift3_model=self.params["deadlift3_model_path"]
        squat2_model=self.params["squat2_model_path"]
        squat3_model=self.params["squat3_model_path"]
        experiment_no=self.params['experiment_no']

        os.makedirs(DIRNAME,exist_ok=True)
        mlflow.set_experiment(f'Model Training {experiment_no}')

        type_of_prediction=['Regression']
        lift_types=['bench','squat','deadlift']
        lift_nos=['2','3']
        
        TRAIN_DATA=pd.read_csv(TRAIN_PATH)
        TEST_DATA=pd.read_csv(TEST_PATH)
        for type in type_of_prediction:
            for lift_type in lift_types:
                for lift_no in lift_nos:
                    with mlflow.start_run(run_name=f'{type}-{lift_type}-{lift_no}'):
                        if type=='Regression':
                            hps_from_params_file=self.params['regression_hp']
                        else:
                            hps_from_params_file=self.params['classification_hp']

                        MODEL_PATH=os.path.join(DIRNAME,self.params[f'{lift_type}{lift_no}_model_path'])
                        self.training(lift_no,lift_type,type,TRAIN_DATA,TEST_DATA,MODEL_PATH,hps_from_params_file)

        logging.info('------  Model Training completed  ------')



