import streamlit as st
import numpy as np
import os 
import requests 
from dotenv import load_dotenv 

load_dotenv()
API_ENDPOINT=os.environ['API_ENDPOINT']

st.title("WELCOME TO THE COMPETITIVE POWERLIFTING PREDICTOR 💪💪")
st.info("""We can give a good estimate for the below lifts:
        \n1)Predict a good lift for 2nd attempt(Squat,Deadlift,Benchpress)
        \n2)Predict a good lift for 3rd attempt(Squat,Deadlift,Benchpress)""")

sidebar=st.sidebar
sidebar.title('Please provide the below values')

predict_option = sidebar.radio("Predict 2nd or 3rd lift?",["2nd lift","3rd lift"],index=None)
gender=sidebar.radio('Gender',['Male','Female'],index=None)

if gender and predict_option:
    gender={'Male':'M',"Female":'F'}.get(gender)
    weight=float(sidebar.number_input("Weight:",min_value=1))

    if predict_option=='2nd lift':
        attempt_no=2
    else:
        attempt_no=3

    if weight:
        type_of_lift=sidebar.radio('Squat or Benchpress or Deadlift?',['Squat','Benchpress','Deadlift'],index=None)
        if type_of_lift=='Squat':
            lift_type='squat'
        elif type_of_lift=='Benchpress':
            lift_type='bench'
        else:
            lift_type='deadlift'
        
        if predict_option=='2nd lift' and type_of_lift:
            lift1=sidebar.number_input(f"1st attempt {type_of_lift} weight:")
            payload={"lift_type":lift_type,
                     "attempt_no":attempt_no,
                     "lift1":lift1,
                     "gender":gender,
                     "weight":weight}
            response=requests.post(API_ENDPOINT,json=payload)
            status_code=response.status_code
            result=response.json()

            if status_code==200:
                st.subheader(f"Our model predicts {result['response']} kgs to be a good estimate")
            else:
                st.subheader(f"Error with Processing - {result['error']}")

        elif predict_option=='3rd lift' and type_of_lift:
            lift1=sidebar.number_input(f"1st attempt {type_of_lift} weight:")
            lift2=sidebar.number_input(f"2nd attempt {type_of_lift} weight:")
            payload={"lift_type":lift_type,
                     "attempt_no":attempt_no,
                     "lift1":lift1,
                     "gender":gender,
                     "weight":weight,
                     "lift2":lift2}
            response=requests.post(API_ENDPOINT,json=payload)
            status_code=response.status_code
            result=response.json()

            if status_code==200:
                st.subheader(f"Our model predicts {result['response']} kgs to be a good estimate")
            else:
                st.subheader(f"Error with Processing - {result['error']}")