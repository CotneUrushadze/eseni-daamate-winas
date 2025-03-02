from rest_framework import serializers
from products.models import Review, Product, FavoriteProduct, Cart, ProductTag, ProductImage



class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = [ 'id', 'product_id', 'content', 'rating']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data.pop('product_id'))
        user = self.context['request'].user
        existing_review = Review.objects.filter(product=product, user=user)
        if existing_review.exists():
            raise serializers.ValidationError("you has already reviewed this product nigga.")
        
        return Review.objects.create(product=product, user=user, **validated_data)






class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        exclude = ['created_at', 'updated_at', 'tags'] 
        model = Product


    
    
    
class FavoriteProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = FavoriteProduct
        fields = ['id', 'user', 'product', 'product_id'] 
        read_only_fields = ['id', 'product'] 

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("product with given id not found")
        return value
    
    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        user = validated_data.pop('user')
        
        product = Product.objects.get(id=product_id)
        
        favorite, created = FavoriteProduct.objects.get_or_create(user=user, product=product)
        
        if not created:
            raise serializers.ValidationError("this product is already in favorites")
        
        
        
    
    
    
class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    products = ProductSerializer(many=True, read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source = 'products',
        queryset = Product.objects.all(),
        many=True,
        write_only=True
    )
    
    class Meta:
        model = Cart
        fields = ['user', 'product_id', 'products'] 

    def create(self, validated_data):
        user = validated_data.pop('user')
        products = validated_data.pop('products')
        
        cart, _ =Cart.objects.get_or_create(user=user)
        cart.products.add(*products)
        
        return cart
    


class ProductTagSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ['name'] 
        model = ProductTag



    
class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'product'] 
