from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import FormReview, FormComment, ContactForm
from django.db.models import Avg, Min, Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def return_movie(film):
    get_movie_list = Film.objects.filter(Q(available=True) & Q(category__title=film)).order_by('-id')[:6]

    return get_movie_list


def home_page(request):
    film_genres = Genre.objects.all()
    films = return_movie('Movies')
    short_movies = return_movie('Short film')
    documentaries = return_movie('Documentaries')
    cartoons = return_movie('Cartoons')
    editor_films = Film.objects.filter(
        Q(available=True) & Q(editor_choice=True)
    )
    unavailable = Film.objects.exclude(available=True)[:6]

    return render(request, 'pages/index.html',
                  {
                      'editor_choice': editor_films, 'films': films,
                      'short_movies': short_movies, 'documentaries': documentaries,
                      'cartoons': cartoons, 'unavailable': unavailable, 'film_genres': film_genres,
                  })


def film_list_category(request, category_slug):
    category_obj = get_object_or_404(Category, slug=category_slug)
    filtered_films = Film.objects.filter(category=category_obj).order_by('-id')
    genres = Genre.objects.filter(film__in=filtered_films).distinct()
    films_years = Film.objects.all().values_list('release_year', flat=True)
    unavailable = Film.objects.exclude(available=True)[:6]
    paginator = Paginator(filtered_films, 6)
    page_number = request.GET.get('page')
    year_min = filtered_films.aggregate(Min('release_year')).get('release_year__min')
    year_max = filtered_films.aggregate(Max('release_year')).get('release_year__max')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'catalogs/films_catalog.html', {'selected': category_obj,
                                                           'genres': genres,
                                                           'films_years': films_years,
                                                           'unavailable': unavailable,
                                                           'page_obj': page_obj,
                                                           'year_min': year_min,
                                                           'year_max': year_max})


def film_list_genre(request, pk, slug):
    genre_obj = get_object_or_404(Genre, id=pk)
    category_obj = get_object_or_404(Category, slug=slug)
    filtered_films = Film.objects.filter(genre=genre_obj).filter(category=category_obj).order_by('-id')
    genres = Genre.objects.filter(film__in=filtered_films).distinct()
    films_years = Film.objects.all().values_list('release_year', flat=True)
    unavailable = Film.objects.exclude(available=True)[:6]
    paginator = Paginator(filtered_films, 6)
    page_number = request.GET.get('page')
    year_min = filtered_films.aggregate(Min('release_year')).get('release_year__min')
    year_max = filtered_films.aggregate(Max('release_year')).get('release_year__max')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'catalogs/films_catalog.html', {'page_obj': page_obj,
                                                           'selected': category_obj,
                                                           'genres': genres,
                                                           'selected_genre': genre_obj,
                                                           'films_years': films_years,
                                                           'unavailable': unavailable,
                                                           'year_min': year_min,
                                                           'year_max': year_max})


def detail_page(request, film_slug):
    film = get_object_or_404(Film, slug=film_slug)
    film_stills = film.stills_set.all()
    film_review = film.reviews.all()
    film_comment = film.comment_set.filter(parent__isnull=True)
    genres = Genre.objects.filter(film=film)
    films_may_like = Film.objects.exclude(id=film.id).filter(genre__in=genres).distinct()[0:6]
    selected_flag = ""

    if request.user in film.selected.all():
        selected_flag = "add"
    elif request.user not in film.selected.all():
        selected_flag = "remove"

    return render(request, 'pages/details.html', {'film': film, 'film_stills': film_stills, 'genres': genres,
                                                  'film_review': film_review, "film_comment": film_comment,
                                                  'films_may_like': films_may_like, 'selected_flag': selected_flag, })


