from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork, RoleType as PersonRoleChoices


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']
    
    @staticmethod
    def get_person_aggregation(role: PersonRoleChoices):
        return ArrayAgg(
            'personfilmwork__role',
            filter=Q(personfilmwork__role=str(role)),
            distinct=True
        )    

    def get_queryset(self):
        film_works = (
            Filmwork.objects.prefetch_related(
                'genres', 'persons').order_by('title')
        )
        queryset = film_works.values(
            'id', 'title', 'description', 'creation_date', 'rating', 'type'
        ).annotate(
            genres=ArrayAgg(
                'genres__name',
                distinct=True
            ),

            actors = MoviesApiMixin.get_person_aggregation(PersonRoleChoices.ACTOR),
            directors = MoviesApiMixin.get_person_aggregation(PersonRoleChoices.DIRECTOR),
            writers = MoviesApiMixin.get_person_aggregation(PersonRoleChoices.WRITER)

        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': None if page.number == 1 else page.previous_page_number(),
            'next': None if paginator.num_pages == page.number
            else page.next_page_number(),
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return kwargs['object'] 