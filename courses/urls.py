
from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("", views.course_list, name="list"),

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

    # Keep your other lesson and vocabulary management routes here.

    # Public routes must remain last
    path("<slug:course_slug>/<slug:lesson_slug>/", views.lesson_detail, name="lesson"),
    path("<slug:slug>/", views.course_detail, name="detail"),


    path(
    "<slug:course_slug>/<slug:lesson_slug>/complete/",
    views.mark_lesson_complete,
    name="mark_lesson_complete"
    ),
    path(
        "<slug:course_slug>/<slug:lesson_slug>/",
        views.lesson_detail,
        name="lesson"
    ),
]