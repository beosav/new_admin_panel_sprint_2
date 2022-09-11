from django.contrib import admin
from .models import GenreFilmwork, PersonFilmWork, Filmwork, Person, Genre
from django.utils.translation import gettext_lazy as _


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 0
    verbose_name = _('genre')
    autocomplete_fields = ('genre',)


class PersonRoleInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 0
    verbose_name = _('role')
    autocomplete_fields = ('person_id',)
    # raw_id_fields = ['person_id']


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_filter = ('type', )
    search_fields = ('id', 'title', 'description')
    list_display = ('title', 'type', 'creation_date', 'rating')
    fields = (
        'title', 'type', 'description', 'creation_date', 'certificate',
        'file_path', 'rating'
    )
    empty_value_display = _('empty')
    inlines = (GenreFilmworkInline, PersonRoleInline)
    ordering = ('title',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name', 'birth_date', 'id')
    list_display = ('full_name', 'birth_date', 'created', 'modified')
    empty_value_display = _('empty')
    ordering = ('full_name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')
