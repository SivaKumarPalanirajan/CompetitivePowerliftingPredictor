# Competitive Powerlifting Predictor <br>

## Overview <br>
Due to my background as a powerlifter, I designed this project with my domain knowledge.
It is able to accurately predict results such as weights for 2nd lift and 3rd lift along with experimentation for predicting if a lift would be successfully.<br>

Curated a dataset by web scraping using Selenium.<br>

The data had columns such as 'Name', 'Gender', 'YOB', 'State', 'Lot', 'Weight', 'Squat1', 'Squat2', 'Squat3', 'Benchpress1', 'Benchpress2', 'Benchpress3', 'Deadlift1', 'Deadlift2', 'Deadlift3','Total' and 'Points'. Additionally more features such as Age, status of various lifts were created during the feature engineering process.<br>

## Architecture
![Model Development Pipeline](assets/ModelDevelopmentPipeline.png)<br>

![Application Flow](assets/ApplicationFlow.png)<br>

## Tech Stack
&emsp;→ **Versioning**: DVC, Git and GitHub <br>
&emsp;→ **Experiment Tracking**: MLflow <br>
&emsp;→ **Deployment**: Docker <br>
&emsp;→ **Framework**: Streamlit and Flask 

## Deployment Ready
Dockerfiles **(Dockerfile.server and Dockerfile.streamlit)** have been created for the api and the Streamlit app.<br>
Both the services can be set up and used using the docker compose file **(docker-compose.yml)**. 

## Results
| Model | R2 Score | 
|----------|----------|
| Bench2   | 0.995   |
| Bench3   | 0.886   |
| Deadlift2   | 0.992  |
| Deadlift3   | 0.992  |
| Squat2   | 0.993   |
| Squat3   | 0.823   |


## EDA (Using Power BI)
![EDA Slide 1](EDA/EDA_1.png)<br>
![EDA Slide 2](EDA/EDA_2.png)<br>
![EDA Slide 3](EDA/EDA_3.png)

### FEW INSIGHTS FROM ANALYSIS

&emsp;→Maximum of Total weight lifted by Male participants are higher than Female participants <br>
&emsp;→Average of Total weight lifted by Male participants is 651.03 whereas Average of Total weight lifted by Female participants is 391.95 <br>
&emsp;→Number of Male participants is 537 and Number of Female participants is 519 <br>
&emsp;→Percentage of Participants who failed the first attempt of Benchpress is 5.21% whereas the Percentage of participants who didnt is 94.79% <br>
&emsp;→Number of Male participants who succeeded in the first attempt of Benchpress is 500 and Number of Female participants who 
succeeded in the first attempt of Benchpress is 501 <br>
&emsp;→The absolute value of Benchpress1 and absolute value of Benchpress3 tend to have a linear distribution with each other, signifying &the high positive correlation between the 1st and 3rd benchpress attempt <br>
&emsp;→Lifters in their late 20s and early 30s tend to lift the highest <br>
&emsp;→Male Lifters from California had the highest total weights lifted of 41.61k and Female Lifters from Texas had the highest total weights lifted of 22.80k <br>
&emsp;→In generally, the participants from California had the highest total weights lifted of 64.15k <br>
&emsp;→There seems to be a noticeable increase in the total weights lifted as the weight of the participant increases <br>
&emsp;→The Maximum of total weights lifted tends to increase as the age of the participant decreases but only to a certain limit <br>
&emsp;→The age of participants with highest successful deadlifts is 23 <br>
&emsp;→The absolute value of Deadlift1 and absolute value of Deadlift3 tend to have a linear distribution with each other, signifying the high positive correlation between the 1st and 3rd Deadlift attempt <br>
&emsp;→The age of participant with highest total weights lifted is 34 whereas The age of participant with lowest total weights lifted is 85 <br>
&emsp;→Percentage of Participants who failed the first attempt of Deadlift is 6.06% whereas the Percentage of participants who didnt is 93.94% <br>
&emsp;→Number of Male participants who succeeded in the first attempt of Deadlift is 511 and Number of Female participants who succeeded in the first attempt of Deadlift is 481 <br>
&emsp;→Percentage of Participants who failed the first attempt of Squat is 10.8% whereas the Percentage of participants who didnt is 89.2% <br>
&emsp;→Number of Male participants who succeeded in the first attempt of Squat is 476 and Number of Female participants who succeeded in the first attempt of Squat is 466 <br>
&emsp;→State with the highest number of successful deadlifts is California <br>
&emsp;→State with the highest number of participants is California <br>
&emsp;→State of the participant who has the highest total weights lifted is New Jersey <br>
&emsp;→The Average Weight of Male lifters and the Average Weight of Female lifters had a difference of 19.77 <br>
&emsp;→The Weight of the lifters was log normally distributed <br>
&emsp;→The distribution between Deadlift3 and Deadlift1 had X-shaped distribution. Similarly for Benchpress and Squat. <br>
&emsp;→The X-shaped distribution was due to the fact that there existed negative values for the lifts signifying the <br>failed lifts.<br>
&emsp;→The absolute value of Squat1 and absolute value of Squat3 tend to have a linear distribution with each other, signifying the high positive correlation between the 1st and 3rd Deadlift attempt <br>
&emsp;→The weight lifted by the participant with the highest total weights lifted is 355 Kgs for Squat attempt 1 <br>
&emsp;→The difference between the Average weight of Squat attempt 1 and weight lifted by participant with the highest total weights for Squat attempt 1 is 210.85 <br>