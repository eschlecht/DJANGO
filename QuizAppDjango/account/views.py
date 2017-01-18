from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.shortcuts import render, redirect, render_to_response
from django.views import generic
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic import View
from .forms import UserForm
from .models import ProfilePicture, UserRank
import quiz
from quiz.models import Course, Quiz, EssayQuestion, TFQuestion, SingleChoiceQuestion, MultipleChoiceQuestion
from quiz.models import Ergebnis

# Create your views here.

logged_out = 0
account_updated = 0


def index(request):
    username = request.user.username
    staff = request.user.is_staff
    global logged_out
    if logged_out == 0:
        return render(request, 'account/index.html', {'username': username, 'staff': staff})
    else:
        logged_out = 0
        return render(request, 'account/index.html', {'username': username, 'staff': staff, 'logged_out': True})


class UserRegistration(View):
    form_class = UserForm
    template_name = 'account/registration.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            userrank_registration = UserRank(user_fk_id=user.id, rank=0, picture_id=1)
            userrank_registration.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    print('user: ', request.user.username, 'registriert und angemeldet!')
                    print('is staff?: ', request.user.is_staff)
                    request.session['member_id']=user.id
                    print(request.session['member_id'])
                    return redirect('/account/')


        return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    print('user ist ausgelogt!')
    global logged_out
    logged_out = 1
    return HttpResponseRedirect('/account/')


def profile(request):
    username = request.user.username
    email = request.user.email
    last_name = request.user.last_name
    lastlogin = request.user.last_login
    user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
    obj_picture = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    picture_url = obj_picture.picture
    title = user_rank.title
    best_erg_array_profile = []
    for erg in (Ergebnis.objects.all()):
        if erg.user_id == request.user.id:
            best_erg_array_profile.append(erg)
    if request.user.is_staff == 1:
        account = 'Dozent'
    else:
        account = 'Student'

    if email == '':
        email = 'Nicht eingetragen'
    global account_updated
    if account_updated == 0:
        return render(request, 'account/profile.html', {'title': title, 'username': username, 'email': email, 'account': account,
                                                    'lastlogin': lastlogin, 'last_name': last_name, 'picture_url': picture_url})
    else:
        account_updated = 0
        return render(request, 'account/profile.html', {'title': title, 'username': username, 'email': email, 'account': account,
                                                        'lastlogin': lastlogin, 'last_name': last_name, 'picture_url': picture_url, 'account_updated': True})

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
                                                            'lastlogin': lastlogin, 'last_name': last_name})
        else:
            account_updated = 0
            return render(request, 'Navi.html', {'username': username, 'email': email, 'account': account,
                                                            'lastlogin': lastlogin, 'last_name': last_name,
                                                            'account_updated': True})


def update_account(request):
    context = RequestContext(request)
    if request.method == 'POST':
        user = request.user
        new_password = request.POST.get('password')
        user.username = request.POST.get('username')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.set_password(request.POST.get('password'))
        user.save()

        user = authenticate(username=user.username, password=new_password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print('user: ', request.user.username, 'daten changed')

        global account_updated
        account_updated = 1
        return HttpResponseRedirect('/account/profile/')
    else:
        form = UserForm()

    return render(request, 'account/update_account.html', {'form': form}, context)


def update_picture(request):
    user_id = request.user.id
    obj_user_rank = get_object_or_404(UserRank, user_fk_id=user_id)
    user_rank = obj_user_rank.rank
    if user_rank == 0:
        user_rank = 1
    obj_propic = ProfilePicture.objects.filter(rank__lte=user_rank)
    return render(request, 'account/update_picture.html', {'obj_propic': obj_propic})


def update_picture_save(request, profilepicture_id):
    user_id = request.user.id
    obj_user_rank = get_object_or_404(UserRank, user_fk_id=user_id)
    obj_user_rank.picture_id = profilepicture_id
    obj_user_rank.save(update_fields=["picture_id"])
    return HttpResponseRedirect('/account/profile/')


def course_statistic(request):
    dozent_id = request.user.id
    all_course = Course.objects.filter(dozent=dozent_id)
    quiz_id_array = []
    for x in TFQuestion.objects.all():
        quiz_id_array.append(x.quizfk_id)
    for x in EssayQuestion.objects.all():
        quiz_id_array.append(x.quizfk_id)
    for x in MultipleChoiceQuestion.objects.all():
        quiz_id_array.append(x.quizfk_id)
    for x in SingleChoiceQuestion.objects.all():
        quiz_id_array.append(x.quizfk_id)

    print(quiz_id_array)

    question_count = []
    all_course_id = []
    all_quiz_name = []
    all_quiz_id = []
    ergebnis = []
    for course in all_course:
        all_course_id.append(course.id)
    all_quiz = Quiz.objects.all()
    for i in all_course_id:
        for quiz in all_quiz:
            if quiz.coursefk_id is i:
                all_quiz_name.append(quiz.quiz_title)
                for erg in Ergebnis.objects.all():
                    if erg.quiz == quiz.quiz_title:
                        ergebnis.append(erg)

    for p in all_course_id:
        for quiz in Quiz.objects.all():
            if quiz.coursefk_id == p:
                all_quiz_id.append(quiz.id)

    print(question_count)
    print(all_quiz_id)
    print(ergebnis)
    return render(request, 'account/course_statistic.html', {'ergebnis': ergebnis})
