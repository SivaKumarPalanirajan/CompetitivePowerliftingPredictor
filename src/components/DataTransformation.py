from src.constants import CONFIG_PATH 
from src.utils.common import * 
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import LabelEncoder
import pickle
import numpy as np 
from ensure import ensure_annotations 
import pandas as pd 

class DataTransformation:
    def __init__(self):
        self.transformation_config=LoadYaml(CONFIG_PATH).transformation
    
    @ensure_annotations
    def Transform(self,data:pd.DataFrame):

        logger.info('------  Data Transformation Started  ------')
        os.makedirs(self.transformation_config.dir,exist_ok=True)
        
        TrainDataPath=os.path.join(self.transformation_config.dir,self.transformation_config.train_data_filename)
        TestDataPath=os.path.join(self.transformation_config.dir,self.transformation_config.test_data_filename)
        GenderEncoderPath=os.path.join(self.transformation_config.dir,self.transformation_config.gender_encoder_path)

        col_with_null=[col for col in  data.columns if  data[col].isna().sum()!=0 ]
        logger.info(f'{",".join(col_with_null)} -  Contains null values')
        for col in col_with_null:
            data[col]= data[col].fillna(0)
            logger.info(f'Replaced null values for {col}')

        if data[data.duplicated()].empty==False:
            data.drop_duplicates(inplace=True)
            logger.info(f'Dropped duplicates')
        else:
            logger.info('No duplicates found')

        lift_categories=['Squat1','Squat2','Squat3','Benchpress1','Benchpress2','Benchpress3','Deadlift1','Deadlift2','Deadlift3']
        for col in lift_categories:
            data[col]=np.where(data[col]<0,abs(data[col]),data[col])

        data['Age']=2026-data['YOB']
        logging.info("Created new features")

        data['Weight']=np.log(data['Weight'])
        logging.info("Convert the Weight feature to Normal distribution")

        outliers_present=['Weight','Deadlift1','Deadlift3']
        for col in outliers_present:  
            min_limit=data[col].mean()-3*data[col].std()    # as the data is fairly normal distributed 
            max_limit=data[col].mean()+3*data[col].std()    # as the data is fairly normal distributed 
            data=data[(data[col]<max_limit) & (data[col]>min_limit)]
            logging.info(f"Outliers removed for {col}")

        encoder_for_gender=LabelEncoder()
        data['Gender']=encoder_for_gender.fit_transform(data['Gender'])
        pickle.dump(encoder_for_gender,open(GenderEncoderPath,'wb'))
        logging.info('Gender encoder saved')

        data=data.drop(columns=["YOB","Lot","State","Points","Name"])

        train,test=train_test_split(data,test_size=0.2)

        train.to_csv(TrainDataPath,index=False)
        logging.info('Training Data stored')

        test.to_csv(TestDataPath,index=False)
        logging.info('Testing Data stored')

        logging.info('------  Data Transformation completed  ------')

        return train,test
        