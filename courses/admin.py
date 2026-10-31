
from django.contrib import admin
from .models import Course, Lesson, Vocabulary


class VocabularyInline(admin.TabularInline):
    model = Vocabulary
    extra = 1


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    show_change_link = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "language",
        "level",
        "lesson_count",
        "is_premium",
        "is_published",
    )

    list_filter = (
        "language",
        "level",
        "is_premium",
        "is_published",
    )

    search_fields = (
        "title",
        "description",
        "language__name",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "lesson_number",
        "duration_minutes",
        "is_published",
    )

    list_filter = (
        "course",
        "is_published",
    )

    search_fields = (
        "title",
        "course__title",
    )

    inlines = [VocabularyInline]


@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = (
        "word",
        "english",
        "lesson",
    )

    search_fields = (
        "word",
        "english",
    )
