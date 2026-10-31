
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch

from .models import Course, Lesson, Vocabulary
from .forms import CourseForm, LessonForm, VocabularyForm
from django import forms


# -----------------------------------------
# ACCESS CONTROL
# -----------------------------------------

def is_content_manager(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.is_staff
            or getattr(user, "role", None) == "INSTRUCTOR"
        )
    )


content_manager_required = user_passes_test(
    is_content_manager,
    login_url="accounts:login"
)


# -----------------------------------------
# COURSE CATALOG
# -----------------------------------------

def course_list(request):

    courses = Course.objects.filter(
        is_published=True
    ).select_related("language")

    languages = Course.objects.filter(
        is_published=True
    ).values(
        "language__name",
        "language__slug"
    ).distinct()

    language_slug = request.GET.get("language")

    if language_slug:
        courses = courses.filter(
            language__slug=language_slug
        )

    context = {
        "courses": courses,
        "languages": languages,
    }

    return render(
        request,
        "courses/course_list.html",
        context
    )


# -----------------------------------------
# COURSE DETAIL
# -----------------------------------------

def course_detail(request, slug):

    course = get_object_or_404(
        Course.objects.select_related("language"),
        slug=slug,
        is_published=True
    )

    lessons = course.lessons.filter(
        is_published=True
    )

    context = {
        "course": course,
        "lessons": lessons,
    }

    return render(
        request,
        "courses/course_detail.html",
        context
    )


# -----------------------------------------
# LESSON DETAIL
# -----------------------------------------

@login_required
def lesson_detail(request, course_slug, lesson_slug):

    course = get_object_or_404(
        Course,
        slug=course_slug,
        is_published=True
    )

    lesson = get_object_or_404(
        Lesson,
        course=course,
        slug=lesson_slug,
        is_published=True
    )

    vocabulary = lesson.vocabulary.all()

    next_lesson = course.lessons.filter(
        is_published=True,
        lesson_number__gt=lesson.lesson_number
    ).order_by("lesson_number").first()

    previous_lesson = course.lessons.filter(
        is_published=True,
        lesson_number__lt=lesson.lesson_number
    ).order_by("-lesson_number").first()

    return render(
        request,
        "courses/lesson_detail.html",
        {
            "course": course,
            "lesson": lesson,
            "vocabulary": vocabulary,
            "next_lesson": next_lesson,
            "previous_lesson": previous_lesson,
        }
    )


# -----------------------------------------
# CREATE COURSE
# -----------------------------------------

@login_required
@content_manager_required
def course_create(request):

    if request.method == "POST":
        form = CourseForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            course = form.save()

            messages.success(
                request,
                "Course created successfully."
            )

            return redirect(
                "courses:manage_lessons",
                slug=course.slug
            )

    else:
        form = CourseForm()

    return render(
        request,
        "courses/course_form.html",
        {"form": form}
    )


# -----------------------------------------
# UPDATE COURSE
# -----------------------------------------

@login_required
@content_manager_required
def course_update(request, slug):

    course = get_object_or_404(
        Course,
        slug=slug
    )

    if request.method == "POST":
        form = CourseForm(
            request.POST,
            request.FILES,
            instance=course
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Course updated successfully."
            )

            return redirect(
                "courses:course_update",
                slug=course.slug
            )

    else:
        form = CourseForm(instance=course)

    return render(
        request,
        "courses/course_form.html",
        {
            "form": form,
            "course": course,
        }
    )


# -----------------------------------------
# DELETE COURSE
# -----------------------------------------

@login_required
@content_manager_required
def course_delete(request, slug):

    course = get_object_or_404(
        Course,
        slug=slug
    )

    if request.method == "POST":
        course.delete()

        messages.success(
            request,
            "Course deleted successfully."
        )

        return redirect("courses:course_list")

    return render(
        request,
        "courses/course_confirm_delete.html",
        {"course": course}
    )


# -----------------------------------------
# MANAGE LESSONS
# -----------------------------------------

@login_required
@content_manager_required
def manage_lessons(request, slug):

    course = get_object_or_404(
        Course,
        slug=slug
    )

    lessons = course.lessons.all()

    return render(
        request,
        "courses/manage_lessons.html",
        {
            "course": course,
            "lessons": lessons,
        }
    )


# -----------------------------------------
# CREATE LESSON
# -----------------------------------------

