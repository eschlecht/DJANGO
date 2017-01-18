from django.db import models


# Create your models here.
class Course(models.Model):
    course_title = models.CharField(max_length=50)
    semester = models.IntegerField()
    dozent = models.IntegerField()

    def __str__(self):
        return self.course_title


class Quiz(models.Model):
    quiz_title = models.CharField(max_length=200)
    coursefk = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.quiz_title


class Ergebnis(models.Model):
    quiz = models.CharField(max_length=200)
    punkte = models.IntegerField()
    user_id = models.IntegerField()

    def __str__(self):
        return self.quiz


class MultiplayerErgebnis(models.Model):
    quiz = models.CharField(max_length=200)
    points = models.IntegerField()
    user_id = models.IntegerField()

    def __str__(self):
        return self.quiz


class EssayQuestion(models.Model):
    essay_question_text = models.CharField(max_length=200)
    answer_text = models.CharField(max_length=200)
    quizfk = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=200, default='essay')

    def __str__(self):
        return self.essay_question_text


class SingleChoiceQuestion(models.Model):
    single_question_text = models.CharField(max_length=200)
    answer_text1 = models.CharField(max_length=200, default='')
    answer_text2 = models.CharField(max_length=200, default='')
    answer_text3 = models.CharField(max_length=200, default='')
    answer_text4 = models.CharField(max_length=200, default='')

    correct_answer = models.CharField(max_length=200)
    question_type = models.CharField(max_length=200, default='singlechoice')
    quizfk = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.single_question_text


class MultipleChoiceQuestion(models.Model):

    multi_question_text = models.CharField(max_length=200)
    answer_text1 = models.CharField(max_length=200, default='')
    answer_text2 = models.CharField(max_length=200, default='')
    answer_text3 = models.CharField(max_length=200, default='')
    answer_text4 = models.CharField(max_length=200, default='')
    correct_answer_1 = models.BooleanField(help_text="*       clear = False | Checked = True")
    correct_answer_2 = models.BooleanField(help_text="*       clear = False | Checked = True")
    correct_answer_3 = models.BooleanField(help_text="*       clear = False | Checked = True")
    correct_answer_4 = models.BooleanField(help_text="*       clear = False | Checked = True")
    question_type = models.CharField(max_length=200, default='multiplechoice')
    quizfk = models.ForeignKey(Quiz, on_delete=models.CASCADE)


    def __str__(self):
        return self.multi_question_text


class TFQuestion(models.Model):
    tf_question_text = models.CharField(max_length=200)
    true_or_false = models.BooleanField(default=False, help_text="*clear = False | Checked = True")
    quizfk = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=200, default='truefalse')

    def __str__(self):
        return self.tf_question_text

class Lobby(models.Model):
    owner = models.CharField(max_length=200, default="")
    label = models.SlugField(unique=True)
    quiz_id = models.IntegerField(default=1)
    lobby_password = models.CharField(max_length=200, default="")
    started = models.BooleanField(default=False)

    def __unicode__(self):
        return self.label


class UserInLobby(models.Model):
    user_id = models.IntegerField(default=1)
    lobby_id = models.IntegerField(default=1)
    username = models.CharField(max_length=50)
    points = models.IntegerField(default=0)
    current_question = models.IntegerField(default=0)

class ProposeEssayQuestion(models.Model):
    essay_question_text = models.CharField(max_length=200)
    answer_text = models.CharField(max_length=200)
    quizfk = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=200, default='essay')
    user = models.IntegerField(default='')
    dozent = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.essay_question_text


class ProposeSingleChoiceQuestion(models.Model):
    single_question_text = models.CharField(max_length=200)
    answer_text1 = models.CharField(max_length=200, default='')
    answer_text2 = models.CharField(max_length=200, default='')
    answer_text3 = models.CharField(max_length=200, default='')
    answer_text4 = models.CharField(max_length=200, default='')

    correct_answer = models.CharField(max_length=200)
    question_type = models.CharField(max_length=200, default='singlechoice')
    quizfk = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.IntegerField(default='')
    dozent = models.CharField(max_length=200, default='')


    def __str__(self):
        return self.single_question_text


class ProposeMultipleChoiceQuestion(models.Model):

    multi_question_text = models.CharField(max_length=200)
    answer_text1 = models.CharField(max_length=200, default='')
    answer_text2 = models.CharField(max_length=200, default='')
    answer_text3 = models.CharField(max_length=200, default='')
    answer_text4 = models.CharField(max_length=200, default='')
    correct_answer_1 = models.BooleanField(help_text="*       clear = False | Checked = True")
    correct_answer_2 = models.BooleanField(help_text="*       clear = False | Checked = True")
    correct_answer_3 = models.BooleanField(help_text="*       clear = False | Checked = True")
    correct_answer_4 = models.BooleanField(help_text="*       clear = False | Checked = True")
    question_type = models.CharField(max_length=200, default='multiplechoice')
    quizfk = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.IntegerField(default='')
    dozent = models.CharField(max_length=200, default='')


    def __str__(self):
        return self.multi_question_text


class ProposeTFQuestion(models.Model):
    tf_question_text = models.CharField(max_length=200)
    true_or_false = models.BooleanField(default=False, help_text="*clear = False | Checked = True")
    quizfk = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=200, default='truefalse')
    user = models.IntegerField(default='')
    dozent = models.CharField(max_length=200, default='')


    def __str__(self):
        return self.tf_question_text