def add_review_or_comment(request, film_slug):
    film = get_object_or_404(
        Film,
        slug=film_slug
    )

    if request.method == "POST" and 'review_button' in request.POST:
        form = FormReview(request.POST)

        if form.is_valid():
            rf = form.cleaned_data
            author = "guest"
            current_user = None

            if request.user.is_authenticated:
                author = request.user.username
                current_user = request.user

            if request.POST.get("review_update"):
                review_update = Review.objects.get(id=int(request.POST.get("review_update")))
                if request.user == review_update.user:
                    form = FormReview(request.POST, instance=review_update)
                    form.save()
                return redirect(film.get_absolute_url())

            Review.objects.create(
                user=current_user,
                film=film,
                author=author,
                review=rf['review'],
                title=rf['title'],
                rating=float(rf['rating'])
            )
            return redirect(film.get_absolute_url())

    if request.method == "POST" and 'comment_button' in request.POST:
        form_com = FormComment(request.POST)

        if form_com.is_valid():
            cf = form_com.cleaned_data
            author = "guest"
            current_user = None

            if request.user.is_authenticated:
                author = request.user.username
                current_user = request.user

            if request.POST.get("top_comment_up"):
                parent = int(request.POST.get("top_comment_up"))
                Comment.objects.create(
                    film=film,
                    user=current_user,
                    author=author,
                    comment=cf['comment'],
                    parent_id=parent,
                )
                return redirect(film.get_absolute_url())

            if request.POST.get("comment_update"):
                comment_to_update = Comment.objects.get(id=int(request.POST.get("comment_update")))
                if request.user == comment_to_update.user:
                    form = FormComment(request.POST, instance=comment_to_update)
                    form.save()
                return redirect(film.get_absolute_url())

            cf = form_com.cleaned_data
            Comment.objects.create(
                user=current_user,
                film=film,
                author=author,
                comment=cf['comment'],
            )
            return redirect(film.get_absolute_url())


@login_required(login_url='login')
def delete_comment(request, pk, slug):
    film = Film.objects.get(slug=slug)
    comment_to_delete = get_object_or_404(Comment, id=pk)
    if request.method == 'POST' and comment_to_delete.user == request.user:
        comment_to_delete.delete()
        return redirect(film.get_absolute_url())

    return render(request, 'pages/delete.html', {'film': film, 'object_to_delete': comment_to_delete, })


@login_required(login_url='/accounts/signin/')
def delete_review(request, pk, slug):
    film = Film.objects.get(slug=slug)
    review_to_delete = get_object_or_404(Review, id=pk)
    if request.method == 'POST' and review_to_delete.user == request.user:
        review_to_delete.delete()
        return redirect(film.get_absolute_url())

    return render(request, 'pages/delete.html', {'film': film, 'object_to_delete': review_to_delete, })


@require_POST
@login_required(login_url='/accounts/signin/')
def comments_likes_or_dislike(request):
    if request.POST.get('action') == 'post':
        json_dislike = ''
        json_like = ''
        comment_id = int(request.POST.get('comment_id'))
        comment = get_object_or_404(Comment, id=comment_id)

        if request.POST.get('flag') == 'like':
            if comment.likes.filter(id=request.user.id).exists():
                comment.likes.remove(request.user)
                json_like = comment.likes.count()
                json_dislike = comment.dislikes.count()
                comment.save()
            elif comment.dislikes.filter(id=request.user.id).exists():
                comment.dislikes.remove(request.user)
                comment.likes.add(request.user)
                json_like = comment.likes.count()
                json_dislike = comment.dislikes.count()
                comment.save()
            else:
                comment.likes.add(request.user)
                json_like = comment.likes.count()
                json_dislike = comment.dislikes.count()
                comment.save()

        if request.POST.get('flag') == 'dislike':
            if comment.dislikes.filter(id=request.user.id).exists():
                comment.dislikes.remove(request.user)
                json_like = comment.likes.count()
                json_dislike = comment.dislikes.count()
                comment.save()
            elif comment.likes.filter(id=request.user.id).exists():
                comment.likes.remove(request.user)
                comment.dislikes.add(request.user)
                json_like = comment.likes.count()
                json_dislike = comment.dislikes.count()
                comment.save()
            else:
                comment.dislikes.add(request.user)
                json_like = comment.likes.count()
                json_dislike = comment.dislikes.count()
                comment.save()

        return JsonResponse({'json_like': json_like, 'json_dislike': json_dislike})


