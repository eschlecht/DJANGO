# -*- coding: utf-8 -*-
from __future__ import division

from itertools import chain

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.shortcuts import render_to_response
from .forms import CourseForm, QuizForm, EssayQuestionForm, SingleChoiceQuestionForm, MultipleChoiceQuestionForm, \
    TFQuestionForm, LobbyForm, EntryLobbyForm
from .models import Course, Quiz, EssayQuestion, SingleChoiceQuestion, MultipleChoiceQuestion, TFQuestion, Ergebnis, \
    Lobby, UserInLobby, ProposeEssayQuestion, ProposeSingleChoiceQuestion, ProposeMultipleChoiceQuestion, \
    ProposeTFQuestion, MultiplayerErgebnis, ProposeTFQuestion
from django.http import HttpResponseRedirect

from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from datetime import datetime
from time import sleep
import time

from .models import Course, Quiz, EssayQuestion, SingleChoiceQuestion, MultipleChoiceQuestion, TFQuestion \
    , ProposeSingleChoiceQuestion, ProposeEssayQuestion, ProposeMultipleChoiceQuestion, ProposeTFQuestion, Lobby, \
    UserInLobby
from account.models import UserRank, ProfilePicture
from django.http import HttpResponseRedirect

from django.views import generic
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
import os, sys, sqlite3
import json
from itertools import cycle
from django.template.loader import render_to_string
from django.template import loader, Context
import random
import ctypes

# import Tkinter
# import tkMessageBox

array_index = 0
myList = []
anzahl = 0
max_id_multiplechoice = 0
max_id_singlechoice = 0
max_id_truefalse = 0
max_id_essay = 0
starttime = None
endtime = None
gesamtpunktzahl = 0
question_delete = 0
deleted_question = u""
quiz_delete = 0
deleted_quiz = u""
course_delete = 0
deleted_course = u""
propose_question_delete = 0
propose_question_save = 0


# -*- coding: utf-8 -*-

def index(request):
    return render(request, 'quiz/index.html')


def settings(request):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)
    user = request.user
    print('Staff? :', request.user.is_staff)
    print('Username =', request.user.username)
    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    return render_to_response('quiz/settings.html', {'user': user, 'pro_pic': pro_pic})


def add_course(request):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)
    user = request.user
    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    context = RequestContext(request)
    if request.method == 'POST':

        form = CourseForm(request.POST)
        if form.is_valid():
            course_title = request.POST.get('course_title')
            semester = request.POST.get('semester')
            dozent = request.POST.get('dozent')
            c_obj = Course(course_title=course_title,
                           semester=semester,
                           dozent=request.user.id)
            c_obj.save()
        form = CourseForm()
        return render_to_response('quiz/add_course.html',
                                  {'user': user, 'form': form, 'saved': True, 'course': course_title,
                                   'pro_pic': pro_pic},
                                  context)

    else:
        form = CourseForm()
    return render_to_response('quiz/add_course.html', {'user': user, 'form': form, 'pro_pic': pro_pic}, context)


def add_course_rename(request, course_id):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)
    user = request.user
    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    context = RequestContext(request)
    rename = 1
    if request.method == 'POST':

        form = CourseForm(request.POST)
        if form.is_valid():
            c_obj = get_object_or_404(Course, pk=course_id)
            c_obj.course_title = request.POST.get('course_title')
            c_obj.semester = request.POST.get('semester')

            c_obj.id = course_id
            c_obj.save()
        form = CourseForm(None)
        return render_to_response('quiz/add_course.html',
                                  {'user': user, 'form': form, 'pro_pic': pro_pic, 'update': True,
                                   'course': c_obj.course_title},
                                  context)

    else:
        c_obj = get_object_or_404(Course, id=course_id)
        form = CourseForm(instance=c_obj)
    return render_to_response('quiz/add_course.html',
                              {'user': user, 'form': form, 'pro_pic': pro_pic, 'rename': rename}, context)


def add_quiz(request, course_id):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)
    user = request.user
    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')

    context = RequestContext(request)
    if request.method == 'POST':

        form = QuizForm(request.POST)
        if form.is_valid():
            quiz_title = request.POST.get('quiz_title')
            q_obj = Quiz(quiz_title=quiz_title,
                         coursefk_id=course_id)
            q_obj.save()
            form = QuizForm(None)
            allquiz = []
            for aq in Quiz.objects.filter(coursefk_id=course_id):
                allquiz.append(aq.quiz_title.encode('utf-8'))
            print(allquiz)
            if request.POST.get('submit'):
                print('s1')
                return render_to_response('quiz/add_quiz.html',
                                          {'form': form, 'saved': True, 'quiz': quiz_title, 'user': user,
                                           'allquiz': allquiz, 'pro_pic': pro_pic}, context)
            if request.POST.get('submit2'):
                print('s2')
                print(q_obj.id)
                return HttpResponseRedirect('/quiz/%s/add_question/' % q_obj.id)
    else:
        form = QuizForm()
        allquiz = []
        for aq in Quiz.objects.filter(coursefk_id=course_id):
            allquiz.append(aq.quiz_title.encode('utf-8'))

    return render_to_response('quiz/add_quiz.html',
                              {'form': form, 'allquiz': allquiz, 'user': user, 'pro_pic': pro_pic}, context)


def add_quiz_rename(request, course_id, quiz_id):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)
    user = request.user
    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    context = RequestContext(request)
    rename = 1
    quiz_obj = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':

        form = QuizForm(request.POST)
        quiz = str(request.POST.get('quiz_title'))
        if form.is_valid():
            q_obj = get_object_or_404(Quiz, pk=quiz_id)
            q_obj.quiz_title = request.POST.get('quiz_title')
            q_obj.coursefk_id = course_id
            q_obj.id = quiz_id
            q_obj.save()
        form = QuizForm(None)

        return render_to_response('quiz/add_quiz.html',
                                  {'user': user, 'form': form, 'pro_pic': pro_pic, 'update': True, 'quiz': quiz},
                                  context)
    else:
        form = QuizForm(instance=quiz_obj)
        allquiz = Quiz.objects.filter(coursefk_id=course_id)
    return render_to_response('quiz/add_quiz.html',
                              {'user': user, 'form': form, 'pro_pic': pro_pic, 'quiz': quiz_obj, 'rename': rename,
                               'allquiz': allquiz}, context)


def add_question(request, quiz_id):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)
    user = request.user

    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')

    tquestion = TFQuestion.objects.filter(quizfk=quiz_id)
    equestion = EssayQuestion.objects.filter(quizfk=quiz_id)
    squestion = SingleChoiceQuestion.objects.filter(quizfk=quiz_id)
    mquestion = MultipleChoiceQuestion.objects.filter(quizfk=quiz_id)

    context = RequestContext(request)
    if request.POST.get('essay') == 'Begriffs Frage':
        form = EssayQuestionForm()
        return render_to_response('quiz/addquestionselect.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "Begriffs Frage",
                                   'tquestion': tquestion,
                                   'equestion': equestion,
                                   'squestion': squestion, 'user': user,
                                   'mquestion': mquestion, 'pro_pic': pro_pic}, context)

    if request.POST.get('single') == 'single':
        form = SingleChoiceQuestionForm()
        return render_to_response('quiz/addquestionselect.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "Single Choice Question",
                                   'tquestion': tquestion,
                                   'equestion': equestion,
                                   'squestion': squestion, 'user': user,
                                   'mquestion': mquestion, 'pro_pic': pro_pic}, context)

    if request.POST.get('multi') == 'MultipleChoice Frage':
        form = MultipleChoiceQuestionForm()
        return render_to_response('quiz/addquestionselect.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "Multiple Choice Frage", 'a': True,
                                   'tquestion': tquestion,
                                   'equestion': equestion,
                                   'squestion': squestion, 'user': user,
                                   'mquestion': mquestion, 'pro_pic': pro_pic}, context)

    if request.POST.get('truefalse') == 'WahrFalsch Frage':
        form = TFQuestionForm()
        return render_to_response('quiz/addquestionselect.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "Wahr/Falsch Frage", 'b': True,
                                   'tquestion': tquestion,
                                   'equestion': equestion,
                                   'squestion': squestion, 'user': user,
                                   'mquestion': mquestion, 'pro_pic': pro_pic}, context)

    if request.POST.get('essay_question_text'):
        form = EssayQuestionForm(request.POST)
        if form.is_valid():
            q_obj = EssayQuestion(essay_question_text=request.POST.get('essay_question_text'),
                                  answer_text=request.POST.get('answer_text').lower(),
                                  quizfk_id=quiz_id)
            q_obj.save()
            form = EssayQuestionForm()
        return render_to_response('quiz/addquestionselect.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "Begriffs Frage",
                                   'tquestion': tquestion,
                                   'equestion': equestion,
                                   'squestion': squestion, 'user': user,
                                   'mquestion': mquestion, 'saved': True, 'saved_question': q_obj, 'pro_pic': pro_pic},
                                  context)

    if request.POST.get('single_question_text'):
        form = SingleChoiceQuestionForm(request.POST)
        if form.is_valid():
            scq_obj = SingleChoiceQuestion(single_question_text=request.POST.get('single_question_text'),
                                           false_answer1=request.POST.get('false_answer1'),
                                           false_answer2=request.POST.get('false_answer2'),
                                           false_answer3=request.POST.get('false_answer3'),
                                           right_answer=request.POST.get('right_answer'),
                                           quizfk_id=quiz_id)
            scq_obj.save()
        return render_to_response('quiz/addquestionselect.html',
                                  {'form': form, 'quiz_id': quiz_id, 'tquestion': tquestion,
                                   'equestion': equestion,
                                   'squestion': squestion, 'user': user,
                                   'mquestion': mquestion, 'saved': True, 'saved_question': scq_obj,
                                   'pro_pic': pro_pic}, context)

    if request.POST.get('tf_question_text'):
        form = TFQuestionForm(request.POST)
        if form.is_valid():
            if str(request.POST.get('drop')) == "True":
                true_or_false = True
            else:
                true_or_false = False

            mq_obj = TFQuestion(tf_question_text=request.POST.get('tf_question_text'),
                                true_or_false=true_or_false,
                                question_type="truefalse",
                                quizfk_id=quiz_id)
            mq_obj.save()
            form = TFQuestionForm()
        return render_to_response('quiz/addquestionselect.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "True or False Question", 'b': True,
                                   'tquestion': tquestion,
                                   'equestion': equestion,
                                   'squestion': squestion, 'user': user,
                                   'mquestion': mquestion, 'saved': True, 'saved_question': mq_obj, 'pro_pic': pro_pic},

                                  context)

    if request.POST.get('multi_question_text'):
        form = MultipleChoiceQuestionForm(request.POST)
        if form.is_valid():
            if str(request.POST.get('drop')) == "1":
                correct_answer = '1'

                print(str(request.POST.get('drop')))

            if str(request.POST.get('drop')) == "2":
                correct_answer = '2'

            if str(request.POST.get('drop')) == "3":
                correct_answer = '3'

            if str(request.POST.get('drop')) == "4":
                correct_answer = '4'

            mq_obj = SingleChoiceQuestion(single_question_text=request.POST.get('multi_question_text'),
                                          answer_text1=request.POST.get('answer_text1'),
                                          answer_text2=request.POST.get('answer_text2'),
                                          answer_text3=request.POST.get('answer_text3'),
                                          answer_text4=request.POST.get('answer_text4'),
                                          correct_answer=correct_answer,

                                          quizfk_id=quiz_id)
            mq_obj.save()
            form = MultipleChoiceQuestionForm()
            return render_to_response('quiz/addquestionselect.html',
                                      {'form': form, 'quiz_id': quiz_id, 'Question': "Multiple Choice Question",
                                       'a': True, 'tquestion': tquestion,
                                       'equestion': equestion,
                                       'squestion': squestion, 'user': user,
                                       'mquestion': mquestion, 'saved': True, 'saved_question': mq_obj,
                                       'pro_pic': pro_pic},

                                      context)

    else:
        form = EssayQuestionForm()
    return render_to_response('quiz/addquestionselect.html',
                              {'form': form, 'quiz_id': quiz_id, 'Question': "Begriffs Frage", 'tquestion': tquestion,
                               'equestion': equestion,
                               'squestion': squestion, 'user': user,
                               'mquestion': mquestion, 'pro_pic': pro_pic}, context)

    if request.POST.get('fertig'):
        return render(request, 'quiz/add_quiz.html', {'tquestion': tquestion,
                                                      'equestion': equestion,
                                                      'squestion': squestion,
                                                      'mquestion': mquestion, 'pro_pic': pro_pic}, context)


