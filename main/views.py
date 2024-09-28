from django.shortcuts import render
import os
from django.core.files.storage import default_storage
import tensorflow as tf

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from . models import DiseaseDetection
from .helper_function import load_and_pred

cur_dir = os.path.dirname(__file__)
model = tf.keras.models.load_model(os.path.join(cur_dir, 'model', 'model_0.h5'))
# model = tf.keras.models.load_model('https://agro-detect.s3.us-west-2.amazonaws.com/model_0.h5')


class_names = ['anthracnose', 'cercospora_leaf_spot', 'phosphorus_deficiency']
plant_names = {
    'anthracnose': 'Anthracnose',
    'cercospora_leaf_spot': 'Cercospora Leaf Spot',
    'phosphorus_deficiency': 'Phosphorus Deficiency',
}


def index(request):
    if request.method == 'POST':
        file = request.FILES['image']
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.path(file_name)
        try:
            pred, prob = load_and_pred(model, file_url, class_names)
        except ValueError as e:
            prediction = 'An error occured, try again!'
        else:
             prediction, probability = pred, prob
        context = {
            'pred': prediction,
            'prediction': plant_names[prediction],
            'probability': probability,
            # 'prob': f'{math.ceil(pred.max()*100)}%'
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


@api_view(['POST'])
def prediction(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['image']
    file_name = default_storage.save(file.name, file)
    file_url = default_storage.path(file_name)
    try:
        pred, prob = load_and_pred(model, file_url, class_names)
        # disease_prediction = DiseaseDetection.objects.create(image=file_url,
        #                                                      prediction=plant_names[pred],
        #                                                      prob=prob)
        # disease_prediction.save()
        # os.remove(file_name)
        return Response({'pred': pred,
                         'prob': prob,
                         'result': plant_names[pred],
                         },
                        status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'error': str(e),
                         'message': 'An error occurred, try again!',
                         },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def anthracnose(request):
    return render(request, 'diseases/anthracnose.html')


def cls(request):
    return render(request, 'diseases/cls.html')


def pd(request):
    return render(request, 'diseases/pd.html')


def camera(request):
    return render(request, 'camera.html')
