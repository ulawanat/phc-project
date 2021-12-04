from django.urls import path
from products.views import create, detail, upvote, SearchResultsView

urlpatterns = [
    path('create/', create, name='create'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('<int:product_id>/', detail, name='detail'),
    path('<int:product_id>/upvote', upvote, name='upvote')
]


