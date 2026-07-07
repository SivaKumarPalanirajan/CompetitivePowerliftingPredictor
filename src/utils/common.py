from box import ConfigBox
from ensure import ensure_annotations 
import json 
import logging 
from logging import StreamHandler,FileHandler
from datetime import datetime 
import os 
import sys
from pathlib import Path
from yaml import safe_load 
from box.exceptions import BoxValueError 
import pickle 

def SetupLogger():
    """
    Setup logging
    """
    dirname='logs'
    filename=f"{str(datetime.now().strftime('%d-%m-%Y-%H-%M-%S'))}.log"
    complete_dir=os.path.join(dirname,filename)

    os.makedirs(dirname,exist_ok=True)
    logging.basicConfig(level=logging.INFO, 
                        format="[%(asctime)s] - %(levelname)s - %(module)s - %(lineno)d - %(message)s",
                        handlers=[StreamHandler(sys.stdout),FileHandler(complete_dir)])
    logger=logging.getLogger('CompetitivePowerliftingPredictor')
    return logger

logger=SetupLogger()

@ensure_annotations
def LoadYaml(filename:Path)->ConfigBox|None:
    try:
        with open(filename,'r') as f:
            data=safe_load(f)
            logger.info(f'Successfully loaded {filename}')
            return ConfigBox(data)
    except BoxValueError:
        logging.exception(f"{filename} is Empty")
    except Exception as e:
        logging.exception(f"Can't open {filename} - {e}")

@ensure_annotations
def LoadJson(filename:Path)->ConfigBox|None:
    try:
        with open(filename,'r') as f:
            data=json.load(f)
            logger.info(f'Successfully loaded {filename}')
            return ConfigBox(data)
    except BoxValueError:
        logging.exception(f"{filename} is Empty")
    except Exception as e:
        logging.exception(f"Can't open {filename} - {str(e)}")

@ensure_annotations
def CreateJson(filename:Path,data:dict)->None:
    try:
        os.makedirs(filename.parent,exist_ok=True)
        with open(filename,'w') as f:
            json.dump(data,f,indent=2)
        logger.info(f'Successfully saved {filename}')
    except Exception as e:
        logging.exception(str(e))

@ensure_annotations
def LoadModel(filename:Path):
    try:
        dirname,ext=os.path.splitext(filename)
        if ext in ['.pkl','.sav','.h5']:
            with open(filename,'rb') as f:
                model=pickle.load(f)
                logger.info(f'Successfully loaded {filename}')
                return model 
        else:
            logger.info(f'Invalid model extension - {ext} - Model was not loaded')
    except Exception as e:
        logging.exception(str(e))

def SaveModel(filename:Path,model):
    try:
        dirname,ext=os.path.splitext(filename)
        if ext in ['.pkl','.sav','.h5']:
            with open(filename,'wb') as f:
                pickle.dump(model,f)
                logger.info(f'Successfully saved {filename}')
                return model 
        else:
            logger.info(f'Invalid model extension - {ext} - Model was not saved')
    except Exception as e:
        logging.exception(str(e))

