from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Auction, Bid, UserProfile, ContactMessage
import json


def index(request):
    featured = Auction.objects.filter(featured=True, is_active=True)
    return render(request, 'index.html', {'featured': featured})


def search(request):
    query = request.GET.get('query', '')
    results = Auction.objects.filter(title__icontains=query, is_active=True) if query else Auction.objects.filter(is_active=True)
    return render(request, 'search.html', {'results': results, 'query': query})


def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    bids = auction.bids.all().order_by('-bid_amount')[:10]
    return render(request, 'auction_detail.html', {'auction': auction, 'bids': bids})


def login_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'login.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with that email.')
        return redirect('login')
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('mnumber')
        password = request.POST.get('password')
        profile_pic = request.FILES.get('profilepic')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('login')

        user = User.objects.create_user(username=username, email=email, password=password)
        profile = UserProfile.objects.create(user=user, phone=phone)
        if profile_pic:
            profile.profile_pic = profile_pic
            profile.save()
        messages.success(request, 'Account created! Please login.')
        return redirect('login')
    return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def dashboard(request):
    featured = Auction.objects.filter(featured=True, is_active=True)
    all_auctions = Auction.objects.filter(is_active=True).order_by('-created_at')
    user_bids = Bid.objects.filter(bidder=request.user).select_related('auction').order_by('-created_at')
    return render(request, 'dashboard.html', {
        'featured': featured,
        'all_auctions': all_auctions,
        'user_bids': user_bids,
    })


@login_required
def post_auction(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        starting_bid = request.POST.get('starting_bid')
        image = request.FILES.get('image')
        featured = request.POST.get('featured') == 'on'

        auction = Auction.objects.create(
            title=title,
            current_bid=starting_bid,
            created_by=request.user,
            featured=featured,
        )
        if image:
            auction.image = image
            auction.save()
        return JsonResponse({'success': True, 'message': 'Auction posted!'})
    return render(request, 'post_auction.html')


@login_required
def place_bid(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            bid_amount = float(data.get('bid_amount', 0))
        except Exception:
            bid_amount = float(request.POST.get('bid_amount', 0))

        if bid_amount <= float(auction.current_bid):
            return JsonResponse({'success': False, 'message': f'Bid must be higher than current bid of ${auction.current_bid}'})

        Bid.objects.create(auction=auction, bidder=request.user, bid_amount=bid_amount)
        auction.current_bid = bid_amount
        auction.save()
        return JsonResponse({'success': True, 'message': 'Bid placed!', 'new_bid': str(bid_amount)})
    return redirect('auction_detail', pk=pk)


@login_required
def user_profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    return render(request, 'user_profile.html', {'profile': profile})


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.save()
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        profile.phone = request.POST.get('phone', profile.phone)
        if request.FILES.get('profile_pic'):
            profile.profile_pic = request.FILES['profile_pic']
        profile.save()
        messages.success(request, 'Profile updated!')
        return redirect('user_profile')
    return redirect('user_profile')


@login_required
def user_auctions(request):
    auctions = Auction.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'user_auctions.html', {'auctions': auctions})


@login_required
def user_bids(request):
    bids = Bid.objects.filter(bidder=request.user).select_related('auction').order_by('-created_at')
    return render(request, 'user_bids.html', {'bids': bids})


@login_required
def delete_auction(request, pk):
    auction = get_object_or_404(Auction, pk=pk, created_by=request.user)
    auction.delete()
    messages.success(request, 'Auction deleted.')
    return redirect('user_auctions')


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            message=request.POST.get('message'),
        )
        messages.success(request, 'Message sent! We will contact you shortly.')
        return redirect('contact')
    return render(request, 'contact.html')


# Admin views
def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == 'admin@gmail.com' and password == '123':
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        try:
            user_obj = User.objects.get(email=email, is_staff=True)
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                request.session['admin_logged_in'] = True
                login(request, user)
                return redirect('admin_dashboard')
        except User.DoesNotExist:
            pass
        messages.error(request, 'Invalid admin credentials.')
        return redirect('admin_login')
    return render(request, 'admin_login.html')


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_logged_in'):
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    auctions = Auction.objects.all().order_by('-created_at')
    users = User.objects.filter(is_staff=False).select_related('profile')
    bids = Bid.objects.all().select_related('auction', 'bidder').order_by('-created_at')
    contacts = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard.html', {
        'auctions': auctions,
        'users': users,
        'bids': bids,
        'contacts': contacts,
    })


@admin_required
def admin_delete_auction(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    auction.delete()
    return JsonResponse({'success': True})


@admin_required
def admin_delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return JsonResponse({'success': True})


@admin_required
def admin_delete_bid(request, pk):
    bid = get_object_or_404(Bid, pk=pk)
    bid.delete()
    return JsonResponse({'success': True})


@admin_required
def admin_toggle_featured(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    auction.featured = not auction.featured
    auction.save()
    return JsonResponse({'success': True, 'featured': auction.featured})


def admin_logout(request):
    request.session.pop('admin_logged_in', None)
    return redirect('admin_login')
