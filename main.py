from src.pipelines.DataTransformationPipeline import DataTransformationPipeline 
from src.pipelines.TrainingPipeline import ModelTraining
from src.utils.common import * 
from src.pipelines.DataIngestionPipeline import DataIngestionPipeline 
from src.pipelines.DataValidationPipeline import DataValidationPipeline 
import pandas as pd 
from src.components.Training import ModelTraining

if __name__=='__main__':
  
    obj1=DataIngestionPipeline()
    data=obj1.StartIngestionPipeline()

    obj2=DataValidationPipeline()
    ValidationStatus=obj2.StartValidationPipeline(data)

    if ValidationStatus:
        obj3=DataTransformationPipeline()
        train,test=obj3.StartDataTransformationPipeline(data)
        obj4=ModelTraining()
        obj4.StartTraining()

    else:
        logger.info('Data Validation Failed so Pipeline stopped')