def fill_quiz(request):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)

    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    all_quiz = Quiz.objects.all()
    context = {
        'all_quiz': all_quiz
    }
    return render(request, 'quiz/fill_quiz.html', {'pro_pic': pro_pic}, context)


def fill_course(request):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)

    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    all_course = Course.objects.all()
    return render(request, 'quiz/fill_course.html', {'pro_pic': pro_pic, 'all_course': all_course})


def choose(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    all_question = EssayQuestion.objects.all()

    return render_to_response('quiz/choose.html', {'quiz': quiz, 'quiz_id': quiz_id, 'all_question': all_question})


def course_select(request):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)

    context = RequestContext(request)
    if request.GET.get('Suchen') == 'Suchen':
        search_query = request.GET.get('search_box')
        all_course = Course.objects.filter(course_title__startswith=search_query)
        if all_course.count() != 0:
            return render(request, 'quiz/course_select.html', {'all_course': all_course, 'pro_pic': pro_pic}, context)
        else:
            print('Suche ohne Treffer :(')
            return render(request, 'quiz/course_select.html',
                          {'all_course': all_course, 'pro_pic': pro_pic, 'empty': True}, context)
    else:
        all_course = Course.objects.all()
        print(all_course)
    return render(request, 'quiz/course_select.html', {'all_course': all_course, 'pro_pic': pro_pic}, context)


def quiz_select(request, course_id):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)

    context = RequestContext(request)
    if request.GET.get('Suchen') == 'Suchen':
        search_query = request.GET.get('search_box')
        all_quiz = Quiz.objects.filter(coursefk_id=course_id, quiz_title__startswith=search_query)
        if all_quiz.count() != 0:
            return render(request, 'quiz/quiz_select.html', {'all_quiz': all_quiz, 'pro_pic': pro_pic}, context)
        else:
            print('Suche ohne Treffer :(')
            return render(request, 'quiz/quiz_select.html', {'all_quiz': all_quiz, 'pro_pic': pro_pic, 'empty': True},
                          context)
    else:

        all_quiz = Quiz.objects.filter(coursefk_id=course_id)
        print(all_quiz)
    return render(request, 'quiz/quiz_select.html', {'all_quiz': all_quiz, 'pro_pic': pro_pic}, context)


def delete_quiz(request, quiz_id):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)

    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')

    all_quiz = Quiz.objects.all()

    quiz = get_object_or_404(Quiz, id=quiz_id)
    global deleted_quiz
    deleted_quiz = quiz
    for q in Ergebnis.objects.all():
        if q.quiz == quiz_id:
            q.delete()
    quiz.delete()
    print('Quiz mit ID', quiz_id, 'deleted.')
    global quiz_delete
    quiz_delete = 1

    # return render_to_response('quiz/update_quiz.html', {'all_quiz':all_quiz, 'quiz':quiz, 'delete':True})

    return HttpResponseRedirect('/quiz/update_quiz/', {'delete': True, 'pro_pic': pro_pic})

    return render(request, 'quiz/update_quiz.html', {'all_quiz': all_quiz, 'pro_pic': pro_pic}, context)


def delete_course(request, course_id):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)

    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    all_course = Course.objects.all()
    course = get_object_or_404(Course, id=course_id)
    global deleted_course
    print(course)
    deleted_course = course
    course.delete()
    print('Kurs mit ID', course_id, 'deleted.')
    global course_delete
    course_delete = 1

    return HttpResponseRedirect('/quiz/update_course/', {'pro_pic': pro_pic})


def delete_question(request, quiz_id):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)

    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    context = RequestContext(request)
    global question_delete
    global deleted_question
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if question_delete == 0:
        if request.GET.get('Suchen') == 'Suchen':
            search_query = request.GET.get('search_box')
            tquestion = TFQuestion.objects.filter(quizfk_id=quiz_id, tf_question_text__startswith=search_query)
            equestion = EssayQuestion.objects.filter(quizfk_id=quiz_id, essay_question_text__startswith=search_query)
            squestion = SingleChoiceQuestion.objects.filter(quizfk_id=quiz_id,
                                                            single_question_text__startswith=search_query)
            mquestion = MultipleChoiceQuestion.objects.filter(quizfk_id=quiz_id,
                                                              multi_question_text__startswith=search_query)
            return render(request, 'quiz/delete_question.html', {'tquestion': tquestion,
                                                                 'equestion': equestion,
                                                                 'squestion': squestion, 'quiz': quiz,
                                                                 'mquestion': mquestion, 'pro_pic': pro_pic}, context)
        else:
            tquestion = TFQuestion.objects.filter(quizfk_id=quiz_id)
            equestion = EssayQuestion.objects.filter(quizfk_id=quiz_id)
            squestion = SingleChoiceQuestion.objects.filter(quizfk_id=quiz_id)
            mquestion = MultipleChoiceQuestion.objects.filter(quizfk_id=quiz_id)
        return render(request, 'quiz/delete_question.html', {'tquestion': tquestion,
                                                             'equestion': equestion,
                                                             'squestion': squestion, 'quiz': quiz,
                                                             'mquestion': mquestion, 'pro_pic': pro_pic}, context)
    else:
        question_delete = 0
        if request.GET.get('Suchen') == 'Suchen':
            search_query = request.GET.get('search_box')
            tquestion = TFQuestion.objects.filter(quizfk_id=quiz_id, tf_question_text__startswith=search_query)
            equestion = EssayQuestion.objects.filter(quizfk_id=quiz_id, essay_question_text__startswith=search_query)
            squestion = SingleChoiceQuestion.objects.filter(quizfk_id=quiz_id,
                                                            single_question_text__startswith=search_query)
            mquestion = MultipleChoiceQuestion.objects.filter(quizfk_id=quiz_id,
                                                              multi_question_text__startswith=search_query)
            return render(request, 'quiz/delete_question.html', {'tquestion': tquestion,
                                                                 'equestion': equestion,
                                                                 'squestion': squestion, 'quiz': quiz,
                                                                 'mquestion': mquestion, 'delete': True,
                                                                 'deleted_question': deleted_question,
                                                                 'pro_pic': pro_pic}, context)
        else:
            tquestion = TFQuestion.objects.filter(quizfk_id=quiz_id)
            equestion = EssayQuestion.objects.filter(quizfk_id=quiz_id)
            squestion = SingleChoiceQuestion.objects.filter(quizfk_id=quiz_id)
            mquestion = MultipleChoiceQuestion.objects.filter(quizfk_id=quiz_id)
        return render(request, 'quiz/delete_question.html', {'tquestion': tquestion,
                                                             'equestion': equestion,
                                                             'squestion': squestion, 'quiz': quiz,
                                                             'mquestion': mquestion, 'delete': True,
                                                             'deleted_question': deleted_question, 'pro_pic': pro_pic},
                      context)


def delete_tfquestion(request, quiz_id, TFQuestion_id):
    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    tquestion = get_object_or_404(TFQuestion, id=TFQuestion_id)
    global deleted_question
    deleted_question = unicode(tquestion)
    tquestion.delete()
    global question_delete
    question_delete = 1
    return HttpResponseRedirect('/quiz/%s/delete_question/' % quiz_id)


