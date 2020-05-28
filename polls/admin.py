from django.contrib import admin
from .models import Question, Choice
# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    #fields = ['question_text','pub_date',]
    list_display = ('question_text','pub_date','was_published_recently')
    search_fields = ['question_text']
    list_filter = ['question_text','pub_date']
    fieldsets = [
        ("Question information", {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date",]}),
    
    ]
    inlines = [ChoiceInline]

admin.site.register(Question,QuestionAdmin)
