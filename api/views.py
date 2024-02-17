from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np
import pandas as pd
import pickle

with open('models/SVMClassifier.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
# model1 = pickle.load(open('models/health.pkl', 'rb'))

@api_view(['GET'])
def health_check(request):
    print('Checking health, request received successfully')
    return Response({'status': 200, 'message': "Success"})

@api_view(['POST'])
def crop_recommend(request):
    # Extract features from the request data
    N = int(request.data['N'])
    P = int(request.data['P'])
    K = int(request.data['K'])
    temperature = float(request.data['temperature'])
    humidity = float(request.data['humidity'])
    ph = float(request.data['ph'])
    rainfall = float(request.data['rainfall'])
    final_features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    
    # Make predictions
    prediction = model.predict(final_features)

    output = prediction[0]
    return Response({'status': 200, 'message': "Success", "payload": output})

@api_view(['POST'])
def suggestion(request):
    Crop = str(request.data['Crop'])
    N = int(request.data['N'])
    P = int(request.data['P'])
    K = int(request.data['K'])
    
    df = pd.read_csv('models/fertilizer.csv')
    
    nr = df[df['Crop'] == Crop]['N'].iloc[0]
    pr = df[df['Crop'] == Crop]['P'].iloc[0]
    kr = df[df['Crop'] == Crop]['K'].iloc[0]

    n = nr - N
    p = pr - P
    k = kr - K

    temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
    max_value = temp[max(temp.keys())]
    if max_value == "N":
        if n < 0:
            output = 'High in Nitrogen'
        else:
            output = "Low in Nitrogen"
    elif max_value == "P":
        if p < 0:
            output = 'High in Phosphorus'
        else:
            output = "Low in Phosphorus"
    else:
        if k < 0:
            output = 'High in Potassium'
        else:
            output = "Low in Potassium"
            
    return Response({'status': 200, 'message': "Success", "payload": output})

# @api_view(['POST'])
# def predict(request):
#     Estimated_Insects_Count = int(request.data['Estimated_Insects_Count'])
#     Crop_Type = int(request.data['Crop_Type'])
#     if(Crop_Type == 0):
#         Crop_Type_0 = 1
#         Crop_Type_1 = 0
#     else:
#         Crop_Type_0 = 0
#         Crop_Type_1 = 1
#     Soil_Type = int(request.data['Soil_Type'])
#     if(Soil_Type == 0):
#         Soil_Type_0 = 1
#         Soil_Type_1 = 0
#     else:
#         Soil_Type_0 = 0
#         Soil_Type_1 = 1
       
#     Pesticide_Use_Category = int(request.data['Pesticide_Use_Category'])
#     if(Pesticide_Use_Category == 1):
#         Pesticide_Use_Category_1 = 1
#         Pesticide_Use_Category_2 = 0
#         Pesticide_Use_Category_3 = 0
#     elif(Pesticide_Use_Category == 2):
#         Pesticide_Use_Category_1 = 0
#         Pesticide_Use_Category_2 = 1
#         Pesticide_Use_Category_3 = 0
#     else:
#         Pesticide_Use_Category_1 = 0
#         Pesticide_Use_Category_2 = 0
#         Pesticide_Use_Category_3 = 1
    
#     Number_Doses_Week = int(request.data['Number_Doses_Week'])
#     Number_Weeks_Used = int(request.data['Number_Weeks_Used'])
#     Number_Weeks_Quit = int(request.data['Number_Weeks_Quit'])
    
#     Season = int(request.data['Season'])
#     if(Season == 1):
#         Season_1 = 1
#         Season_2 = 0
#         Season_3 = 0
#     elif(Season == 2):
#         Season_1 = 0
#         Season_2 = 1
#         Season_3 = 0
#     else:
#         Season_1 = 0
#         Season_2 = 0
#         Season_3 = 1

#     final_features = np.array([[Estimated_Insects_Count,Number_Doses_Week, Number_Weeks_Used, Number_Weeks_Quit, Crop_Type_0, Crop_Type_1, Soil_Type_0, Soil_Type_1, Pesticide_Use_Category_1, Pesticide_Use_Category_2, Pesticide_Use_Category_3, Season_1, Season_2, Season_3]])
#     prediction = model1.predict(final_features)
#     output = prediction[0]

#     if output== 0:
#         output = "None"
#     elif output == 1:
#         output = "Damage due to other Cause"
#     else:
#         output = "Damage due to Pesticides"
        
#     return Response({'status': 200, 'message': "Success", "payload": output})
