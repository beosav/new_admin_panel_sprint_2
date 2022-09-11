import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class RoleType(models.TextChoices):
    ACTOR = 'actor', _('actor')
    DIRECTOR = 'director', _('director')
    WRITER = 'writer', _('writer')


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('tv_show')


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation_date'), blank=True, null=True)
    certificate = models.TextField(_('certificate'), blank=True, null=True)
    file_path = models.FileField(_('FilePath'), blank=True, upload_to='film_works/')
    rating = models.FloatField(_('rating'), default=0.0,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(10)])

    type = models.CharField(_('FilmType'), max_length=20, choices=FilmworkType.choices)
    genres = models.ManyToManyField('Genre', through='GenreFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film')
        verbose_name_plural = _('films')
        managed = False

    def __str__(self):
        return self.title


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        managed = False

    def __str__(self):
        return self.name


class GenreFilmwork(UUIDMixin):
    filmwork = models.ForeignKey('Filmwork', on_delete=models.CASCADE, db_column='film_work_id')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, db_column='genre_id')
    created = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('GenreFilm')
        verbose_name_plural = _('GenresFilms')
        managed = False
        constraints = [
            models.UniqueConstraint(fields=['filmwork', 'genre_id'], name='film_work_genre')
        ]

    def __str__(self):
        return f'{self.filmwork} - {self.genre}'


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('FIO'), validators=[MinLengthValidator(3)], max_length=200)
    birth_date = models.DateField(_('birth_date'), null=True, blank=True)


    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        managed = False

    def __str__(self):
        return self.full_name


class PersonFilmWork(UUIDMixin):
    filmwork = models.ForeignKey('Filmwork', on_delete=models.CASCADE, to_field='id', db_column='film_work_id')
    person = models.ForeignKey('Person', on_delete=models.CASCADE, to_field='id')
    role = models.TextField('role', null=True, choices=RoleType.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('person and role')
        verbose_name_plural = _('persons and roles')
        constraints = [
            models.UniqueConstraint(fields=['filmwork', 'person_id', 'role'], name='film_work_person_role')
        ]

        managed = False

    def __str__(self):
        return str(f'{self.filmwork} - {self.person}')
