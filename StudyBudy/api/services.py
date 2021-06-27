from .models import CommonQuestions
from .apps import ApiConfig


def get_answer(question):
    try:
        passage = ApiConfig.jsonData[question.lower()]
        result = ApiConfig.predictor.predict(passage=passage, question=question)
        answer = result["best_span_str"]
        return answer
    except Exception:
        return None


def check_if_already_asked(question):
    try:
        model = CommonQuestions.objects.get(question=question)
        return model.answer
    except CommonQuestions.DoesNotExist:
        return None
