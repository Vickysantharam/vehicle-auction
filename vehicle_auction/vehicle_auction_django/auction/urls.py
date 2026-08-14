from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('auction/<int:pk>/', views.auction_detail, name='auction_detail'),
    path('login/', views.login_register, name='login'),
    path('login/submit/', views.login_view, name='login_submit'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('post-auction/', views.post_auction, name='post_auction'),
    path('bid/<int:pk>/', views.place_bid, name='place_bid'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('my-auctions/', views.user_auctions, name='user_auctions'),
    path('my-bids/', views.user_bids, name='user_bids'),
    path('delete-auction/<int:pk>/', views.delete_auction, name='delete_auction'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # Admin
    path('admin-panel/login/', views.admin_login, name='admin_login'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/logout/', views.admin_logout, name='admin_logout'),
    path('admin-panel/delete-auction/<int:pk>/', views.admin_delete_auction, name='admin_delete_auction'),
    path('admin-panel/delete-user/<int:pk>/', views.admin_delete_user, name='admin_delete_user'),
    path('admin-panel/delete-bid/<int:pk>/', views.admin_delete_bid, name='admin_delete_bid'),
    path('admin-panel/toggle-featured/<int:pk>/', views.admin_toggle_featured, name='admin_toggle_featured'),
]
