from django.urls import path
from django.views.generic import RedirectView
from reviewapp.views import IndexView, ProductsCreateView, ProductsView, ProductsUpdateView, ProductsDeleteView, \
    ReviewsCreateView, ReviewsUpdateView, ReviewsDeleteView

app_name = 'reviewapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('articles/', RedirectView.as_view(pattern_name='reviewapp:index')),
    path('articles/add/', ProductsCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/', ProductsView.as_view(), name='article_view'),
    path('article/<int:pk>/update/', ProductsUpdateView.as_view(), name='article_update_view'),
    path('article/<int:pk>/delete/', ProductsDeleteView.as_view(), name='article_delete_view'),
    path('article/<int:pk>/comment/add/', ReviewsCreateView.as_view(), name='comment_add'),
    path('comment/<int:pk>/update/', ReviewsUpdateView.as_view(), name='comment_update_view'),
    path('comment/<int:pk>/delete/', ReviewsDeleteView.as_view(), name='comment_delete_view'),
]

