
from django.db import models
from django.utils.text import slugify


class Course(models.Model):

    class Level(models.TextChoices):
        BEGINNER = "BEGINNER", "Beginner"
        INTERMEDIATE = "INTERMEDIATE", "Intermediate"
        ADVANCED = "ADVANCED", "Advanced"

    language = models.ForeignKey(
        "languages.Language",
        on_delete=models.CASCADE,
        related_name="courses"
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True
    )

    description = models.TextField()

    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        default=Level.BEGINNER
    )

    thumbnail = models.ImageField(
        upload_to="courses/",
        blank=True,
        null=True
    )

    is_premium = models.BooleanField(default=False)

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["language", "level", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(
                f"{self.language.name}-{self.level}-{self.title}"
            )
            slug = base_slug
            counter = 1

            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.language.name} - {self.title}"

    @property
    def lesson_count(self):
        return self.lessons.filter(is_published=True).count()



class Lesson(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=220,
        blank=True
    )

    lesson_number = models.PositiveIntegerField()

    description = models.TextField(blank=True)

    content = models.TextField(blank=True)

    audio = models.FileField(
        upload_to="lesson_audio/",
        blank=True,
        null=True
    )

    duration_minutes = models.PositiveIntegerField(default=5)

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["lesson_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["course", "lesson_number"],
                name="unique_lesson_number_per_course"
            )
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.lesson_number}-{self.title}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.title} - Lesson {self.lesson_number}"


class Vocabulary(models.Model):

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="vocabulary"
    )

    word = models.CharField(max_length=120)

    pronunciation = models.CharField(
        max_length=150,
        blank=True
    )

    english = models.CharField(max_length=200)

    example = models.TextField(blank=True)

    example_translation = models.TextField(blank=True)

    audio = models.FileField(
        upload_to="vocabulary_audio/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["word"]

    def __str__(self):
        return f"{self.word} - {self.english}"