@login_required
@content_manager_required
def lesson_create(request, course_slug):

    course = get_object_or_404(
        Course,
        slug=course_slug
    )

    if request.method == "POST":
        form = LessonForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()

            messages.success(
                request,
                "Lesson created successfully."
            )

            return redirect(
                "courses:manage_lessons",
                slug=course.slug
            )

    else:
        form = LessonForm(initial={
            "course": course
        })

    # Course is selected through the URL, not the form.
    form.fields["course"].widget = forms.HiddenInput()

    return render(
        request,
        "courses/lesson_form.html",
        {
            "form": form,
            "course": course,
        }
    )


# -----------------------------------------
# UPDATE LESSON
# -----------------------------------------

@login_required
@content_manager_required
def lesson_update(request, pk):

    lesson = get_object_or_404(
        Lesson,
        pk=pk
    )

    if request.method == "POST":
        form = LessonForm(
            request.POST,
            request.FILES,
            instance=lesson
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Lesson updated successfully."
            )

            return redirect(
                "courses:manage_lessons",
                slug=lesson.course.slug
            )

    else:
        form = LessonForm(instance=lesson)

    return render(
        request,
        "courses/lesson_form.html",
        {
            "form": form,
            "course": lesson.course,
            "lesson": lesson,
        }
    )


# -----------------------------------------
# DELETE LESSON
# -----------------------------------------

@login_required
@content_manager_required
def lesson_delete(request, pk):

    lesson = get_object_or_404(
        Lesson,
        pk=pk
    )

    course_slug = lesson.course.slug

    if request.method == "POST":
        lesson.delete()

        messages.success(
            request,
            "Lesson deleted successfully."
        )

        return redirect(
            "courses:manage_lessons",
            slug=course_slug
        )

    return render(
        request,
        "courses/lesson_confirm_delete.html",
        {"lesson": lesson}
    )


# -----------------------------------------
# CREATE VOCABULARY
# -----------------------------------------

@login_required
@content_manager_required
def vocabulary_create(request, lesson_pk):

    lesson = get_object_or_404(
        Lesson,
        pk=lesson_pk
    )

    if request.method == "POST":
        form = VocabularyForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            vocabulary = form.save(commit=False)
            vocabulary.lesson = lesson
            vocabulary.save()

            messages.success(
                request,
                "Vocabulary added successfully."
            )

            return redirect(
                "courses:vocabulary_list",
                lesson_pk=lesson.pk
            )

    else:
        form = VocabularyForm(initial={
            "lesson": lesson
        })

    form.fields["lesson"].widget = forms.HiddenInput()

    return render(
        request,
        "courses/vocabulary_form.html",
        {
            "form": form,
            "lesson": lesson,
        }
    )


# -----------------------------------------
# LIST VOCABULARY
# -----------------------------------------

@login_required
@content_manager_required
def vocabulary_list(request, lesson_pk):

    lesson = get_object_or_404(
        Lesson,
        pk=lesson_pk
    )

    vocabulary = lesson.vocabulary.all()

    return render(
        request,
        "courses/vocabulary_list.html",
        {
            "lesson": lesson,
            "vocabulary": vocabulary,
        }
    )


# -----------------------------------------
# UPDATE VOCABULARY
# -----------------------------------------

@login_required
@content_manager_required
def vocabulary_update(request, pk):

    vocabulary = get_object_or_404(
        Vocabulary,
        pk=pk
    )

    if request.method == "POST":
        form = VocabularyForm(
            request.POST,
            request.FILES,
            instance=vocabulary
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Vocabulary updated successfully."
            )

            return redirect(
                "courses:vocabulary_list",
                lesson_pk=vocabulary.lesson.pk
            )

    else:
        form = VocabularyForm(instance=vocabulary)

    return render(
        request,
        "courses/vocabulary_form.html",
        {
            "form": form,
            "lesson": vocabulary.lesson,
            "vocabulary": vocabulary,
        }
    )


# -----------------------------------------
# DELETE VOCABULARY
# -----------------------------------------

@login_required
@content_manager_required
def vocabulary_delete(request, pk):

    vocabulary = get_object_or_404(
        Vocabulary,
        pk=pk
    )

    lesson_pk = vocabulary.lesson.pk

    if request.method == "POST":
        vocabulary.delete()

        messages.success(
            request,
            "Vocabulary deleted successfully."
        )

    return redirect(
        "courses:vocabulary_list",
        lesson_pk=lesson_pk
    )
