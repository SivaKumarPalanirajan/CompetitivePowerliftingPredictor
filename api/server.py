from flask import Flask,request,jsonify
import pickle 
import numpy as np
import logging 

app= Flask(__name__)

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(lineno)d - %(message)s')

@app.route('/')
def home():
    return jsonify({'AppName':'CompetitivePowerliftingPredictor',
                    'Description': 'Predict 2nd / 3rd lift of powerlifting exercises - Deadlift, squat and benchpress',
                    'Version':'v2',
                    'Endpoints':[
                        '/health',
                        '/predict'
                    ],
                    "Status":"running"}),200

@app.route('/health')
def health():
    try:
        GenderEncoder=pickle.load(open('artifacts_inferencing/gender_encoder.pkl','rb'))
        logging.info('Encoder was accessed successfully')
        return jsonify({'response':'healthy'}),200
    except:
        return jsonify({'response':'unhealthy'}),503


@app.route('/predict',methods=['POST'])
def predict():
    logging.info(f'Prediction request received')
    data=request.get_json()
    lift_type=data.get('lift_type')
    attempt_no=data.get('attempt_no')
    filename=lift_type+str(attempt_no)+'_'+'predictor'+'.pkl'
    model=pickle.load(open(f'artifacts_inferencing/{filename}','rb'))
    GenderEncoder=pickle.load(open('artifacts_inferencing/gender_encoder.pkl','rb'))
    
    logging.info(f'{filename} was loaded')
    logging.info(f'Encoder was loaded')

    lift1_value=data.get('lift1')
    gender=data.get('gender')
    weight=data.get('weight')

    weight_transformed=np.log(float(weight))
    gender_encoded=GenderEncoder.transform([gender])[0]
    if attempt_no==2:
        try:
            predicted_value=model.predict([[gender_encoded,weight_transformed,lift1_value]])[0]
        except Exception as e:
            logging.exception(str(e))
            return jsonify({'error':f"Inferencing Stage: {str(e)}"}),500
        
    elif attempt_no==3:
        lift2_value=data.get('lift2')
        try:
            predicted_value=model.predict([[gender_encoded,weight_transformed,lift1_value,lift2_value]])[0]
        except Exception as e:
            logging.exception(str(e))
            return jsonify({'error':f"Inferencing Stage: {str(e)}"}),500

    else:
        logging.error(f"Valid attempt number wasn't provided - {attempt_no}")
        return jsonify({'error':'Incorrect parameters - provided attempt number not valid'}),400
    
    return jsonify({'response':round(predicted_value,2)})

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": str(e)}), 500
    
if __name__=='__main__':
    app.run(host='0.0.0.0',port=7860)