from django.http import HttpResponseRedirect
from quiz import urls
from quiz.models import Quiz
import random


def homepage(request):


    try:
        q_obj = Quiz(pk=6)
        myList = []

        for i in (Quiz.objects.all()):
            myList.append(i)

        quiz_id = myList[random.randint(0, len(myList))].id

        return HttpResponseRedirect('quiz/%s/answer_quiz/' % quiz_id)
    except Exception:
        return HttpResponseRedirect('quiz')
