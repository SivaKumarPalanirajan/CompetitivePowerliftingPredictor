from src.components.DataIngestion import DataIngestion 
from src.utils.common import * 
from ensure import ensure_annotations 

class DataIngestionPipeline:
    def __init__(self):
        self.obj=DataIngestion()
    
    @ensure_annotations
    def StartIngestionPipeline(self):
        data=self.obj.Ingest()
        return data