from django.apps import AppConfig
from allennlp.predictors.predictor import Predictor

import json


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    # Predictor
    predictor = Predictor.from_path(
        "https://storage.googleapis.com/allennlp-public-models/bidaf-model-2020.03.19.tar.gz"
    )
    # Json Loader
    data = open("/home/arkaanfast/StudyBudyAPI/StudyBudy/api/data.json")
    jsonData = json.load(data)
    questions = list(jsonData.keys())