@require_POST
@login_required(login_url='/accounts/signin/')
def review_likes_or_dislike(request):
    if request.POST.get('action') == 'post':
        json_dislike = ''
        json_like = ''
        review_id = int(request.POST.get('review_id'))
        review = get_object_or_404(Review, id=review_id)

        if request.POST.get('flag') == 'like':
            if review.likes.filter(id=request.user.id).exists():
                review.likes.remove(request.user)
                json_like = review.likes.count()
                json_dislike = review.dislikes.count()
                review.save()
            elif review.dislikes.filter(id=request.user.id).exists():
                review.dislikes.remove(request.user)
                review.likes.add(request.user)
                json_like = review.likes.count()
                json_dislike = review.dislikes.count()
                review.save()
            else:
                review.likes.add(request.user)
                json_like = review.likes.count()
                json_dislike = review.dislikes.count()
                review.save()

        if request.POST.get('flag') == 'dislike':
            if review.dislikes.filter(id=request.user.id).exists():
                review.dislikes.remove(request.user)
                json_like = review.likes.count()
                json_dislike = review.dislikes.count()
                review.save()
            elif review.likes.filter(id=request.user.id).exists():
                review.likes.remove(request.user)
                review.dislikes.add(request.user)
                json_like = review.likes.count()
                json_dislike = review.dislikes.count()
                review.save()
            else:
                review.dislikes.add(request.user)
                json_like = review.likes.count()
                json_dislike = review.dislikes.count()
                review.save()

        return JsonResponse({'json_like': json_like, 'json_dislike': json_dislike})


def search_result(request):
    query_search = ""
    if request.method == 'POST':
        query_search = request.POST['search_query']

    if request.method == 'GET':
        query_search = request.GET['search_result']

    result_movie = Film.objects.filter(title__icontains=query_search).order_by('-id')
    paginator = Paginator(result_movie, 12)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    if page_obj:
        return render(request, 'catalogs/result_catalog.html', {'page_obj': page_obj, 'query_search': query_search})
    else:
        return render(request, 'catalogs/result_catalog.html', {'message': "Sorry no results were found"})


def filter_films(request):
    year_min = Film.objects.all().aggregate(Min('release_year')).get('release_year__min')
    year_max = Film.objects.all().aggregate(Max('release_year')).get('release_year__max')

    if request.method == "GET":
        selected_genre = None
        category = Category.objects.all()
        films = Film.objects.all()
        unavailable = Film.objects.exclude(available=True)[:6]

        if request.GET.get('selected'):
            category = category.get(id=request.GET.get('selected'))
            films = films.filter(category=category)
            genres = Genre.objects.filter(film__in=films).distinct()

        if request.GET.get('selected_genre'):
            selected_genre = Genre.objects.get(title=request.GET.get('selected_genre'))
            films = films.filter(genre=selected_genre)

        if request.GET.get('ratings_start'):
            rating_start = float(request.GET.get('ratings_start'))
            rating_end = float(request.GET.get('ratings_end'))

            def check_rating(x):
                if rating_start <= x.get_average_rating() <= rating_end:
                    return x

            films_to_check = filter(check_rating, films)
            films = films.filter(title__in=films_to_check)

            # films = films.annotate(avg_rat=Avg('reviews__rating')).filter(avg_rat__range=(rating_start, rating_end))

        if request.GET.get('years_start'):
            year_start = request.GET.get('years_start')
            year_end = request.GET.get('years_end')
            films = films.filter(release_year__range=(year_start, year_end))

        films = films.order_by('-id')
        paginator = Paginator(films, 6)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(request, 'catalogs/films_catalog.html', {'page_obj': page_obj, 'selected': category,
                                                               'genres': genres, 'selected_genre': selected_genre,
                                                               'ratings_start': rating_start, 'ratings_end': rating_end,
                                                               'years_start': year_start, 'years_end': year_end,
                                                               'unavailable': unavailable, 'year_min': year_min,
                                                               'year_max': year_max
                                                               })


def about_page(request):
    return render(request, 'pages/about.html')


def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'pages/contacts.html')


def privacy_page(request):
    return render(request, 'pages/privacy.html')


@require_POST
@login_required(login_url='/accounts/signin/')
def selected_movie(request):

    if request.POST.get('action') == 'post':
        film_id = int(request.POST.get('movie_id'))
        film = get_object_or_404(Film, id=film_id)
        flag = request.POST.get('flag')

        if request.POST.get('flag') == 'add' and film.selected.filter(id=request.user.id).exists():
            film.selected.remove(request.user)
            film.save()
            flag = 'remove'

        if request.POST.get('flag') == 'remove':
            film.selected.add(request.user)
            flag = 'add'
            film.save()

    return JsonResponse({'selected': flag, })
