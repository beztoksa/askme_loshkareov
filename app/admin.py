from django.contrib import admin
from app import models
from django.db.models import Count
# Register your models here.
admin.site.register(models.Answer)
admin.site.register(models.Profile)
admin.site.register(models.AnswerLike)
admin.site.register(models.QuestionLike)
@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'question_count')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(q_count=Count('question'))

    def question_count(self, obj):
        return obj.q_count
    question_count.short_description = 'Вопросов'
@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

