import os
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from huella_carbon import settings
from .serializers import PrediccionesSerializers
import pandas as pd

# Create your views here.
import joblib
model_path = os.path.join(settings.BASE_DIR, 'use_model', 'models', 'Boosting.joblib')
if os.path.exists(model_path):
    model = joblib.load(model_path)
prepocesamiento_path = os.path.join(settings.BASE_DIR, 'use_model', 'models', 'preprocesamiento.joblib')
if os.path.exists(prepocesamiento_path):
    prepocesamiento = joblib.load(prepocesamiento_path)

class PrediccionAIView(APIView):
    def post(self,request,*args,**kwargs):
        serializer = PrediccionesSerializers(data = request.data)

        if serializer.is_valid():
            Data = pd.DataFrame({
            'Body Type': [serializer.validated_data['Body_type']],
            'Diet': [serializer.validated_data['Diet']],
            'How Often Shower': [serializer.validated_data['How_Often_Shower']],
            'Heating Energy Source': [serializer.validated_data['Heating_Energy_Source']],
            'Transport': [serializer.validated_data['Transport']],
            'Vehicle Type': [serializer.validated_data['Vehicle_Type']],
            'Social Activity': [serializer.validated_data['Social_Activity']],
            'Frequency of Traveling by Air': [serializer.validated_data['Frequency_of_Traveling_by_Air']],
            'Waste Bag Size': [serializer.validated_data['Waste_Bag_Size']],
            'Energy efficiency': [serializer.validated_data['Energy_efficiency']],
            'Recycling': [serializer.validated_data['Recycling']],
            'Cooking_With': [serializer.validated_data['Cooking_With']],
            'Monthly Grocery Bill': [serializer.validated_data['Monthly_Grocery_Bill']],
            'Vehicle Monthly Distance Km': [serializer.validated_data['Vehicle_Monthly_DistanceKm']],
            'Waste Bag Weekly Count': [serializer.validated_data['Waste_Bag_Weekly_Count']],
            'How Long TV PC Daily Hour': [serializer.validated_data['How_Long_TV_PC_Daily_Hour']],
            'How Many New Clothes Monthly': [serializer.validated_data['How_Many_New_Clothes_Monthly']],
            'How Long Internet Daily Hour': [serializer.validated_data['How_Long_Internet_Daily_Hour']]
        })
            df_transformer = prepocesamiento.transform(Data)
            prediction = model.predict(df_transformer)
            return Response({'Prediccion': prediction},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)