
from django.contrib import admin
from .models import Course, Lesson, Vocabulary,LessonProgress, Quiz, Question, AnswerOption, QuizAttempt


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




@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = (
        "learner",
        "lesson",
        "is_completed",
        "completed_at",
        "updated_at",
    )
    list_filter = ("is_completed", "lesson__course")
    search_fields = (
        "learner__username",
        "lesson__title",
        "lesson__course__title",
    )
    readonly_fields = ("completed_at", "updated_at")




class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 3


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson", "pass_mark", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "lesson__title")
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "quiz", "points", "order")
    inlines = [AnswerOptionInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "learner", "quiz", "score",
        "total_points", "percentage", "passed", "completed_at"
    )
    list_filter = ("passed", "completed_at")
    search_fields = ("learner__username", "quiz__title")