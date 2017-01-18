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
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic= get_object_or_404(ProfilePicture, id=1)
    global logged_out
    if logged_out == 0:
        return render(request, 'account/index.html', {'username': username, 'staff': staff, 'pro_pic': pro_pic})
    else:
        logged_out = 0
        return render(request, 'account/index.html', {'username': username, 'staff': staff, 'logged_out': True, 'pro_pic': pro_pic})


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
    user = request.user
    if user.username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic= get_object_or_404(ProfilePicture, id=1)

    if request.user.is_staff == 1:
        account = 'Dozent'
    else:
        account = 'Student'

    ergebnis = Ergebnis.objects.filter(user_id=request.user.id)
    quiz_ids = []
    for i in ergebnis:
        quiz_ids.append(Quiz.objects.filter(id=i.quiz)[0])
    print(str(quiz_ids))

    quiz_punkte = []

    for p in ergebnis:
        quiz_punkte.append(p.punkte)
    print('punkte' + str(quiz_punkte))

    ergebnis_liste = []

    for k in range (0, len(quiz_ids)):
        tup_punkte_liste = (quiz_ids[k], quiz_punkte[k])
        ergebnis_liste.append(tup_punkte_liste)
    print('ergl' + str(ergebnis_liste))


    global account_updated
    if account_updated == 0:
        return render(request, 'account/profile.html', {'user_rank': user_rank, 'user': user, 'account': account, 'pro_pic': pro_pic,
                                                        'ergebnis': ergebnis,'ergebnis_liste':ergebnis_liste})
    else:
        account_updated = 0
        return render(request, 'account/profile.html', {'user_rank': user_rank, 'user': user, 'account': account, 'pro_pic': pro_pic,
                                                        'account_updated': True, 'ergebnis': ergebnis})


def update_account(request):
    context = RequestContext(request)
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic= get_object_or_404(ProfilePicture, id=1)
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
        user = request.user
        form = UserForm(instance=user)

    return render(request, 'account/update_account.html', {'form': form, 'pro_pic': pro_pic}, context)


def update_picture(request):
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    user_rank_rank = user_rank.rank
    if user_rank_rank == 0:
        user_rank_rank = 1
    obj_propic = ProfilePicture.objects.filter(rank__lte=user_rank_rank)
    return render(request, 'account/update_picture.html', {'obj_propic': obj_propic, 'pro_pic': pro_pic})


def update_picture_save(request, profilepicture_id):
    user_id = request.user.id
    obj_user_rank = get_object_or_404(UserRank, user_fk_id=user_id)
    obj_user_rank.picture_id = profilepicture_id
    obj_user_rank.save(update_fields=["picture_id"])
    return HttpResponseRedirect('/account/profile/')


def course_statistic(request):
    dozent_id = request.user.id
    all_course = Course.objects.filter(dozent=dozent_id)
    username = request.user.username
    if username != '':
        user_rank = get_object_or_404(UserRank, user_fk_id=request.user.id)
        pro_pic = get_object_or_404(ProfilePicture, id=user_rank.picture_id)
    else:
        pro_pic = get_object_or_404(ProfilePicture, id=1)
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
    print(all_quiz_id)

    question_count = [0 for i in range(0, len(all_quiz_id))]

    print(str(len(quiz_id_array)))
    for x in range (0, len(quiz_id_array)):
        for y in range(0, len(all_quiz_id)):
            if quiz_id_array[x] == all_quiz_id[y]:
                question_count[y]+=1
    print('quest count' + str(question_count))
    max_score = [0 for i in range(0, len(all_quiz_id))]

    for k in range (0, len(question_count)):

        max_score[k]=question_count[k]*10

    print('max_score' + str(max_score))
    print('all_quiz_name' + str(all_quiz_name))

    print('all quiz' + str(all_quiz_id))
    print('ergebnis' + str(ergebnis))
    index_list = [i for i in range(0, len(all_quiz_id))]
    print('index liste' + str(index_list))

    terg_list = []
    for terg in ergebnis:
        tup_erg = (terg.punkte, terg.quiz)
        terg_list.append(tup_erg)
    print('tubdqbdb' + str(terg_list))

    drschnt_array = []
    for name in all_quiz_name:
        quiz_name = name
        gsmt_pkt = 0
        cntr = 0
        for erg in terg_list:
            if erg[1] == quiz_name:
                gsmt_pkt += erg[0]
                cntr+= 1
        if cntr == 0:
            drschnt = 0
        else:
            drschnt = gsmt_pkt / cntr
        drschnt_array.append(drschnt)
    print('drschnisztarray' +str(drschnt_array))

    tup_list = []
    for i in range(0, len(question_count)):
        tup = (all_quiz_name[i],max_score[i],drschnt_array[i])
        tup_list.append(tup)

    print(tup_list)

    return render(request, 'account/course_statistic.html', {'ergebnis': ergebnis, 'max_score': max_score,
                                                             'all_quiz_name': all_quiz_name, 'index_list': index_list,
                                                             'tup_list': tup_list, 'pro_pic': pro_pic})
