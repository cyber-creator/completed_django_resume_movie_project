from datetime import date

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    title = models.CharField("Category", max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('films:films_catalog_category', args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Film_Category"
        verbose_name_plural = "Films_Categories"


class Genre(models.Model):
    title = models.CharField("Genres", max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    # def get_absolute_url(self):
    #     return reverse('films:films_catalog_genre', args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Actors(models.Model):
    name = models.CharField("Name", max_length=50)
    biography = models.TextField("Biography")
    age = models.PositiveSmallIntegerField("Age")
    photo = models.ImageField("Photo", upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Actor and Director"
        verbose_name_plural = "Actors and Directors"


class Film(models.Model):
    title = models.CharField("Film", max_length=50)
    poster = models.ImageField("Poster", upload_to="films/")
    genre = models.ManyToManyField(Genre, verbose_name="genre")
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.SET_NULL, null=True)
    plot = models.TextField("Film_plot")
    release_year = models.SmallIntegerField("Release Year", default=2020)
    running_time = models.SmallIntegerField("Running time", default=100)
    country = models.CharField("Country", max_length=50)
    actors = models.ManyToManyField(Actors, verbose_name="Film actors", related_name="film_actor")
    directors = models.ManyToManyField(Actors, verbose_name="Film directors", related_name="film_director")
    slug = models.SlugField(max_length=50, unique=True)
    date_added = models.DateField("Movie added", default=date.today)
    editor_choice = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    video = models.FileField("video", upload_to="video/", default="video/unavailable.mp4")
    selected = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='movies_selected')

    def get_absolute_url(self):
        return reverse('films:detail_page', args=[self.slug])

    def get_average_rating(self):
        average_score = 0.0
        if self.reviews.count() > 0:
            total_score = sum([review.rating for review in self.reviews.all()])
            average_score = total_score / self.reviews.count()

        return round(average_score, 1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Films"


class Stills(models.Model):
    title = models.CharField("title", max_length=50)
    stills = models.ImageField("photo", upload_to="stills/")
    films = models.ForeignKey(Film, verbose_name="film", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "still"
        verbose_name_plural = "stills"


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', blank=True,
                             null=True)
    author = models.CharField("Author", max_length=50)
    comment = models.TextField("Comment", max_length=2000)
    film = models.ForeignKey(Film, verbose_name="Comment", on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', related_name='Parent', on_delete=models.SET_NULL,
                               blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='comments_likes')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='comments_dislike')

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ('-posted_date',)


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', blank=True,
                             null=True)
    film = models.ForeignKey(Film, related_name="reviews", verbose_name="Review", on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    review = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='review_likes')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='review_dislike')

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ('-created',)


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.email