def delete_essayquestion(request, quiz_id, EssayQuestion_id):
    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    equestion = get_object_or_404(EssayQuestion, id=EssayQuestion_id)
    global deleted_question
    deleted_question = unicode(equestion)
    equestion.delete()
    global question_delete
    question_delete = 1
    return HttpResponseRedirect('/quiz/%s/delete_question/' % quiz_id)


def delete_singlechoicequestion(request, quiz_id, SingleChoiceQuestion_id):
    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    squestion = get_object_or_404(SingleChoiceQuestion, id=SingleChoiceQuestion_id)
    global deleted_question
    deleted_question = unicode(squestion)
    squestion.delete()
    global question_delete
    question_delete = 1
    return HttpResponseRedirect('/quiz/%s/delete_question/' % quiz_id)


def delete_multiplechoicequestion(request, quiz_id, MultipleChoiceQuestion_id):
    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    mquestion = get_object_or_404(MultipleChoiceQuestion, id=MultipleChoiceQuestion_id)
    global deleted_question
    deleted_question = unicode(mquestion)
    mquestion.delete()
    global question_delete
    question_delete = 1
    return HttpResponseRedirect('/quiz/%s/delete_question/' % quiz_id)


def update_quiz(request):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)

    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    context = RequestContext(request)
    global quiz_delete
    if quiz_delete == 0:

        if request.GET.get('Suchen') == 'Suchen':
            search_query = request.GET.get('search_box')
            all_quiz = Quiz.objects.filter(quiz_title__startswith=search_query)
            if all_quiz.count() != 0:
                return render(request, 'quiz/update_quiz.html', {'all_quiz': all_quiz, 'pro_pic': pro_pic}, context)
            else:
                print('Suche ohne Treffer :(')
                return render(request, 'quiz/update_quiz.html',
                              {'all_quiz': all_quiz, 'pro_pic': pro_pic, 'empty': True}, context)
        else:
            all_quiz = Quiz.objects.all()

        return render(request, 'quiz/update_quiz.html', {'all_quiz': all_quiz, 'pro_pic': pro_pic}, context)
    else:
        quiz_delete = 0
        global deleted_quiz
        deleted_quiz = unicode(deleted_quiz)
        if request.GET.get('Suchen') == 'Suchen':
            search_query = request.GET.get('search_box')
            all_quiz = Quiz.objects.filter(quiz_title__startswith=search_query)
            if all_quiz.count() != 0:
                return render(request, 'quiz/update_quiz.html',
                              {'all_quiz': all_quiz, 'delete': True, 'deleted_quiz': deleted_quiz, 'pro_pic': pro_pic},
                              context)
            else:
                print('Suche ohne Treffer :(')
                return render(request, 'quiz/update_quiz.html',
                              {'all_quiz': all_quiz, 'delete': True, 'empty': True, 'deleted_quiz': deleted_quiz,
                               'pro_pic': pro_pic}, context)
        else:
            all_quiz = Quiz.objects.all()

        return render(request, 'quiz/update_quiz.html',
                      {'all_quiz': all_quiz, 'delete': True, 'deleted_quiz': deleted_quiz, 'pro_pic': pro_pic}, context)


def update_course(request):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)

    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    context = RequestContext(request)
    global course_delete
    if course_delete == 0:
        if request.GET.get('Suchen') == 'Suchen':

            search_query = request.GET.get('search_box')
            all_course = Course.objects.filter(course_title__startswith=search_query)
            print(all_course)
            if all_course.count() != 0:
                return render(request, 'quiz/update_course.html', {'all_course': all_course, 'pro_pic': pro_pic},
                              context)
            else:
                print('Suche ohne Treffer :(')
                return render(request, 'quiz/update_course.html',
                              {'all_course': all_course, 'pro_pic': pro_pic, 'empty': True}, context)
        else:
            all_course = Course.objects.all()
        return render(request, 'quiz/update_course.html', {'all_course': all_course, 'pro_pic': pro_pic}, context)
    else:
        course_delete = 0

        if request.GET.get('Suchen') == 'Suchen':

            search_query = request.GET.get('search_box')
            all_course = Course.objects.filter(course_title__startswith=search_query)
            print(all_course)
            if all_course.count() != 0:
                global deleted_course
                return render(request, 'quiz/update_course.html',
                              {'all_course': all_course, 'delete': True, 'deleted_course': deleted_course,
                               'pro_pic': pro_pic}, context)
            else:
                print('Suche ohne Treffer :(')
        else:
            all_course = Course.objects.all()
        return render(request, 'quiz/update_course.html',
                      {'all_course': all_course, 'delete': True, 'deleted_course': deleted_course, 'pro_pic': pro_pic},
                      context)


def update_question(request):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)

    if request.user.is_staff is False:
        print('Keine Berechtigung!')
        return HttpResponseNotFound('<h1>Keine Berechtigung!</h1>')
    context = RequestContext(request)
    global question_delete
    global deleted_question
    if question_delete == 0:
        if request.GET.get('Suchen') == 'Suchen':
            search_query = request.GET.get('search_box')
            tquestion = TFQuestion.objects.filter(tf_question_text__startswith=search_query)
            equestion = EssayQuestion.objects.filter(essay_question_text__startswith=search_query)
            squestion = SingleChoiceQuestion.objects.filter(single_question_text__startswith=search_query)
            mquestion = MultipleChoiceQuestion.objects.filter(multi_question_text__startswith=search_query)
            return render(request, 'quiz/update_question.html', {'tquestion': tquestion,
                                                                 'equestion': equestion,
                                                                 'squestion': squestion,
                                                                 'mquestion': mquestion, 'pro_pic': pro_pic}, context)
        else:
            tquestion = TFQuestion.objects.all()
            equestion = EssayQuestion.objects.all()
            squestion = SingleChoiceQuestion.objects.all()
            mquestion = MultipleChoiceQuestion.objects.all()
        return render(request, 'quiz/update_question.html', {'tquestion': tquestion,
                                                             'equestion': equestion,
                                                             'squestion': squestion,
                                                             'mquestion': mquestion, 'pro_pic': pro_pic}, context)
    else:
        question_delete = 0
        if request.GET.get('Suchen') == 'Suchen':
            search_query = request.GET.get('search_box')
            tquestion = TFQuestion.objects.filter(tf_question_text__startswith=search_query)
            equestion = EssayQuestion.objects.filter(essay_question_text__startswith=search_query)
            squestion = SingleChoiceQuestion.objects.filter(single_question_text__startswith=search_query)
            mquestion = MultipleChoiceQuestion.objects.filter(multi_question_text__startswith=search_query)
            return render(request, 'quiz/update_question.html', {'tquestion': tquestion,
                                                                 'equestion': equestion,
                                                                 'squestion': squestion,
                                                                 'mquestion': mquestion, 'delete': True,
                                                                 'deleted_question': deleted_question,
                                                                 'pro_pic': pro_pic}, context)
        else:
            tquestion = TFQuestion.objects.all()
            equestion = EssayQuestion.objects.all()
            squestion = SingleChoiceQuestion.objects.all()
            mquestion = MultipleChoiceQuestion.objects.all()
        return render(request, 'quiz/update_question.html', {'tquestion': tquestion,
                                                             'equestion': equestion,
                                                             'squestion': squestion,
                                                             'mquestion': mquestion, 'delete': True,
                                                             'deleted_question': deleted_question, 'pro_pic': pro_pic},
                      context)


