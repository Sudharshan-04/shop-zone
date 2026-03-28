# 🛒 ShopZone — Amazon-Style E-Commerce Platform

A full-featured, resume-ready e-commerce website built with **Django**, **MySQL**, and modern CSS — designed to closely mirror Amazon's UI/UX.

---

## 📸 Features

### UI & Design
- ✅ Amazon-style dark navbar with logo, search bar, cart icon, and user menu
- ✅ Category sub-navigation bar
- ✅ Product grid with cards (image, title, rating stars, price, discount badge, Add to Cart)
- ✅ Responsive design (mobile-first, works on all screen sizes)
- ✅ Hover effects, transitions, and micro-interactions
- ✅ Amazon color palette (dark navy, orange accent)

### Pages
| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Product listing with hero, featured, filters |
| Product Detail | `/product/<slug>/` | Full product info with buy box |
| Search Results | `/search/?q=` | Keyword search results |
| Cart | `/cart/` | Cart with quantity controls |
| Checkout | `/checkout/` | Address + payment form |
| Order Success | `/order/success/<id>/` | Confirmation page |
| Order History | `/orders/` | All past orders |
| Order Detail | `/orders/<id>/` | Single order details |
| Login | `/login/` | Sign in page |
| Sign Up | `/signup/` | Create account |
| Profile | `/profile/` | User profile + recent orders |
| Admin | `/admin/` | Django admin panel |

### Core Features
- **Phase 1** — Product grid, detail page, add to cart (session + DB), cart with totals
- **Phase 2** — User registration, login, logout, session merge on login
- **Phase 3** — Order history, admin panel, search, category + price filters
- **Payment** — Cash on Delivery, UPI, Card (dummy — no real payment processing)

---

## 🗂 Project Structure

```
shopzone/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3                  ← auto-created on migration
├── media/
│   └── products/               ← uploaded product images
├── shopzone/                   ← Django project config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── store/                      ← Main application
    ├── __init__.py
    ├── models.py               ← Product, Category, Cart, Order, OrderItem
    ├── views.py                ← All view functions
    ├── urls.py                 ← URL routing
    ├── admin.py                ← Admin panel config
    ├── context_processors.py  ← Cart count in navbar
    ├── management/
    │   └── commands/
    │       └── seed_data.py    ← Load sample products
    ├── templatetags/
    │   └── store_tags.py       ← Custom template filters (stars, currency)
    ├── static/store/
    │   ├── css/main.css        ← All styles (~900 lines)
    │   └── js/main.js          ← Cart controls, UI interactions
    └── templates/store/
        ├── base.html           ← Navbar + footer layout
        ├── home.html           ← Homepage
        ├── product_card.html   ← Reusable product card
        ├── product_detail.html ← Product page
        ├── cart.html           ← Shopping cart
        ├── checkout.html       ← Checkout form
        ├── order_success.html  ← Success page
        ├── order_history.html  ← Past orders
        ├── order_detail.html   ← Order details
        ├── login.html          ← Sign in
        ├── signup.html         ← Register
        ├── profile.html        ← User account
        └── search_results.html ← Search page
```

---

## ⚡ Quick Setup (SQLite — Easiest)

### 1. Clone / Extract the project
```bash
cd shopzone
```

### 2. Create virtual environment
```bash
python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install Django Pillow
# (For MySQL, also run: pip install mysqlclient)
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create superuser (Admin)
```bash
python manage.py createsuperuser
# Enter: username, email, password
```

### 6. Seed sample data (20 products across 8 categories)
```bash
python manage.py seed_data
```

### 7. Run the development server
```bash
python manage.py runserver
```

### 8. Open your browser
- 🛒 **Store:** http://127.0.0.1:8000/
- 🔧 **Admin:** http://127.0.0.1:8000/admin/

---

## 🐬 MySQL Setup (Production-Ready)

### Step 1: Create MySQL database
```sql
CREATE DATABASE shopzone_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'shopzone_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON shopzone_db.* TO 'shopzone_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 2: Install MySQL client
```bash
pip install mysqlclient
```

### Step 3: Update `shopzone/settings.py`
Comment out the SQLite block and uncomment the MySQL block:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shopzone_db',
        'USER': 'shopzone_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 4: Migrate and seed
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
python manage.py runserver
```

---

## 🗃 Database Models

### Category
| Field | Type | Description |
|-------|------|-------------|
| name | CharField | Category name |
| slug | SlugField | URL-friendly identifier |
| image | ImageField | Optional category image |

### Product
| Field | Type | Description |
|-------|------|-------------|
| category | ForeignKey | Linked category |
| name | CharField | Product name |
| slug | SlugField | URL identifier |
| description | TextField | Full description |
| price | DecimalField | Selling price |
| original_price | DecimalField | MRP (for discount calc) |
| image | ImageField | Product photo |
| stock | IntegerField | Quantity available |
| rating | DecimalField | Star rating (0.0–5.0) |
| rating_count | IntegerField | Number of reviews |
| is_featured | BooleanField | Show in featured section |

### Cart + CartItem
Supports both logged-in users (user FK) and guests (session key).

### Order + OrderItem
Full order with shipping address, payment method, and status tracking.

---

## 🔧 Admin Panel

Go to `/admin/` and log in with your superuser credentials.

You can:
- **Add/Edit/Delete** products and categories
- **Upload product images**
- **View and manage orders**
- **Change order status** (Pending → Processing → Shipped → Delivered)

### Adding products via Admin
1. Go to `/admin/store/category/` → Add your categories
2. Go to `/admin/store/product/add/` → Fill in all fields
3. Upload a product image (optional but recommended)
4. Check "Is featured" to show in the featured section

---

## 🔍 Search & Filtering

- **Navbar search** → searches product name, description, and category
- **Category sidebar** → filter by category
- **Price range** → min/max price filter
- **Sort by** → Featured, Price (low→high), Price (high→low), Rating, Newest

---

## 🚀 Deployment Tips

### Collect static files
```bash
python manage.py collectstatic
```

### Environment variables (production)
```bash
export SECRET_KEY="your-production-secret-key"
export DEBUG=False
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
```

### Recommended: use `python-decouple` or `.env` files for secrets.

---

## 🎨 Customization

### Change colors
Edit `store/static/store/css/main.css` → update the `:root` variables:
```css
:root {
  --amazon-orange: #ff9900;   /* Primary accent */
  --amazon-dark: #131921;     /* Navbar background */
  --price-color: #B12704;     /* Price text */
}
```

### Add product images
Upload via Django Admin. Images are stored in `media/products/`.
Recommended size: **500×500 pixels**, PNG or JPG.

### Change site name
Search for "ShopZone" in templates and CSS to rebrand.

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, Django 4.2 |
| Database | SQLite (dev) / MySQL (prod) |
| Frontend | HTML5, CSS3, Vanilla JS |
| Styling | Custom CSS (Flexbox + Grid) |
| Auth | Django built-in auth system |
| Images | Pillow + Django ImageField |
| Admin | Django Admin (customized) |

---

## 📝 License

This project is for educational and portfolio use. Feel free to customize and deploy!
