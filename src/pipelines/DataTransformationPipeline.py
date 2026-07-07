from src.components.DataTransformation import DataTransformation 
from src.utils.common import * 
from src.pipelines.DataIngestionPipeline import DataIngestionPipeline 
from src.pipelines.DataValidationPipeline import DataValidationPipeline 
import pandas as pd 
from ensure import ensure_annotations 

class DataTransformationPipeline:
    def __init__(self):
        self.obj=DataTransformation()
    
    @ensure_annotations
    def StartDataTransformationPipeline(self,data:pd.DataFrame):
        train,test=self.obj.Transform(data)
        return train,test

if __name__=="__main__":
    obj1=DataIngestionPipeline()
    data=obj1.StartIngestionPipeline()

    obj2=DataValidationPipeline()
    ValidationStatus=obj2.StartValidationPipeline(data)

    if ValidationStatus:
        obj3=DataTransformationPipeline()
        train,test=obj3.StartDataTransformationPipeline(data)
    else:
        logger.info('Data Validation Failed so Pipeline stopped')

