from django.contrib import admin

# Register your models here.

from .models import Quiz,Lobby,UserInLobby,EssayQuestion,TFQuestion,MultipleChoiceQuestion,ProposeEssayQuestion,ProposeMultipleChoiceQuestion,ProposeTFQuestion,MultiplayerErgebnis,Ergebnis,Course

admin.site.register(Quiz)
admin.site.register(Lobby)
admin.site.register(UserInLobby)
admin.site.register(EssayQuestion)
admin.site.register(TFQuestion)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(ProposeMultipleChoiceQuestion)
admin.site.register(ProposeTFQuestion)
admin.site.register(ProposeEssayQuestion)
admin.site.register(MultiplayerErgebnis)
admin.site.register(Course)
admin.site.register(Ergebnis)
