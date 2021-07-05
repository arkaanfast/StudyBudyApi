from .models import CommonQuestions
from .apps import ApiConfig
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity


def get_answer(question):
    try:
        passage = ApiConfig.jsonData[question.lower()[0 : len(question) - 1].strip()]
        result = ApiConfig.predictor.predict(passage=passage, question=question)
        answer = result["best_span_str"]
        return answer
    except Exception:
        vectorizer = CountVectorizer(stop_words="english")
        tfidf = TfidfTransformer(norm="l2")
        X_vec = vectorizer.fit_transform(ApiConfig.questions)
        X_tfidf = tfidf.fit_transform(X_vec)
        Y_vec = vectorizer.transform([question.lower()[0 : len(question) - 1].strip()])
        Y_tfidf = tfidf.fit_transform(Y_vec)
        angle = np.rad2deg(np.arccos(max(cosine_similarity(Y_tfidf, X_tfidf)[0])))
        if angle > 60:
            return None
        else:
            index = np.argmax(cosine_similarity(Y_tfidf, X_tfidf)[0])
            similar_question = ApiConfig.questions[index]
            passage = ApiConfig.jsonData[similar_question]
            result = ApiConfig.predictor.predict(passage=passage, question=question)
            answer = result["best_span_str"]
            return answer


def check_if_already_asked(question):
    try:
        model = CommonQuestions.objects.get(question=question)
        return model.answer
    except CommonQuestions.DoesNotExist:
        return None
