from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [

    # Course catalog
    path("", views.course_list, name="list"),


    # Instructor quiz management
    path(
        "instructor/quizzes/",
        views.instructor_quizzes,
        name="instructor_quizzes"
    ),

    path(
        "instructor/lessons/<int:lesson_id>/quiz/create/",
        views.quiz_create,
        name="quiz_create"
    ),

    path(
        "instructor/quizzes/<int:quiz_id>/edit/",
        views.quiz_update,
        name="quiz_update"
    ),

    path(
        "instructor/quizzes/<int:quiz_id>/delete/",
        views.quiz_delete,
        name="quiz_delete"
    ),

    # Learner progress
    path(
        "my-progress/",
        views.course_progress,
        name="course_progress"
    ),

    # Instructor dashboard
    path(
        "instructor/dashboard/",
        views.instructor_dashboard,
        name="instructor_dashboard"
    ),
    path(
        "instructor/courses/",
        views.instructor_courses,
        name="instructor_courses"
    ),

    # Course management
    path("manage/create/", views.course_create, name="course_create"),
    path("manage/<slug:slug>/edit/", views.course_update, name="course_update"),
    path("manage/<slug:slug>/delete/", views.course_delete, name="course_delete"),
    path("manage/<slug:slug>/lessons/", views.manage_lessons, name="manage_lessons"),

    # Lesson completion
    path(
        "<slug:course_slug>/<slug:lesson_slug>/complete/",
        views.mark_lesson_complete,
        name="mark_lesson_complete"
    ),

    # Public lesson
    path(
        "<slug:course_slug>/<slug:lesson_slug>/",
        views.lesson_detail,
        name="lesson"
    ),

    # Public course detail - KEEP LAST
    path("<slug:slug>/", views.course_detail, name="detail"),
]