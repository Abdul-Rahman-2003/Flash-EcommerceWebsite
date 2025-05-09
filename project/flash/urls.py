from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_page, name="logout"),
    path('cart', views.cart_page, name="cart"),
    path('fav', views.fav_page, name="fav"),
    path('favviewpage', views.favviewpage, name="favviewpage"),
    path('remove_cart/<str:cid>', views.remove_cart, name="remove_cart"),
    path('remove_fav/<str:fid>', views.remove_fav, name="remove_fav"),
    path("collections/", views.collections, name="collections"),
    path('collections/<slug:cname>', views.collectionsview, name="collections_view"),
    path('collections/<slug:cname>/<slug:slug>/', views.product_details, name="product_details"),
    path('addtocart', views.add_to_cart, name="addtocart"),
    path('search/', views.search_view, name="search"),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('men', views.category_products_men, name="category_products_men"),
    path('women', views.category_products_women, name="category_products_women"),
    path('kid', views.category_products_kid, name="category_products_kid"),
    path('bestseller',views.bestseller,name="bestseller"),
    path('upcoming',views.upcoming,name="upcoming"),
    path('arrival',views.arrival,name="arrival"),

]
