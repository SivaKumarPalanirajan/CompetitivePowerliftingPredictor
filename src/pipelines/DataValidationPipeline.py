from src.components.DataValidation import DataValidation 
from src.utils.common import * 
from ensure import ensure_annotations 
import pandas as pd 
from src.pipelines.DataIngestionPipeline import DataIngestionPipeline

class DataValidationPipeline:
    def __init__(self):
        self.obj=DataValidation()
    
    @ensure_annotations
    def StartValidationPipeline(self,data:pd.DataFrame)->bool:
        ValidationStatus=self.obj.Validate(data)
        return ValidationStatus