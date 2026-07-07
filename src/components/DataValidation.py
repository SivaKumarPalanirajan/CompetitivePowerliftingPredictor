from src.utils.common import * 
from src.constants import SCHEMA_PATH
from ensure import ensure_annotations 
import pandas as pd 

class DataValidation:
    def __init__(self):
        self.schema=LoadYaml(SCHEMA_PATH).REQUIRED_COLS

    @ensure_annotations
    def Validate(self,data:pd.DataFrame)->bool:
        logger.info('------  Data Validation Started  ------')
        DataValidityStatus=True 
        
        if data is not None:
            for col,datatype in self.schema.items():
                if col in data.columns:
                    if data[col].dtype==datatype:
                        logger.info(f'Column {col} - Valid')
                        continue
                    else:
                        logger.error(f'Column {col} has datatype mismatch - Please rectify the data')
                        DataValidityStatus=False
                else:
                    DataValidityStatus=False
                    logger.error(f'Column {col} is not present in the data - Please rectify the data')

        else:
            DataValidityStatus=False
            logger.error('Data is not found so validation failed')
        
        if DataValidityStatus:
            logger.info('Data has been successfully validated')
        
        logger.info('------  Data Validation Completed  ------')
        return DataValidityStatus
            
        