
from django import forms
from .models import Course, Lesson, Vocabulary


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = [
            "language",
            "title",
            "description",
            "level",
            "thumbnail",
            "is_premium",
            "is_published",
        ]

        widgets = {
            "language": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter course title"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),
            "level": forms.Select(attrs={"class": "form-select"}),
            "thumbnail": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "is_premium": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            "is_published": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }


class LessonForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = [
            "course",
            "title",
            "lesson_number",
            "description",
            "content",
            "audio",
            "duration_minutes",
            "is_published",
        ]

        widgets = {
            "course": forms.Select(attrs={
                "class": "form-select",
            }),
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Basic Greetings",
            }),
            "lesson_number": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
                "placeholder": "Enter the lesson content...",
            }),
            "audio": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
            "duration_minutes": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
            }),
            "is_published": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }




class VocabularyForm(forms.ModelForm):

    class Meta:
        model = Vocabulary
        fields = [
            "lesson",
            "word",
            "pronunciation",
            "english",
            "example",
            "example_translation",
            "audio",
        ]

        widgets = {
            "lesson": forms.Select(attrs={
                "class": "form-select",
            }),
            "word": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter native language word",
            }),
            "pronunciation": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "How is it pronounced?",
            }),
            "english": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "English meaning",
            }),
            "example": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Example sentence...",
            }),
            "example_translation": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "English translation...",
            }),
            "audio": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
        }



