
from django.urls import path
from . import views

app_name = "courses"
urlpatterns = [
    path("", views.course_list, name="list"),

    # Course management
    path("manage/create/", views.course_create, name="course_create"),
    path("manage/<slug:slug>/edit/", views.course_update, name="course_update"),
    path("manage/<slug:slug>/delete/", views.course_delete, name="course_delete"),
    path("manage/<slug:slug>/lessons/", views.manage_lessons, name="manage_lessons"),

    # Lesson management
    path("manage/<slug:course_slug>/lessons/create/", views.lesson_create, name="lesson_create"),
    path("manage/lessons/<int:pk>/edit/", views.lesson_update, name="lesson_update"),
    path("manage/lessons/<int:pk>/delete/", views.lesson_delete, name="lesson_delete"),

    # Vocabulary management
    path("manage/lessons/<int:lesson_pk>/vocabulary/", views.vocabulary_list, name="vocabulary_list"),
    path("manage/lessons/<int:lesson_pk>/vocabulary/create/", views.vocabulary_create, name="vocabulary_create"),
    path("manage/vocabulary/<int:pk>/edit/", views.vocabulary_update, name="vocabulary_update"),
    path("manage/vocabulary/<int:pk>/delete/", views.vocabulary_delete, name="vocabulary_delete"),

    # Public learning pages
    path("<slug:course_slug>/<slug:lesson_slug>/", views.lesson_detail, name="lesson"),
    path("<slug:slug>/", views.course_detail, name="detail"),
]