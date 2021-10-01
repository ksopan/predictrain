#Import Modules
# source ../../weather_predict/bin/activate
import flask
from flask import request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import joblib
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import plotly


#Define Flask App Environment
app = flask.Flask(__name__)
CORS(app)

#@app.route('/')
#def main():    
#  return render_template('index.html')

@app.route('/app.js')
def js():
    return render_template('app.js')

@app.route('/')
def plotchart():
    df2=pd.read_csv("./daily.csv")
    fig = make_subplots(rows=2, cols=2,horizontal_spacing = 0.1,
                    specs=[[{"secondary_y": True}, {"secondary_y": True}],
                           [{"secondary_y": True}, {"secondary_y": True}]])

    trace1 = go.Bar(x=df2.date,
            y=df2['Rainfall'], opacity=0.6,name='Precipitation')

    trace2p = go.Scatter(x=df2.date,
            y=df2['MaxTemp'],name='2m Air Temperature',mode='lines',line=dict(color='red', width=2))
   
    trace3p = go.Bar(x=df2.date,
            y=df2['humidity_change_percent'], opacity=0.6,name='(%) Humidity Change')

    trace3 = go.Scatter(x=df2.date,
            y=df2['Evaporation'],name='Evaporation',mode='lines',line=dict(color='blue', width=2))
    
    
    trace4 = go.Bar(x=df2.date,
            y=df2['temp_change_min_max'], opacity=0.6,name='Temp Change')

    trace4p = go.Scatter(x=df2.date,
            y=df2['MinTemp'],name='Min Temp',mode='lines',line=dict(color='green', width=2))
        
    trace5 = go.Scatter(x=df2.date,
            y=df2['MaxTemp'],name='Max Temp',mode='lines',line=dict(color='goldenrod', width=2))

    trace5p = go.Scatter(x=df2.date,
            y=df2['WindGustSpeed'],name='Wind Gust',mode='lines',line=dict(color='magenta', width=2))


    fig.update_layout(title="Field Sensors Data",
                    template="plotly_white",title_x=0.5,legend=dict(orientation='h'))
    fig.add_trace(trace1,row=1, col=1, secondary_y=False)

    fig.add_trace(trace2p,row=1, col=1, secondary_y=True)
    fig['layout']['yaxis']['title']='ml'
    fig['layout']['yaxis2']['title']='°C'

    fig.add_trace(trace3,row=2, col=1, secondary_y=False)
    fig.add_trace(trace3p,row=2, col=1, secondary_y=True)
    fig['layout']['yaxis3']['title']='ml'
    fig['layout']['yaxis4']['title']='dH'

    fig.add_trace(trace4,row=1, col=2, secondary_y=False)
    fig.add_trace(trace4p,row=1, col=2, secondary_y=True)
    fig['layout']['yaxis5']['title']='°C'
    fig['layout']['yaxis6']['title']='dT'

    fig.add_trace(trace5,row=2, col=2, secondary_y=False)
    fig.add_trace(trace5p,row=2, col=2, secondary_y=True)
    fig['layout']['yaxis7']['title']='°C'
    fig['layout']['yaxis8']['title']='m/s'
    
    fig.update_layout(width=1500,height=500)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("index.html", graphJSON=graphJSON)

    '''
        For two rows and 1 column use following code !!!
    '''
    # fig = make_subplots(rows=2, cols=1,
    #                 specs=[[{"secondary_y": True}],
    #                         [{"secondary_y": True}]])
    # trace1 = go.Bar(x=df2.date,
    #     y=df2['Rainfall'], opacity=0.4,name='Precipitation')

    # trace2p = go.Scatter(x=df2.date,
    #         y=df2['MaxTemp'],name='Air Temperature (positive)',mode='lines',line=dict(color='red', width=1))

    # trace3 = go.Bar(x=df2.date,
    #         y=df2['Evaporation'], opacity=0.4,name='Evaporation')

    # trace3p = go.Scatter(x=df2.date,
    #         y=df2['humidity_change_percent'],name='Humidity Change (%)',mode='lines',line=dict(color='blue', width=1))

    # fig.update_layout(title="Field Sensors",
    #                 template="plotly_white",title_x=0.5,legend=dict(orientation='h'))
    # fig.add_trace(trace1,row=1, col=1, secondary_y=False)

    # fig.add_trace(trace2p,row=1, col=1, secondary_y=True)

    # fig['layout']['yaxis']['title']='ml'
    # fig['layout']['yaxis2']['title']='°C'
    # fig.add_trace(trace3,row=2, col=1, secondary_y=False)
    # fig.add_trace(trace3p,row=2, col=1, secondary_y=True)
    # fig['layout']['yaxis3']['title']='ml'
    # fig['layout']['yaxis4']['title']='DT'
    # fig.update_layout(width=900,height=500)
    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # return render_template("index.html", graphJSON=graphJSON)



#Define Path for Weather Predictions Route
@app.route('/predict/<min_temp>/<max_temp>/<rainfall>/<evaporation>/<sunshine>/<wind_gust_speed>/<wind_speed_9>/<wind_speed_3>/<humidity_9>/<humidity_3>/<pressure_9>/<pressure_3>/<cloud_9>/<cloud_3>/<temp_9>/<temp_3>/<rain_today_b>/<wind_gust_dir>/<wind_dir_9>/<wind_dir_3>', methods = ['GET'])