def answer_quiz(request, quiz_id):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)
    user = request.user
    # return HttpResponse(1)
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    global myList
    if len(myList) == 0:
        print("Array leer")

        connection = sqlite3.connect("db.sqlite3")
        cursor = connection.cursor()

        global max_id_essay
        global max_id_truefalse
        global max_id_multiplechoice
        global max_id_singlechoice
        if str(len(MultipleChoiceQuestion.objects.all())) != 0:
            cursor.execute("""SELECT max(id) FROM quiz_multiplechoicequestion""")
            max_id_multiplechoice = cursor.fetchone()[0]
        else:
            max_id_multiplechoice = 0
        if str(len(SingleChoiceQuestion.objects.all())) != 0:
            cursor.execute("""SELECT max(id) FROM quiz_singlechoicequestion""")
            max_id_singlechoice = cursor.fetchone()[0]
        else:
            max_id_singlechoice = 0
        if str(len(TFQuestion.objects.all())) != 0:
            cursor.execute("""SELECT max(id) FROM quiz_tfquestion""")
            max_id_truefalse = cursor.fetchone()[0]
        else:
            max_id_truefalse = 0
        if str(len(EssayQuestion.objects.all())) != 0:
            cursor.execute("""SELECT max(id) FROM quiz_essayquestion""")
            max_id_essay = cursor.fetchone()[0]
        else:
            max_id_essay = int(0)
        print("kein Essay")

        # return HttpResponse(max_id_essay)

        global anzahl
        global max_id_multiplechoice
        global max_id_singlechoice
        global max_id_truefalse
        global max_id_essay
        anzahl = 0

        if str(len(MultipleChoiceQuestion.objects.all())) != 0:
            if max_id_multiplechoice is not None:
                for i in (MultipleChoiceQuestion.objects.all()):

                    if str(i.quizfk.id) == quiz_id:
                        myList.append(i)
                        anzahl = anzahl + 1

        if str(len(SingleChoiceQuestion.objects.all())) != 0:
            if max_id_singlechoice is not None:
                for i in (SingleChoiceQuestion.objects.all()):

                    if str(i.quizfk.id) == quiz_id:
                        myList.append(i)
                        anzahl = anzahl + 1
        if str(len(TFQuestion.objects.all())) != 0:
            if max_id_truefalse is not None:
                for i in (TFQuestion.objects.all()):

                    if str(i.quizfk.id) == quiz_id:
                        myList.append(i)  #
                        anzahl = anzahl + 1
        if str(len(EssayQuestion.objects.all())) != 0:
            if max_id_essay is not None:
                for i in (EssayQuestion.objects.all()):

                    if str(i.quizfk.id) == quiz_id:
                        myList.append(i)
                        anzahl = anzahl + 1

        random.shuffle(myList)

    # return HttpResponse(question)

    # return render_to_response('quiz/answer_multiplechoice.html', {'question': question, 'question_id': question_id})




    # return render(request, 'quiz/answer_multiplechoice.html', {'question': question})

    # url = '/quiz/' + quiz_id + '/answer_quiz/0'
    # return HttpResponseRedirect(url)

    if len(myList) != 0:
        global anzahl
        global max_id_multiplechoice
        global max_id_singlechoice
        global max_id_truefalse
        global max_id_essay
        global array_index

        if str(myList[0].quizfk.id) != str(quiz_id):
            myList = []
            array_index = 0
            anzahl = 0
            print("Andere quiz_id")

            global myList
            myList = []
            connection = sqlite3.connect("db.sqlite3")
            cursor = connection.cursor()

            cursor.execute("""SELECT max(id) FROM quiz_multiplechoicequestion""")
            max_id_multiplechoice = cursor.fetchone()[0]
            cursor.execute("""SELECT max(id) FROM quiz_singlechoicequestion""")
            max_id_singlechoice = cursor.fetchone()[0]
            cursor.execute("""SELECT max(id) FROM quiz_tfquestion""")
            max_id_truefalse = cursor.fetchone()[0]
            cursor.execute("""SELECT max(id) FROM quiz_essayquestion""")
            max_id_essay = cursor.fetchone()[0]

            # return HttpResponse(max_id_essay)



            if max_id_multiplechoice is None:
                max_id_multiplechoice = 0

            if max_id_singlechoice is None:
                max_id_singlechoice = 0

            if max_id_truefalse is None:
                max_id_truefalse = 0

            if max_id_essay is None:
                max_id_essay = 0

            for i in (MultipleChoiceQuestion.objects.all()):

                if str(i.quizfk.id) == quiz_id:
                    myList.append(i)
                    anzahl = anzahl + 1

            for i in (SingleChoiceQuestion.objects.all()):

                if str(i.quizfk.id) == quiz_id:
                    myList.append(i)
                    anzahl = anzahl + 1

            for i in (TFQuestion.objects.all()):

                if str(i.quizfk.id) == quiz_id:
                    myList.append(i)  #
                    anzahl = anzahl + 1

            for i in (EssayQuestion.objects.all()):

                if str(i.quizfk.id) == quiz_id:
                    myList.append(i)
                    anzahl = anzahl + 1

                random.shuffle(myList)

    if request.GET.get('Weiter') == 'Weiter':
        if array_index == anzahl - 1:
            global array_index
            global anzahl
            global myList
            global total_highscore
            array_index = 0
            anzahl = 0
            myList = []
            total_highscore = 0
            print("gesamtpunktzahl" + str(gesamtpunktzahl))
            user_id = request.user.id
            for i in (Ergebnis.objects.all()):
                if str(i.quiz) == str(quiz_id):
                    if str(i.user_id) == str(user_id):
                        if i.punkte < gesamtpunktzahl:
                            i.delete()
                            user_id = request.user.id
                            erg_obj = Ergebnis(quiz=quiz_id, punkte=gesamtpunktzahl, user_id=user_id)
                            erg_obj.save()

                            # update userrank.total_score
                            for h in (Ergebnis.objects.filter(user_id=user_id)):
                                total_highscore = total_highscore + h.punkte
                                print('count score: ', total_highscore)
                                obj_user_rank = get_object_or_404(UserRank, user_fk_id=user_id)
                                obj_user_rank.total_score = total_highscore
                                obj_user_rank.save(update_fields=["total_score"])

                            # update userrank.rank
                            obj_user_rank = get_object_or_404(UserRank, user_fk_id=user_id)
                            if obj_user_rank.total_score > 100:
                                obj_user_rank.title = 'Erfahrener'
                                obj_user_rank.rank = 1
                                if obj_user_rank.total_score > 500:
                                    obj_user_rank.title = 'Schlaumeier'
                                    obj_user_rank.rank = 2
                                    if obj_user_rank.total_score > 2000:
                                        obj_user_rank.title = 'Quiz Held'
                                        obj_user_rank.rank = 3
                                        if obj_user_rank.total_score > 5000:
                                            obj_user_rank.title = 'Champion'
                                            obj_user_rank.rank = 4
                                            if obj_user_rank.total_score > 10000:
                                                obj_user_rank.title = 'Grossmeister'
                                                obj_user_rank.rank = 5
                            else:
                                obj_user_rank.title = 'Neuling'
                            obj_user_rank.save(update_fields=["rank"])
                            obj_user_rank.save(update_fields=["title"])

                            return render_to_response('quiz/finish.html',
                                                      {'gesamtpunktzahl': gesamtpunktzahl, 'user': user,
                                                       'quiz': quiz, 'highscore': True, 'pro_pic': pro_pic})

            for i in (Ergebnis.objects.all()):
                if str(i.quiz) == str(quiz_id):
                    if str(i.user_id) == str(user_id):
                        bestleistung = i.punkte
                        return render_to_response('quiz/finish.html', {'gesamtpunktzahl': gesamtpunktzahl, 'quiz': quiz,
                                                                       'bestleistung': bestleistung, 'user': user,
                                                                       'keinHighscore': True, 'pro_pic': pro_pic})

            if username != '':
                erg_obj = Ergebnis(quiz=quiz_id, punkte=gesamtpunktzahl, user_id=user_id)
                erg_obj.save()
            return render_to_response('quiz/finish.html',
                                      {'gesamtpunktzahl': gesamtpunktzahl, 'user': user, 'quiz': quiz,
                                       'highscore': True, 'pro_pic': pro_pic})

        else:
            array_index = array_index + 1

            # return HttpResponse(array_index)

            question = myList[array_index]
            prozent = ((array_index + 1) / anzahl) * 100
            p = 1 / anzahl
            round(prozent, 3)
            stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)
            global starttime
            global endtime

            starttime = datetime.now()

            if question.question_type == 'multiplechoice':
                return render_to_response('quiz/answer_multiplechoice.html',
                                          {'question': question, 'user': user, 'stand': stand, 'prozent': prozent,
                                           'pro_pic': pro_pic})
            elif question.question_type == 'singlechoice':
                return render_to_response('quiz/answer_singlechoice.html',
                                          {'question': question, 'user': user, 'stand': stand, 'prozent': prozent,
                                           'pro_pic': pro_pic})
            elif question.question_type == 'truefalse':
                return render_to_response('quiz/answer_truefalse.html',
                                          {'question': question, 'user': user, 'stand': stand, 'prozent': prozent,
                                           'pro_pic': pro_pic})
            elif question.question_type == 'essay':
                return render_to_response('quiz/answer_essay.html',
                                          {'question': question, 'user': user, 'stand': stand, 'prozent': prozent,
                                           'pro_pic': pro_pic})

            return HttpResponseRedirect('/quiz/')




    elif request.GET.get('Fertig') == 'true':

        question = myList[array_index]
        if str(myList[array_index].true_or_false) == 'True':

            antwort_ist = 'Richtig'
            return render_to_response('quiz/answer_truefalse.html',
                                      {'question': question, 'user': user, 'pro_pic': pro_pic, 'r': True})
        else:
            antwort_ist = 'Falsch'
            return render_to_response('quiz/answer_truefalse.html',
                                      {'question': question, 'user': user, 'pro_pic': pro_pic, 'f': True})


    elif request.GET.get('Fertig') == 'wahr':

        question = myList[array_index]
        prozent = ((array_index + 1) / anzahl) * 100
        print(array_index + 1)
        print(anzahl)
        p = 1 / anzahl
        round(prozent, 3)
        print("p" + str(prozent))
        stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)
        if str(myList[array_index].true_or_false) == 'True':
            global starttime
            global endtime
            endtime = datetime.now()
            timedelta = endtime - starttime
            print("timedelta" + str(timedelta.seconds))
            punktzahl = 10 - int(timedelta.seconds)
            if punktzahl < 1:
                punktzahl = 1
            global gesamtpunktzahl
            gesamtpunktzahl = gesamtpunktzahl + punktzahl

            antwort_ist = 'Richtig'
            return render_to_response('quiz/answer_truefalse.html',
                                      {'question': question, 'r': True, 'stand': stand, 'prozent': prozent,
                                       'punktzahl': punktzahl, 'user': user, 'pro_pic': pro_pic})
        else:
            antwort_ist = 'Falsch'
            return render_to_response('quiz/answer_truefalse.html',
                                      {'question': question, 'f': True, 'stand': stand, 'user': user,
                                       'prozent': prozent, 'pro_pic': pro_pic})





    elif request.GET.get('Fertig') == 'falsch':

        question = myList[array_index]
        prozent = ((array_index + 1) / anzahl) * 100
        p = 1 / anzahl
        round(prozent, 3)
        stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)
        if str(myList[array_index].true_or_false) == 'False':
            global starttime
            global endtime
            endtime = datetime.now()
            timedelta = endtime - starttime
            punktzahl = 10 - int(timedelta.seconds)
            if punktzahl < 1:
                punktzahl = 1
            global gesamtpunktzahl
            gesamtpunktzahl = gesamtpunktzahl + punktzahl

            antwort_ist = 'Richtig'
            return render_to_response('quiz/answer_truefalse.html',
                                      {'question': question, 'r': True, 'stand': stand, 'prozent': prozent,
                                       'punktzahl': punktzahl, 'pro_pic': pro_pic, 'user': user})
        else:
            antwort_ist = 'Falsch'
            return render_to_response('quiz/answer_truefalse.html',
                                      {'question': question, 'f': True, 'stand': stand, 'user': user,
                                       'prozent': prozent, 'pro_pic': pro_pic})



    elif request.GET.get('Fertig') == 'falsch':

        question = myList[array_index]
        prozent = ((array_index + 1) / anzahl) * 100
        p = 1 / anzahl
        round(prozent, 3)
        stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)
        if str(myList[array_index].true_or_false) == 'False':
            global starttime
            global endtime
            endtime = datetime.now()
            timedelta = endtime - starttime
            punktzahl = 10 - int(timedelta.seconds)
            if punktzahl < 1:
                punktzahl = 1
            global gesamtpunktzahl
            gesamtpunktzahl = gesamtpunktzahl + punktzahl

            antwort_ist = 'Richtig'
            return render_to_response('quiz/answer_truefalse.html',
                                      {'question': question, 'r': True, 'stand': stand, 'prozent': prozent,
                                       'punktzahl': punktzahl, 'user': user, 'pro_pic': pro_pic})
        else:
            antwort_ist = 'Falsch'
            return render_to_response('quiz/answer_truefalse.html',
                                      {'question': question, 'user': user, 'f': True, 'stand': stand,
                                       'prozent': prozent, 'pro_pic': pro_pic})



    elif request.GET.get('Fertig') == 'Fertig':
        global starttime
        global endtime
        endtime = datetime.now()
        timedelta = endtime - starttime

        print(myList[array_index].question_type)

        if myList[array_index].question_type == 'multiplechoice':

            # return HttpResponse("<h1>hallo<h1>")
            # k = Question.objects.get(id=question_id).correct_answer_1
            # p = request.GET.get('checks1')
            # return HttpResponse(p)
            global r
            if not request.GET.get('checks1') is None:
                checking1 = "True"
            else:
                checking1 = "False"

            if not request.GET.get('checks2') is None:
                checking2 = "True"
            else:
                checking2 = "False"

            if not request.GET.get('checks3') is None:
                checking3 = "True"
            else:
                checking3 = "False"

            if not request.GET.get('checks4') is None:
                checking4 = "True"
            else:
                checking4 = "False"

            # return HttpResponse(str(Question.objects.get(id=question_id).correct_answer_1))
            prozent = ((array_index + 1) / anzahl) * 100
            p = 1 / anzahl
            round(prozent, 3)
            stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)

            if str(myList[array_index].correct_answer_1) == checking1:
                if str(myList[array_index].correct_answer_2) == checking2:
                    if str(myList[array_index].correct_answer_3) == checking3:
                        if str(myList[array_index].correct_answer_4) == checking4:
                            global starttime
                            global endtime
                            endtime = datetime.now()
                            timedelta = endtime - starttime
                            punktzahl = 10 - int(timedelta.seconds)
                            if punktzahl < 1:
                                punktzahl = 1
                            global gesamtpunktzahl
                            gesamtpunktzahl = gesamtpunktzahl + punktzahl

                            question = myList[array_index]

                            antwort_ist = 'Richtig'
                            return render_to_response('quiz/answer_multiplechoice.html',
                                                      {'question': question, 'r': True, 'user': user,
                                                       'pro_pic': pro_pic})
                            # else:
                            #   antwort_ist = 'Falsch'
                            ##  return render_to_response('quiz/answer_multiplechoice.html',
                            #                          {'question': question, 'f': True})









                            print('user clicked summary')

                        else:
                            question = myList[array_index]
                            return render_to_response('quiz/answer_multiplechoice.html',
                                                      {'question': question, 'f': True, 'user': user,
                                                       'pro_pic': pro_pic})
                    else:
                        question = myList[array_index]
                        return render_to_response('quiz/answer_multiplechoice.html',
                                                  {'question': question, 'f': True, 'user': user, 'pro_pic': pro_pic})
                else:
                    question = myList[array_index]
                    return render_to_response('quiz/answer_multiplechoice.html',
                                              {'question': question, 'f': True, 'user': user, 'pro_pic': pro_pic})
            else:
                question = myList[array_index]
                return render_to_response('quiz/answer_multiplechoice.html',
                                          {'question': question, 'f': True, 'user': user, 'pro_pic': pro_pic})











        elif myList[array_index].question_type == 'singlechoice':

            # return HttpResponse(array_index)
            question = myList[array_index]
            prozent = ((array_index + 1) / anzahl) * 100
            p = 1 / anzahl
            round(prozent, 3)
            stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)
            if myList[array_index].correct_answer == request.GET.get('checks'):
                global starttime
                global endtime
                endtime = datetime.now()
                timedelta = endtime - starttime
                punktzahl = 10 - int(timedelta.seconds)
                if punktzahl < 1:
                    punktzahl = 1
                global gesamtpunktzahl
                gesamtpunktzahl = gesamtpunktzahl + punktzahl
                antwort_ist = 'Richtig'
                return render_to_response('quiz/answer_singlechoice.html',
                                          {'question': question, 'r': True, 'stand': stand, 'prozent': prozent,
                                           'punktzahl': punktzahl, 'user': user, 'pro_pic': pro_pic})
            else:
                antwort_ist = 'Falsch'
                return render_to_response('quiz/answer_singlechoice.html',
                                          {'question': question, 'user': user, 'f': True, 'stand': stand,
                                           'prozent': prozent, 'pro_pic': pro_pic})






        elif myList[array_index].question_type == 'essay':

            question = myList[array_index]
            # return HttpResponse(array_index)
            prozent = ((array_index + 1) / anzahl) * 100
            p = 1 / anzahl
            round(prozent, 3)
            stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)
            if myList[array_index].answer_text.lower() == request.GET.get('answer').lower():
                global starttime
                global endtime
                endtime = datetime.now()
                timedelta = endtime - starttime
                punktzahl = 10 - int(timedelta.seconds)
                if punktzahl < 1:
                    punktzahl = 1
                global gesamtpunktzahl
                gesamtpunktzahl = gesamtpunktzahl + punktzahl
                antwort_ist = 'Richtig'
                return render_to_response('quiz/answer_essay.html',
                                          {'question': question, 'r': True, 'stand': stand, 'prozent': prozent,
                                           'punktzahl': punktzahl, 'user': user, 'pro_pic': pro_pic})
            else:
                antwort_ist = 'Falsch'
                return render_to_response('quiz/answer_essay.html',
                                          {'question': question, 'f': True, 'user': user, 'stand': stand,
                                           'prozent': prozent, 'pro_pic': pro_pic})

    global myList
    if len(myList) == 0:
        search_query = ''
        message = 'Quiz leer'
        print('duhgkddbhgdfjghdhgkdfshb')

        all_quiz = Quiz.objects.filter(quiz_title__startswith=search_query,
                                       coursefk_id=Quiz.objects.filter(id=quiz_id)[0].coursefk_id)

        # return HttpResponseRedirect('/quiz/quiz_select/')
        return render(request, 'quiz/quiz_select.html',
                      {'all_quiz': all_quiz, 'user': user, 'message': message, 'e': True, 'pro_pic': pro_pic})

    else:

        global starttime
        global endtime
        global gesamtpunktzahl
        gesamtpunktzahl = 0

        starttime = datetime.now()

        global array_index
        array_index = 0
        question = myList[array_index]
        prozent = ((array_index + 1) / anzahl) * 100

        p = 1 / anzahl
        round(prozent, 3)

        stand = "Frage " + str(array_index + 1) + " von " + str(anzahl)

    global myList
    if len(myList) == 0:
        message = 'Quiz leer'

        # return HttpResponseRedirect('/quiz/quiz_select/')
        return render_to_response('quiz/quiz_empty.html', {'message': message})

    else:

        antwort_ist = 'Viel Spass'
        global array_index

        array_index = 0
        question = myList[array_index]
        print(antwort_ist)
        if question.question_type == 'multiplechoice':
            return render_to_response('quiz/answer_multiplechoice.html',
                                      {'question': question, 'stand': stand, 'user': user, 'prozent': prozent,
                                       'pro_pic': pro_pic})
        elif question.question_type == 'singlechoice':
            return render_to_response('quiz/answer_singlechoice.html',
                                      {'question': question, 'stand': stand, 'user': user, 'prozent': prozent,
                                       'pro_pic': pro_pic})
        elif question.question_type == 'truefalse':
            return render_to_response('quiz/answer_truefalse.html',
                                      {'question': question, 'stand': stand, 'user': user, 'prozent': prozent,
                                       'pro_pic': pro_pic})
        elif question.question_type == 'essay':
            return render_to_response('quiz/answer_essay.html',
                                      {'question': question, 'stand': stand, 'user': user, 'prozent': prozent,
                                       'pro_pic': pro_pic})


