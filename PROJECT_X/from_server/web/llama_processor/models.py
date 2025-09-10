from django.db import models

class TextEntry(models.Model):
    text = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'TextEntry {self.id}'

class TextChunk(models.Model):
    text_entry = models.ForeignKey(TextEntry, 
                                 on_delete=models.CASCADE, 
                                 related_name='chunks')
    chunk_text = models.TextField()
    order = models.IntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ['text_entry', 'order']

    def __str__(self):
        return f"Chunk {self.order} of {self.text_entry}"

class Question(models.Model):
    text_chunk = models.ForeignKey(TextChunk,
                                 on_delete=models.CASCADE,
                                 related_name='questions')
    question_text = models.TextField()  # Changed to TextField

    def __str__(self):
        return self.question_text[:50]

class Answer(models.Model):
    question = models.ForeignKey(Question,
                               on_delete=models.CASCADE,
                               related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.answer_text[:20]} ({'✓' if self.is_correct else '✗'})"