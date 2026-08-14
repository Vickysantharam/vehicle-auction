# 🚗 Vehicle Auction System - Django

A full-featured vehicle auction web application built with Django, HTML, CSS, JavaScript, and SQLite.

## 🚀 Quick Start

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Seed Sample Data (already done)
```bash
python manage.py shell < seed.py
```

### 4. Start Development Server
```bash
python manage.py runserver
```

Then open: **http://127.0.0.1:8000**

---

## 🔐 Default Credentials

### Admin Panel → http://127.0.0.1:8000/admin-panel/login/
- **Email:** admin@gmail.com
- **Password:** 123

### Django Admin → http://127.0.0.1:8000/django-admin/
- **Username:** admin
- **Password:** 123

---

## 📋 Features

| Feature | Description |
|--------|-------------|
| 🏠 Home Page | Featured auctions carousel, How It Works, Testimonials |
| 🔍 Search | Search auctions by vehicle name |
| 👤 Auth | Register/Login with flip card animation |
| 💰 Bidding | Real-time bid placement via AJAX |
| 📋 Post Auction | Upload vehicle with image |
| 👤 Profile | Update name, email, phone, profile picture |
| 📊 Dashboard | User stats, my auctions, my bids |
| 🔐 Admin Panel | Manage auctions, users, bids, messages |
| 📧 Contact | Contact form with message storage |
| ℹ️ About | Team and mission page |

## 📁 Project Structure
```
vehicle_auction_django/
├── manage.py
├── requirements.txt
├── vehicle_auction.db          ← SQLite database
├── vehicle_auction_django/
│   ├── settings.py
│   └── urls.py
├── auction/
│   ├── models.py               ← DB models
│   ├── views.py                ← All views
│   ├── urls.py                 ← URL routing
│   └── admin.py
├── templates/                  ← HTML templates
├── static/
│   ├── css/styles.css
│   └── js/main.js
└── media/
    └── static_images/          ← Vehicle images
```
