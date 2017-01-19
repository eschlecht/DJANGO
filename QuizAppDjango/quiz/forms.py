# -*- coding: utf-8 -*-
from django import forms
from .models import Course, Quiz, SingleChoiceQuestion, EssayQuestion, MultipleChoiceQuestion, TFQuestion, Lobby


class CourseForm(forms.ModelForm):
    course_title = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'placeholder': 'Kursname eingeben'}))
    semester = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': 'Semesterzahl eingeben'}))

    class Meta:
        model = Course
        fields = ['course_title', 'semester']


class QuizForm(forms.ModelForm):
    quiz_title = forms.CharField(max_length=200, widget=forms.TextInput(

        attrs={'placeholder': 'Quiz Name eintragen'}))

    class Meta:
        model = Quiz
        fields = ['quiz_title']


class EssayQuestionForm(forms.ModelForm):
    essay_question_text = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Frage eingeben'}))
    answer_text = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Antwort eingeben'}))
    foreign_key_quiz_id = forms.HiddenInput()

    class Meta:
        model = EssayQuestion
        fields = ['essay_question_text', 'answer_text']


class SingleChoiceQuestionForm(forms.ModelForm):
    single_question_text = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Frage eingeben'}))
    right_answer = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'erste Antwort eingeben'}))

    false_answer1 = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'zweite Antwort eingeben'}))
    false_answer2 = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'dritte Antwort eingeben'}))
    false_answer3 = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'vierte Antwort eingeben'}))
    correct_answer1 = forms.CharField(max_length=1)

    class Meta:
        model = SingleChoiceQuestion
        fields = '__all__'


class MultipleChoiceQuestionForm(forms.ModelForm):
    multi_question_text = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Frage eingeben'}))
    answer_text1 = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'erste Antwort eingeben'}))
    answer_text2 = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'zweite Antwort eingeben'}))
    answer_text3 = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'dritte Antwort eingeben'}))
    answer_text4 = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'vierte Antwort eingeben'}))

    class Meta:
        model = MultipleChoiceQuestion
        fields = ['multi_question_text', 'answer_text1', 'answer_text2', 'answer_text3', 'answer_text4']


class TFQuestionForm(forms.ModelForm):
    tf_question_text = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Frage eingeben'}))

    class Meta:
        model = TFQuestion
        fields = ['tf_question_text']


class LobbyForm(forms.ModelForm):
    field1 = forms.ModelChoiceField(queryset=Quiz.objects.all(), empty_label="Waehle ein Quiz")
    label = forms.CharField(max_length=200,
                            widget=forms.TextInput(attrs={'placeholder': 'Geben Sie Ihrer Lobby einen Namen!'}))
    lobbypw = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Password *Optional'}),
                              required=False)

    class Meta:
        model = Lobby
        fields = ['label', 'lobbypw', 'field1']


class EntryLobbyForm(forms.ModelForm):
    lobby_choice = forms.ModelChoiceField(queryset=Lobby.objects.all(), empty_label="Waehle eine Lobby")
    lobbyentrypw = forms.CharField(max_length=50,
                                   widget=forms.PasswordInput(attrs={'placeholder': 'Password *Optional'}),
                                   required=False)

    class Meta:
        model = Lobby
        fields = ['lobby_choice', 'lobbyentrypw']