def lobbys(request):
    entryLobby = EntryLobbyForm(request.POST)
    user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
    pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    try:
        if request.user.is_active is True:
            all_lobbys = Lobby.objects.all()
            lobby_form = LobbyForm(request.POST)
            entryLobby = EntryLobbyForm(request.POST)
            if request.POST.get('label'):
                form = LobbyForm(request.POST)
                if form.is_valid():
                    lobby = Lobby(label=str(request.POST.get('label')), owner=request.user.id,
                                  quiz_id=request.POST.get('field1'), lobby_password=request.POST.get('lobbypw'))
                    lobby.save()
                    lobby_id = Lobby.objects.filter(owner=request.user.id)
                    print "Save" + str(lobby_id.last().id)
                    if putUserInLobby(request.user.id, lobby_id.first().id) is True:
                        return HttpResponseRedirect('lobby_entry/%s' % str(lobby_id.last().id), {'notstart': True},
                                                    request)
                else:
                    print "label vorhanden"
                    return render_to_response('quiz/lobbys.html',
                                              {'all_lobbys': all_lobbys, 'lobby_form': lobby_form, 'duplicate': True,
                                               'entryLobby': entryLobby, 'pro_pic': pro_pic},
                                              request)
            if request.POST.get('beitreten'):
                print "beim beitreten"
                print request.POST.get('lobby_choice')
                if check_password(request.POST.get('lobby_choice'), request.POST.get('lobbyentrypw')):
                    print "nach dem check"
                    if putUserInLobby(request.user.id, request.POST.get('lobby_choice')) is True:
                        print "iwas"
                        return HttpResponseRedirect('lobby_entry/%s' % str(request.POST.get('lobby_choice')),
                                                    {'notstart': True, 'pro_pic': pro_pic},
                                                    request)
                    else:
                        return render_to_response('quiz/lobbys.html', {'all_lobbys': all_lobbys, 'lobby_form': lobby_form,
                                                                   'entryLobby': entryLobby,'lobbyStarted':True, 'pro_pic': pro_pic},
                                              request)

                else:
                    return render_to_response('quiz/lobbys.html', {'all_lobbys': all_lobbys, 'lobby_form': lobby_form,
                                                                   'entryLobby': entryLobby,'pwWrong':True, 'pro_pic': pro_pic},
                                              request)
            print "normal"
            return render_to_response('quiz/lobbys.html',
                                      {'all_lobbys': all_lobbys, 'lobby_form': lobby_form, 'entryLobby': entryLobby, 'pro_pic': pro_pic},
                                      request)
        else:
            print "not authorized"
            return render_to_response('quiz/index.html', {'b': True}, request)
    except Exception as e:
        print e.message
        print "exception in lobby"
        return render_to_response('quiz/lobbys.html',
                                  {'all_lobbys': all_lobbys, 'lobby_form': lobby_form, 'entryLobby': entryLobby, 'pro_pic': pro_pic},
                                  request)


