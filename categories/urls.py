from django.urls import path
from categories.views import CategoryImageViewSet, CategoryListView, CategoryDetailView


urlpatterns = [
    path('categories/', CategoryListView.as_view({'get': 'list'}), name='category-list'),
    path('categories/<int:pk>', CategoryDetailView.as_view({'get': 'retrieve'}), name='category-detail'),
    path('categories/<int:category_id>/images/', CategoryImageViewSet.as_view({'get': 'list', 'post':'create'}), name='category-images'),
]
