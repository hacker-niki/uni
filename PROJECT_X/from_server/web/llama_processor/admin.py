from django.contrib import admin
from .models import TextEntry, TextChunk, Question, Answer

@admin.register(TextEntry)
class TextEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_at')
    ordering = ('-uploaded_at',)

@admin.register(TextChunk)
class TextChunkAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_entry', 'order')
    list_filter = ('text_entry',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_chunk', 'question_text')
    search_fields = ('question_text',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer_text', 'is_correct')
    list_filter = ('is_correct',)