def lobby_entry(request, lobby_id):
    try:
        all_users_in_lobby = UserInLobby.objects.filter(lobby_id=lobby_id)
        all_quiz = return_quiz(lobby_id)
        current_lobby = Lobby.objects.get(id=lobby_id)
        current_question_in_lobby = UserInLobby.objects.get(user_id=request.user.id)
        all_lobbys = Lobby.objects.all()
        lobby_form = LobbyForm
        entryLobby = EntryLobbyForm
        print all_quiz
        print Lobby.objects.get(id=lobby_id).owner is not request.user.id
        if request.POST.get('starten'):
            print "ich will starten"
            start_quiz(lobby_id)
            update_current_question(lobby_id,request.user.id)
            return render_to_response('quiz/lobby_entry.html',
                                      {'all_user': all_users_in_lobby,
                                       'quiz': all_quiz[current_question_in_lobby.current_question+1],
                                       'start': True},
                                      request)

        if request.POST.get('austreten'):
            all_lobbys = Lobby.objects.all()
            lobby_form = LobbyForm
            entryLobby = EntryLobbyForm
            userinlobby = UserInLobby.objects.filter(lobby_id=lobby_id)
            print userinlobby
            if len(userinlobby) == 1:
                print "lobby geloescht"
                Lobby.objects.get(id=lobby_id).delete()
                UserInLobby.objects.get(user_id=request.user.id).delete()
                return HttpResponseRedirect('/quiz/lobbys',
                                        {'all_lobbys': all_lobbys, 'lobby_form': lobby_form, 'entryLobby': entryLobby},
                                        request.POST)
            else:
                return HttpResponseRedirect('/quiz/lobbys',
                                            {'all_lobbys': all_lobbys, 'lobby_form': lobby_form,
                                             'entryLobby': entryLobby},
                                            request.POST)
        if current_lobby.started:
            print "hallo"
            if request.POST.get('True'):
                tffrage = all_quiz[current_question_in_lobby.current_question]
                print tffrage.true_or_false
                if check_tf_answer(tffrage.id, True):
                    print "richtig"
                    updateUserInLobby(request.user.id, 5)
                if not check_tf_answer(tffrage.id, True):
                    print check_tf_answer(tffrage.id, True)
                    print "antwort ist falsch"
                    updateUserInLobby(request.user.id, 0)
            if request.POST.get('False'):
                tffrage = all_quiz[current_question_in_lobby.current_question]
                print tffrage.true_or_false
                if check_tf_answer(tffrage.id, False):
                    print "richtig"
                    print check_tf_answer(tffrage.id, False)
                    updateUserInLobby(request.user.id, 5)
                if not check_tf_answer(tffrage.id, False):
                    print "antwort ist Falsch"
                    updateUserInLobby(request.user.id, 0)
            if request.POST.get('checks1') or request.POST.get('checks2') or request.POST.get('checks3') or request.POST.get('checks4'):
                if not request.POST.get('checks1') is None:
                    checking1 = "True"
                else:
                    checking1 = "False"
                print "check1"
                if not request.POST.get('checks2') is None:
                    checking2 = "True"
                else:
                    checking2 = "False"
                print "check2"
                if not request.POST.get('checks3') is None:
                    checking3 = "True"
                else:
                    checking3 = "False"
                print "check3"
                if not request.POST.get('checks4') is None:
                    checking4 = "True"
                else:
                    checking4 = "False"
                print "check4"
                multifrage = all_quiz[current_question_in_lobby.current_question]
                print str(check_multi_answer(multifrage.id, checking1, checking2, checking3, checking4))
                if check_multi_answer(multifrage.id, checking1, checking2, checking3, checking4):
                    updateUserInLobby(request.user.id, 5)
                    print "richtig multi"
                if not check_multi_answer(multifrage.id, checking1, checking2, checking3, checking4):
                    print "falsch multi"
                    print check_multi_answer(multifrage.id, checking1, checking2, checking3, checking4)
            if request.POST.get('answer'):
                essayfrage = all_quiz[current_question_in_lobby.current_question]
                if check_essay_answer(essayfrage.id, request.POST.get('answer')):
                    updateUserInLobby(request.user.id, 5)
                    print "richtig essay"
                if not check_essay_answer(essayfrage.id, request.POST.get('answer')):
                    print "falsch essay"
            if update_current_question(lobby_id,request.user.id):
                print "frage geupdatet"
                print current_question_in_lobby.current_question + 1
                return render_to_response('quiz/lobby_entry.html',
                                          {'all_user': all_users_in_lobby,
                                           'quiz': all_quiz[current_question_in_lobby.current_question + 1],
                                           'start': True},
                                          request)
            if not update_current_question(lobby_id,request.user.id):
                print "vorbei"
                return HttpResponseRedirect('/quiz/lobbys')
        print "nicht gestartet"
        return render_to_response('quiz/lobby_entry.html',
                                  {'all_user': all_users_in_lobby,
                                   'quiz': all_quiz[current_question_in_lobby.current_question], 'notstart': True},
                                  request)
    except IndexError as e:
        print e.message
        print "vorbei"
        all_users_in_lobby = UserInLobby.objects.filter(lobby_id=lobby_id)
        points = UserInLobby.objects.get(user_id=request.user.id).points
        return HttpResponseRedirect('/quiz/lobbys/mfinish/', {'points': points}, request)

    except Exception as e:
        print e.message
        print "exception in lobby_entry"

        return HttpResponseRedirect('/quiz/lobbys',
                                    {'all_lobbys': all_lobbys, 'lobby_form': lobby_form, 'entryLobby': entryLobby},
                                    request.POST)


def mfinish(request):
    try:
        points = UserInLobby.objects.get(user_id=request.user.id)
        print "im finish"
        lobb_id = UserInLobby.objects.get(user_id=request.user.id).lobby_id
        quiz_id = Lobby.objects.get(id=lobb_id).quiz_id
        quizname = Quiz.objects.get(id=quiz_id).quiz_title
        asd = UserInLobby.objects.filter(lobby_id=lobb_id)
        if request.POST.get('fertigEnde'):
            if len(asd) == 1:
                print "lobby geloescht"
                save_multiplayer_points(quizname,points.points,request.user.id)
                Lobby.objects.get(id=lobb_id).delete()
                UserInLobby.objects.get(user_id=request.user.id).delete()
                return HttpResponseRedirect('/quiz/lobbys')
            else:
                print "nicht owner von lobby"
                save_multiplayer_points(quizname, points.points, request.user.id)
                UserInLobby.objects.get(user_id=request.user.id).delete()
                return HttpResponseRedirect('/quiz/lobbys')

        return render_to_response('quiz/mfinish.html', {'points': points.points}, request)
    except Exception:
        return HttpResponseRedirect('/quiz/')


def putUserInLobby(user_id, lobby_id):
    lobby = Lobby.objects.filter(id=lobby_id)
    if lobby.first().started is True:
        print "lobby already started"
        return False
    if UserInLobby.objects.filter(user_id=user_id):
        print "user already in lobby"
        return False
    else:
        inlobby = UserInLobby(user_id=user_id, lobby_id=lobby_id,
                              username=User.objects.get(id=user_id).username,
                              points=0)
        inlobby.save()
        return True


def updateUserInLobby(user_id, points):
    inlobby = UserInLobby.objects.get(user_id=user_id)
    inlobby.points = points + inlobby.points
    inlobby.save()


def return_quiz(lobby_id):
    try:
        tf_query = TFQuestion.objects.filter(quizfk_id=Lobby.objects.filter(id=lobby_id).first().quiz_id)
        mcq_query = MultipleChoiceQuestion.objects.filter(quizfk_id=Lobby.objects.filter(id=lobby_id).first().quiz_id)
        ess_query = EssayQuestion.objects.filter(quizfk_id=Lobby.objects.filter(id=lobby_id).first().quiz_id)
        quiz = list(chain(tf_query, mcq_query, ess_query))
        print "quiz returned"
        return quiz
    except Exception:
        return Exception


