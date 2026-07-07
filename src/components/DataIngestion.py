from src.utils.common import * 
import pandas as pd 
from ensure import ensure_annotations 
from src.constants import CONFIG_PATH 

class DataIngestion:
    def __init__(self):
        self.IngestionConfig=LoadYaml(CONFIG_PATH).ingestion
    
    @ensure_annotations
    def Ingest(self)->pd.DataFrame|None:
        logger.info('------  Data Ingestion Started  ------')
        dirname=self.IngestionConfig.dir
        filename=self.IngestionConfig.raw_data_filename

        CompletePath=os.path.join(dirname,filename)
        dir,ext=os.path.splitext(CompletePath)
        if os.path.exists(CompletePath):
            if ext=='.csv':
                data=pd.read_csv(CompletePath)
                logging.info(f"Loaded {CompletePath}")
                logging.info(f"Data contains {data.shape[0]} rows and {data.shape[1]} columns")

            elif ext=='.xlsx':
                data=pd.read_excel(CompletePath)
                logging.info(f"Loaded {CompletePath}")
                logging.info(f"Data contains {data.shape[0]} rows and {data.shape[1]} columns")

            else:
                logging.error(f'Invalid file extension - {ext} - Expected .csv or .xlsx')
                data=None 
        else:
            logging.error(f"Filepath doesn't exist- {CompletePath}")
            data=None 

        logger.info('------  Data Ingestion Completed  ------')
        return data

        