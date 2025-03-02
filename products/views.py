from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from products.models import Product, Review, FavoriteProduct, Cart, ProductTag, ProductImage
from products.serializers import ProductSerializer, ReviewSerializer, FavoriteProductSerializer, CartSerializer, ProductTagSerializer, ProductImageSerializer
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.filters import SearchFilter 
from products.pagination import ProductPagination
from products.filters import ProductFilter
from rest_framework.viewsets import GenericViewSet


class ProductViewSet(ModelViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_class = [IsAuthenticated]
    pagination_class = ProductPagination 
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']


        
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_class = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating']

    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs['product_pk'])
    
    def perform_update(self, serializer):
        review = self.get_object()
        if review.user != self.request.user:
            raise PermissionDenied("You can't update this review.")
        serializer.save()
        
    
    def perform_destroy(self, instance):
        if instance.user!= self.request.user:
            raise PermissionDenied("You can't delete this review.")
        instance.delete()
    
    
    
    
    
class FavoriteProductViewSet(ModelViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_class = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']
    
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    

    
    
    

class CartViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_class = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset





class ProductTagViewSet(GenericViewSet, ListModelMixin):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_class = [IsAuthenticated]





class ProductImageViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_class = [IsAuthenticated]

    
    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs['product_pk'])