def update_current_question(lobby_id,user_id):
    try:
        user = UserInLobby.objects.get(user_id=user_id)
        current_question = user.current_question
        query = return_quiz(lobby_id)
        print "query laenge"
        print len(query)
        if len(query) >= current_question:
            print "aktuelle Frage"
            print current_question
            user.current_question = current_question + 1
            user.save()
            current_question_in_lobby = Lobby.objects.get(id=lobby_id)
            print "jetzt frage"
            return True
        else:
            print "return von false"
            return False

    except Exception:
        print "exception in question update"
        return False

def save_multiplayer_points(quizname, points, userid):
    print("save")
    result = MultiplayerErgebnis(quiz=str(quizname), points=points, user_id=userid)
    result.save()


def start_quiz(lobby_id):
    try:
        lobby = Lobby.objects.get(id=lobby_id)
        lobby.started = True
        lobby.save()
    except Exception:
        print("failed to start")


def check_password(lobby_id, password):
    if password == Lobby.objects.get(id=lobby_id).lobby_password:
        return True
    else:
        print("falsches pw")
        return False


def check_tf_answer(question_id, boolean):
    if TFQuestion.objects.get(id=question_id).true_or_false == boolean:
        return True
    else:
        print("returne false")
        return False


def check_multi_answer(question_id, answer1, answer2, answer3, answer4):
    if str(MultipleChoiceQuestion.objects.get(id=question_id).correct_answer_1) == answer1:
        if str(MultipleChoiceQuestion.objects.get(id=question_id).correct_answer_2) == answer2:
            if str(MultipleChoiceQuestion.objects.get(id=question_id).correct_answer_3) == answer3:
                if str(MultipleChoiceQuestion.objects.get(id=question_id).correct_answer_4) == answer4:
                    print("antwort ist richtig")
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def check_essay_answer(question_id, answer):
    if EssayQuestion.objects.get(id=question_id).answer_text.lower() == answer.lower():
        return True
    else:
        return False


def getuserlistbylobbyid(request):
    lobby_id = UserInLobby.objects.get(user_id=request.user.id).lobby_id
    object = UserInLobby.objects.filter(lobby_id=lobby_id)
    print("habs versucht")
    return render_to_response('quiz/lobby_entry.html', {'all_user': object})


def Navi(request):
    username = request.user.username
    email = request.user.email
    last_name = request.user.last_name
    lastlogin = request.user.last_login
    user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
    obj_picture = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    picture_url = obj_picture.picture
    if request.user.is_staff == 1:
        account = 'Dozent'
    else:
        account = 'Student'

    if email == '':
        email = 'Nicht eingetragen'
    global account_updated
    if account_updated == 0:
        return render(request, 'Navi.html', {'username': username, 'email': email, 'account': account,
                                             'lastlogin': lastlogin, 'user': user, 'last_name': last_name,
                                             'pro_pic': pro_pic})
    else:
        account_updated = 0
        return render(request, 'Navi.html', {'username': username, 'email': email, 'account': account,
                                             'lastlogin': lastlogin, 'last_name': last_name,
                                             'account_updated': True, 'user': user, 'pro_pic': pro_pic})


def course_select_propose(request):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)
    context = RequestContext(request)
    if request.GET.get('Suchen') == 'Suchen':
        search_query = request.GET.get('search_box')
        all_course = Course.objects.filter(course_title__startswith=search_query)
        if all_course.count() != 0:
            return render(request, 'quiz/course_select_propose.html', {'all_course': all_course, 'pro_pic': pro_pic},
                          context)
        else:
            print('Suche ohne Treffer :(')
    else:
        all_course = Course.objects.all()
        print(all_course)
    return render(request, 'quiz/course_select_propose.html', {'all_course': all_course, 'pro_pic': pro_pic}, context)


def quiz_select_propose(request, course_id):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)
    context = RequestContext(request)

    if request.GET.get('Suchen') == 'Suchen':
        search_query = request.GET.get('search_box')
        all_quiz = Quiz.objects.filter(coursefk_id=course_id, quiz_title__startswith=search_query)
        if all_quiz.count() != 0:
            return render(request, 'quiz/quiz_select_propose.html', {'all_quiz': all_quiz, 'pro_pic': pro_pic}, context)
        else:
            print('Suche ohne Treffer :(')
    else:

        all_quiz = Quiz.objects.filter(coursefk_id=course_id)
        print(all_quiz)
    return render(request, 'quiz/quiz_select_propose.html', {'all_quiz': all_quiz, 'pro_pic': pro_pic}, context)


def propose_question(request, quiz_id):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)
    quiz = Quiz.objects.filter(id=quiz_id)
    print(quiz[0])
    course = Course.objects.filter(id=quiz[0].coursefk_id)
    print(course[0])
    dozent = course[0].dozent
    print(dozent)
    tquestion = TFQuestion.objects.filter(quizfk=quiz_id)
    equestion = EssayQuestion.objects.filter(quizfk=quiz_id)
    squestion = SingleChoiceQuestion.objects.filter(quizfk=quiz_id)
    mquestion = MultipleChoiceQuestion.objects.filter(quizfk=quiz_id)

    context = RequestContext(request)
    if request.POST.get('essay') == 'Begriffs Frage':
        form = EssayQuestionForm()
        return render_to_response('quiz/question_propose.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "Begriffs Frage",
                                   'tquestion': tquestion,
                                   'equestion': equestion,
                                   'squestion': squestion,
                                   'mquestion': mquestion, 'pro_pic': pro_pic}, context)

    if request.POST.get('single') == 'single':
        form = SingleChoiceQuestionForm()
        return render_to_response('quiz/question_propose.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "Single Choice Question",
                                   'tquestion': tquestion,
                                   'equestion': equestion,
                                   'squestion': squestion,
                                   'mquestion': mquestion, 'pro_pic': pro_pic}, context)

    if request.POST.get('multi') == 'MultipleChoice Frage':
        form = MultipleChoiceQuestionForm()
        return render_to_response('quiz/question_propose.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "Multiple Choice Frage", 'a': True,
                                   'tquestion': tquestion,
                                   'equestion': equestion,
                                   'squestion': squestion,
                                   'mquestion': mquestion, 'pro_pic': pro_pic}, context)

    if request.POST.get('truefalse') == 'WahrFalsch Frage':
        form = TFQuestionForm()
        return render_to_response('quiz/question_propose.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "Wahr/Falsch Frage", 'b': True,
                                   'tquestion': tquestion,
                                   'equestion': equestion,
                                   'squestion': squestion,
                                   'mquestion': mquestion, 'pro_pic': pro_pic}, context)

    if request.POST.get('essay_question_text'):
        form = EssayQuestionForm(request.POST)
        if form.is_valid():
            q_obj = ProposeEssayQuestion(essay_question_text=request.POST.get('essay_question_text'),
                                         answer_text=request.POST.get('answer_text').lower(),
                                         quizfk_id=quiz_id, user=request.user.id, dozent=dozent)
            q_obj.save()
            form = EssayQuestionForm()
        return render_to_response('quiz/question_propose.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "Begriffs Frage",
                                   'tquestion': tquestion,
                                   'equestion': equestion,
                                   'squestion': squestion, 'pro_pic': pro_pic,
                                   'mquestion': mquestion, 'saved': True, 'saved_question': q_obj}, context)

    if request.POST.get('single_question_text'):
        form = SingleChoiceQuestionForm(request.POST)
        if form.is_valid():
            scq_obj = ProposeSingleChoiceQuestion(single_question_text=request.POST.get('single_question_text'),
                                                  false_answer1=request.POST.get('false_answer1'),
                                                  false_answer2=request.POST.get('false_answer2'),
                                                  false_answer3=request.POST.get('false_answer3'),
                                                  right_answer=request.POST.get('right_answer'),
                                                  quizfk_id=quiz_id, user=request.user.id, dozent=dozent)
            scq_obj.save()
        return render_to_response('quiz/question_propose.html',
                                  {'form': form, 'quiz_id': quiz_id, 'tquestion': tquestion,
                                   'equestion': equestion,
                                   'squestion': squestion, 'pro_pic': pro_pic,
                                   'mquestion': mquestion, 'saved': True, 'saved_question': scq_obj}, context)

    if request.POST.get('tf_question_text'):
        print('Username =', request.user.username)
        form = TFQuestionForm(request.POST)
        if form.is_valid():
            if str(request.POST.get('drop')) == "True":
                true_or_false = True
            else:
                true_or_false = False

            mq_obj = ProposeTFQuestion(tf_question_text=request.POST.get('tf_question_text'),
                                       true_or_false=true_or_false,
                                       question_type="truefalse",
                                       quizfk_id=quiz_id, user=request.user.id, dozent=dozent)
            mq_obj.save()
            form = TFQuestionForm()
        return render_to_response('quiz/question_propose.html',
                                  {'form': form, 'quiz_id': quiz_id, 'Question': "True or False Question", 'b': True,
                                   'tquestion': tquestion,
                                   'equestion': equestion,
                                   'squestion': squestion, 'pro_pic': pro_pic,
                                   'mquestion': mquestion, 'saved': True, 'saved_question': mq_obj},

                                  context)

    if request.POST.get('multi_question_text'):
        form = MultipleChoiceQuestionForm(request.POST)
        if form.is_valid():
            if str(request.POST.get('drop')) == "1":
                correct_answer = '1'

                print(str(request.POST.get('drop')))


            else:
                correct_answer_1 = False
            if str(request.POST.get('drop')) == "2":
                correct_answer = '2'
            else:
                correct_answer_2 = False
            if str(request.POST.get('drop')) == "3":
                correct_answer = '3'
            else:
                correct_answer_3 = False
            if str(request.POST.get('drop')) == "4":
                correct_answer = '4'
            else:
                correct_answer_4 = False

            mq_obj = ProposeSingleChoiceQuestion(single_question_text=request.POST.get('multi_question_text'),
                                                 answer_text1=request.POST.get('answer_text1'),
                                                 answer_text2=request.POST.get('answer_text2'),
                                                 answer_text3=request.POST.get('answer_text3'),
                                                 answer_text4=request.POST.get('answer_text4'),
                                                 correct_answer=correct_answer,

                                                 quizfk_id=quiz_id, user=request.user.id, dozent=dozent)
            mq_obj.save()
            form = MultipleChoiceQuestionForm()
            return render_to_response('quiz/question_propose.html',
                                      {'form': form, 'quiz_id': quiz_id, 'Question': "Multiple Choice Question",
                                       'a': True, 'tquestion': tquestion,
                                       'equestion': equestion,
                                       'squestion': squestion,
                                       'mquestion': mquestion, 'saved': True, 'saved_question': mq_obj},

                                      context)

    else:
        form = EssayQuestionForm()
    return render_to_response('quiz/question_propose.html',
                              {'form': form, 'quiz_id': quiz_id, 'Question': "Begriffs Frage", 'tquestion': tquestion,
                               'equestion': equestion,
                               'squestion': squestion, 'pro_pic': pro_pic,
                               'mquestion': mquestion}, context)

    if request.POST.get('fertig'):
        return render(request, 'quiz/add_quiz.html', {'tquestion': tquestion,
                                                      'equestion': equestion,
                                                      'squestion': squestion, 'pro_pic': pro_pic,
                                                      'mquestion': mquestion}, context)