#Define Function for Dashboard Content
def weather_predict(min_temp, max_temp, rainfall, evaporation, sunshine, wind_gust_speed, wind_speed_9, wind_speed_3, humidity_9, humidity_3, pressure_9, pressure_3, cloud_9, cloud_3, temp_9, temp_3, rain_today_b, wind_gust_dir, wind_dir_9, wind_dir_3):

    #Import Baseline Weather Data
    weather_data = pd.read_csv('./Field_weather_data.csv')

    #Split Weather Data into X & Y Sets
    x_values_1 =  weather_data.drop(['rain_tomorrow_b'], axis = 1)
    y_values_1 = weather_data['rain_tomorrow_b']

    x_values_2 =  weather_data.drop(['rain_tomorrow_b', 'wind_change_direction', 'wind_gust_change_3', 'wind_gust_change_9'], axis = 1)
    y_values_2 = weather_data['rain_tomorrow_b']

    #Create Training & Testing Data Sets
    x_train_1, x_test_1, y_train_1, y_test_1 = train_test_split(x_values_1, y_values_1, random_state = 42, train_size = 0.8)
    x_train_2, x_test_2, y_train_2, y_test_2 = train_test_split(x_values_2, y_values_2, random_state = 42, train_size = 0.8)

    #Get Scalar Value for X Training Data
    x_scalar_1 = StandardScaler().fit(x_train_1)
    x_scalar_2 = StandardScaler().fit(x_train_2)

    #Determine Whether Wind Direction Changed
    if wind_dir_9 == wind_dir_3:
        wind_change_dir = 1
    else:
        wind_change_dir = 0

    if wind_dir_9 == wind_gust_dir:
        wind_gust_change_9 = 0
    else:
        wind_gust_change_9 = 1

    if wind_dir_3 == wind_gust_dir:
        wind_gust_change_3 = 0
    else:
        wind_gust_change_3 = 1

    if rain_today_b == True:
        rain_today = 1
    else:
        rain_today = 0

    #Calculate Temperature/Humidity/Pressure Changes
    temp_change_9to3 = abs(float(temp_9) - float(temp_3))
    temp_change_min_max = abs(float(min_temp) - float(max_temp))
    humidity_change = float(humidity_9) - float(humidity_3)
    pressure_change = float(pressure_9) - float(pressure_3)

    #Calculate Humidity Change Percentage
    if float(humidity_9) > 0:
        humidity_change_percent = humidity_change / int(humidity_9)
    else:
        humidity_change_percent = int(weather_data['Humidity9am'].max())

    #Create Lists of Input Values for Machine Learning Models
    mvlr_knn_svm_input = [[float(min_temp), float(max_temp), float(rainfall), float(evaporation), float(sunshine), float(wind_gust_speed), float(wind_speed_9), float(wind_speed_3), float(humidity_9), float(humidity_3), float(pressure_9), float(pressure_3), float(cloud_9), float(cloud_3), float(temp_9), float(temp_3), rain_today, temp_change_9to3, temp_change_min_max, humidity_change, humidity_change_percent, pressure_change, wind_change_dir, wind_gust_change_3, wind_gust_change_9]]
    rf_input = [[float(min_temp), float(max_temp), float(rainfall), float(evaporation), float(sunshine), float(wind_gust_speed), float(wind_speed_9), float(wind_speed_3), float(humidity_9), float(humidity_3), float(pressure_9), float(pressure_3), float(cloud_9), float(cloud_3), float(temp_9), float(temp_3), rain_today, temp_change_9to3, temp_change_min_max, humidity_change, humidity_change_percent, pressure_change]]

    #Transform Input Lists with Training Data Scalar Value
    mvlr_knn_svm_transformed = x_scalar_1.transform(mvlr_knn_svm_input)
    rf_transformed = x_scalar_2.transform(rf_input)

    #Import Machine Learning Models
    mvlr_model = joblib.load('./logistic.sav')
    knn_model = joblib.load('./KNN.sav')
    rf_model = joblib.load('./random_forest_engineered.sav')
    svm_model = joblib.load('./svm.sav')

    #Generate Weather Predictions from Machine Learning Models
    mvlr_predict = mvlr_model.predict(mvlr_knn_svm_transformed)
    knn_predict = knn_model.predict(mvlr_knn_svm_transformed)
    rf_predict = rf_model.predict(rf_transformed)
    svm_predict = svm_model.predict(mvlr_knn_svm_transformed)

    #Define Variables for Machine Learning Model Scores
    mvlr_score = 0.853
    knn_score = 0.850
    rf_score = 0.860
    svm_score = 0.852

    #Convert Weather Predictions to Boolean Values & Caclulate Overall Prediction
    if mvlr_predict == 1:
        mvlr = 'Yes'
    else:
        mvlr = 'No'

        mvlr_score = mvlr_score * -1

    if knn_predict == 1:
        knn = 'Yes'
    else:
        knn = 'No'

        knn_score = knn_score * -1

    if rf_predict == 1:
        rf = 'Yes'
    else:
        rf = 'No'

        rf_score = rf_score * -1

    if svm_predict == 1:
        svm = 'Yes'
    else:
        svm = 'No'

        svm_score = svm_score * -1

    total_score = mvlr_score + knn_score + rf_score + svm_score

    if total_score > 0:
        agg = 'Yes'
    else:
        agg = 'No'

    #Create Dictioary of Machine Learning Model Predictions
    predictions = {'MVLR': mvlr, 'KNN': knn, 'RF': rf, 'SVM': svm, 'AGG': agg}
        
    rain_prediction = jsonify(predictions)
    
    #Call HTML File & Pass in Dictionary with JSON Object
    return rain_prediction

#Initialize Flask App
# app.run()
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
