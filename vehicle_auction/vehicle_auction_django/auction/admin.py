from django.contrib import admin
from .models import Auction, Bid, UserProfile, ContactMessage

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['title', 'current_bid', 'featured', 'created_by', 'created_at']
    list_filter = ['featured', 'is_active']
    search_fields = ['title']

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['auction', 'bidder', 'bid_amount', 'created_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