def proposed_questions(request):
    # Uebergabe von Profilbild
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)

    context = RequestContext(request)
    global question_delete
    global deleted_question
    global propose_question_delete
    my_id = request.user.id

    if propose_question_save == 0:

        if propose_question_delete == 0:

            tquestion = ProposeTFQuestion.objects.filter(dozent=my_id)
            equestion = ProposeEssayQuestion.objects.filter(dozent=my_id)
            squestion = ProposeSingleChoiceQuestion.objects.filter(dozent=my_id)
            mquestion = ProposeMultipleChoiceQuestion.objects.filter(dozent=my_id)
            return render(request, 'quiz/proposed_questions.html', {'tquestion': tquestion,
                                                                    'equestion': equestion,
                                                                    'squestion': squestion, 'pro_pic': pro_pic,
                                                                    'mquestion': mquestion}, context)
        else:
            propose_question_delete = 0

            tquestion = ProposeTFQuestion.objects.filter(dozent=my_id)
            equestion = ProposeEssayQuestion.objects.filter(dozent=my_id)
            squestion = ProposeSingleChoiceQuestion.objects.filter(dozent=my_id)
            mquestion = ProposeMultipleChoiceQuestion.objects.filter(dozent=my_id)
            return render(request, 'quiz/proposed_questions.html', {'tquestion': tquestion,
                                                                    'equestion': equestion,
                                                                    'squestion': squestion, 'pro_pic': pro_pic,
                                                                    'mquestion': mquestion, 'delete': True,
                                                                    'deleted_question': deleted_question}, context)
    else:
        global propose_question_save
        propose_question_save = 0
        if propose_question_delete == 0:

            tquestion = ProposeTFQuestion.objects.filter(dozent=my_id)
            equestion = ProposeEssayQuestion.objects.filter(dozent=my_id)
            squestion = ProposeSingleChoiceQuestion.objects.filter(dozent=my_id)
            mquestion = ProposeMultipleChoiceQuestion.objects.filter(dozent=my_id)
            return render(request, 'quiz/proposed_questions.html', {'tquestion': tquestion,
                                                                    'equestion': equestion,
                                                                    'squestion': squestion, 'pro_pic': pro_pic,
                                                                    'mquestion': mquestion, 'save': True}, context)
        else:
            propose_question_delete = 0

            tquestion = ProposeTFQuestion.objects.filter(dozent=my_id)
            equestion = ProposeEssayQuestion.objects.filter(dozent=my_id)
            squestion = ProposeSingleChoiceQuestion.objects.filter(dozent=my_id)
            mquestion = ProposeMultipleChoiceQuestion.objects.filter(dozent=my_id)
            return render(request, 'quiz/proposed_questions.html', {'tquestion': tquestion,
                                                                    'equestion': equestion,
                                                                    'squestion': squestion, 'pro_pic': pro_pic,
                                                                    'mquestion': mquestion, 'delete': True,
                                                                    'deleted_question': deleted_question}, context)

    if request.GET.get('Fertig') == 'Fertig':
        return HttpResponseRedirect('/quiz')


def show_proposed_truefalse(request, ProposeTFQuestion_id):
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)
    user = request.user
    tquestion = get_object_or_404(ProposeTFQuestion, id=ProposeTFQuestion_id)
    user_id = ProposeTFQuestion.objects.filter(id=ProposeTFQuestion_id)[0].user
    student = User.objects.filter(id=user_id)[0]
    quiz_id = tquestion.quizfk_id
    quiz = Quiz.objects.filter(id=quiz_id)[0]
    if tquestion.true_or_false == 1:
        true_or_false = 'wahr'
        true_or_false_database = 'True'
    else:
        true_or_false = 'falsch'
        true_or_false_database = 'False'
    if request.GET.get('Verwerfen') == 'Verwerfen':
        global propose_question_delete
        propose_question_delete = '1'
        tquestion.delete()
        return HttpResponseRedirect('/quiz/proposed_questions/')

    if request.GET.get('Speichern') == 'Speichern':
        global propose_question_save
        propose_question_save = 1
        tf_obj = TFQuestion(tf_question_text=tquestion.tf_question_text,
                            true_or_false=true_or_false_database,
                            question_type="truefalse",
                            quizfk_id=quiz_id)
        tf_obj.save()
        tquestion.delete()
        return HttpResponseRedirect('/quiz/proposed_questions/')

    return render_to_response('quiz/show_proposed_truefalse.html',
                              {'tquestion': tquestion, 'user': user, 'pro_pic': pro_pic, 'student': student,
                               'user_id': user_id, 'true_or_false': true_or_false, 'quiz': quiz})


def show_proposed_essay(request, ProposeEssayQuestion_id):
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)
    user = request.user
    essayquestion = get_object_or_404(ProposeEssayQuestion, id=ProposeEssayQuestion_id)
    user_id = ProposeEssayQuestion.objects.filter(id=ProposeEssayQuestion_id)[0].user
    student = User.objects.filter(id=user_id)[0]
    quiz_id = essayquestion.quizfk_id
    quiz = Quiz.objects.filter(id=quiz_id)[0]
    global propose_question_delete
    print(student)
    if request.GET.get('Verwerfen') == 'Verwerfen':
        essayquestion.delete()
        global propose_question_delete
        propose_question_delete = '1'
        return HttpResponseRedirect('/quiz/proposed_questions/')

    if request.GET.get('Speichern') == 'Speichern':
        global propose_question_save
        propose_question_save = 1
        essayf_obj = EssayQuestion(essay_question_text=essayquestion.essay_question_text,
                                   answer_text=essayquestion.answer_text,

                                   question_type="essay",
                                   quizfk_id=quiz_id)
        essayf_obj.save()
        essayquestion.delete()

        return HttpResponseRedirect('/quiz/proposed_questions/')

    return render_to_response('quiz/show_proposed_essay.html',
                              {'essayquestion': essayquestion, 'pro_pic': pro_pic, 'user': user, 'student': student,
                               'user_id': user_id, 'quiz': quiz})


def show_proposed_multiplechoice(request, ProposeSingleChoiceQuestion_id):
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)
    user = request.user
    multiplechoicequestion = get_object_or_404(ProposeSingleChoiceQuestion, id=ProposeSingleChoiceQuestion_id)
    user_id = ProposeSingleChoiceQuestion.objects.filter(id=ProposeSingleChoiceQuestion_id)[0].user
    student = User.objects.filter(id=user_id)[0]
    quiz_id = multiplechoicequestion.quizfk_id
    quiz = Quiz.objects.filter(id=quiz_id)[0]
    correct_answer_id = multiplechoicequestion.correct_answer
    correct_answer_text = ''
    if correct_answer_id == '1':
        correct_answer_text = multiplechoicequestion.answer_text1
    elif correct_answer_id == '2':
        correct_answer_text = multiplechoicequestion.answer_text2
    elif correct_answer_id == '3':
        correct_answer_text = multiplechoicequestion.answer_text3
    elif correct_answer_id == '4':
        correct_answer_text = multiplechoicequestion.answer_text4

    print ('at' + str(correct_answer_text))
    if request.GET.get('Verwerfen') == 'Verwerfen':
        global propose_question_delete
        propose_question_delete = '1'
        multiplechoicequestion.delete()
        return HttpResponseRedirect('/quiz/proposed_questions/')

    if request.GET.get('Speichern') == 'Speichern':
        global propose_question_save
        propose_question_save = 1
        multif_obj = SingleChoiceQuestion(single_question_text=multiplechoicequestion.single_question_text,
                                          correct_answer=correct_answer_id,
                                          answer_text1=multiplechoicequestion.answer_text1,
                                          answer_text2=multiplechoicequestion.answer_text2,
                                          answer_text3=multiplechoicequestion.answer_text3,
                                          answer_text4=multiplechoicequestion.answer_text4,

                                          question_type="singlechoice",
                                          quizfk_id=quiz_id)
        multif_obj.save()
        multiplechoicequestion.delete()

        return HttpResponseRedirect('/quiz/proposed_questions/')

    return render_to_response('quiz/show_proposed_multiplechoice.html',
                              {'multiplechoicequestion': multiplechoicequestion, 'correct_answer_id': correct_answer_id,
                               'correct_answer_text': correct_answer_text, 'pro_pic': pro_pic, 'user': user,
                               'student': student, 'user_id': user_id, 'quiz': quiz})
