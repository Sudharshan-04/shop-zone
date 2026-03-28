from django.core.management.base import BaseCommand
from store.models import Category, Product


CATEGORIES = [
    {'name': 'Electronics', 'slug': 'electronics'},
    {'name': 'Fashion', 'slug': 'fashion'},
    {'name': 'Home & Kitchen', 'slug': 'home-kitchen'},
    {'name': 'Books', 'slug': 'books'},
    {'name': 'Sports & Fitness', 'slug': 'sports-fitness'},
    {'name': 'Toys & Games', 'slug': 'toys-games'},
    {'name': 'Beauty & Health', 'slug': 'beauty-health'},
    {'name': 'Grocery', 'slug': 'grocery'},
]

PRODUCTS = [
    # Electronics
    {'name': 'Samsung Galaxy S24 Ultra', 'slug': 'samsung-galaxy-s24-ultra', 'category': 'electronics',
     'description': 'Experience the ultimate smartphone with the Samsung Galaxy S24 Ultra. Featuring a stunning 6.8-inch Dynamic AMOLED 2X display, a powerful Snapdragon 8 Gen 3 processor, and a revolutionary 200MP quad-camera system. With 12GB RAM, up to 1TB storage, and S Pen included, this is the pinnacle of mobile innovation.',
     'price': 124999, 'original_price': 134999, 'stock': 25, 'rating': 4.7, 'rating_count': 8432, 'is_featured': True},
    {'name': 'Apple MacBook Air M3', 'slug': 'apple-macbook-air-m3', 'category': 'electronics',
     'description': 'The MacBook Air with M3 chip is incredibly thin and light, delivering exceptional performance and up to 18 hours of battery life. With a stunning Liquid Retina display, 8GB unified memory, and 256GB SSD, it handles everything effortlessly. The MagSafe charging, two Thunderbolt ports, and headphone jack make it the perfect portable powerhouse.',
     'price': 114900, 'original_price': 124900, 'stock': 15, 'rating': 4.8, 'rating_count': 5621, 'is_featured': True},
    {'name': 'Sony WH-1000XM5 Headphones', 'slug': 'sony-wh-1000xm5', 'category': 'electronics',
     'description': 'Industry-leading noise cancellation with two processors and eight microphones. 30-hour battery life with quick charging. Crystal clear hands-free calling with a precise voice pickup system. Ultra-comfortable design with lightweight materials for all-day wear.',
     'price': 26990, 'original_price': 34990, 'stock': 40, 'rating': 4.6, 'rating_count': 12089, 'is_featured': True},
    {'name': 'OnePlus Nord CE 3 Lite 5G', 'slug': 'oneplus-nord-ce-3-lite', 'category': 'electronics',
     'description': 'Powered by Snapdragon 695 5G, 8GB RAM, and 128GB storage. Features a 108MP AI camera, 5000mAh battery with 67W SUPERVOOC charging, and a 6.72-inch FHD+ LCD display with 120Hz refresh rate.',
     'price': 19999, 'original_price': 22999, 'stock': 60, 'rating': 4.2, 'rating_count': 6754},
    {'name': 'LG 55-Inch 4K Smart TV', 'slug': 'lg-55-4k-smart-tv', 'category': 'electronics',
     'description': '55-inch 4K UHD display with Dolby Vision IQ, Dolby Atmos, and AI ThinQ. webOS 23 smart platform with thousands of apps. Built-in Google Assistant and Amazon Alexa. HDMI 2.1 ports for gaming with VRR, ALLM support.',
     'price': 54999, 'original_price': 74999, 'stock': 12, 'rating': 4.4, 'rating_count': 3201, 'is_featured': True},

    # Fashion
    {'name': 'Levi\'s 511 Slim Fit Jeans', 'slug': 'levis-511-slim-jeans', 'category': 'fashion',
     'description': 'Classic Levi\'s 511 Slim Fit Jeans made from stretch denim for all-day comfort. Sits below the waist with a slim leg that runs close to the thigh, knee, and leg opening. Available in multiple washes.',
     'price': 2499, 'original_price': 3999, 'stock': 100, 'rating': 4.3, 'rating_count': 4521},
    {'name': 'Nike Air Force 1 Sneakers', 'slug': 'nike-air-force-1', 'category': 'fashion',
     'description': 'The radiant icon returns with the Nike Air Force 1. Encapsulated Nike Air cushioning provides excellent impact protection. Leather upper delivers durability and classic style. Perforated toe box allows breathability.',
     'price': 7495, 'original_price': 8495, 'stock': 50, 'rating': 4.5, 'rating_count': 7832, 'is_featured': True},
    {'name': 'Fastrack Casual Wristwatch', 'slug': 'fastrack-casual-watch', 'category': 'fashion',
     'description': 'Stylish Fastrack casual watch with mineral crystal glass, stainless steel case, and genuine leather strap. Water resistant up to 50m. Quartz movement for precision timekeeping. Day and date display.',
     'price': 1995, 'original_price': 2995, 'stock': 75, 'rating': 4.1, 'rating_count': 2341},

    # Home & Kitchen
    {'name': 'Instant Pot Duo 7-in-1', 'slug': 'instant-pot-duo-7-in-1', 'category': 'home-kitchen',
     'description': 'The world\'s best-selling multi-cooker. 7-in-1 functionality: Pressure Cooker, Slow Cooker, Rice Cooker, Steamer, Sauté, Yogurt Maker, and Warmer. 6-quart capacity, 13 customizable Smart Programs. Stainless steel inner pot.',
     'price': 8999, 'original_price': 11999, 'stock': 30, 'rating': 4.6, 'rating_count': 15421, 'is_featured': True},
    {'name': 'Dyson V12 Detect Slim Vacuum', 'slug': 'dyson-v12-detect-slim', 'category': 'home-kitchen',
     'description': 'Laser Detect technology reveals invisible dust. Acoustic piezo sensor counts and sizes dust particles, displaying data on LCD screen. Up to 60 minutes of fade-free power. 5-layer filtration captures 99.99% of particles.',
     'price': 43900, 'original_price': 49900, 'stock': 8, 'rating': 4.7, 'rating_count': 2109},
    {'name': 'Pigeon Automatic Rice Cooker', 'slug': 'pigeon-automatic-rice-cooker', 'category': 'home-kitchen',
     'description': 'Automatic rice cooker with 1.8L capacity. Non-stick inner bowl for easy cleaning. Keep warm function. Comes with measuring cup and serving spoon. Cooks rice perfectly every time.',
     'price': 1299, 'original_price': 1999, 'stock': 150, 'rating': 4.0, 'rating_count': 8976},

    # Books
    {'name': 'Atomic Habits by James Clear', 'slug': 'atomic-habits-james-clear', 'category': 'books',
     'description': 'No.1 New York Times bestseller. Tiny Changes, Remarkable Results. Learn how to build good habits, break bad ones, and get 1% better every day. Used by teams in the NFL, NBA, and MLB. Practical strategies that will teach you exactly how to form good habits, break bad ones, and master the tiny behaviors that lead to remarkable results.',
     'price': 399, 'original_price': 799, 'stock': 200, 'rating': 4.8, 'rating_count': 45231, 'is_featured': True},
    {'name': 'The Alchemist - Paulo Coelho', 'slug': 'the-alchemist-paulo-coelho', 'category': 'books',
     'description': 'A special 25th anniversary edition of the extraordinary international bestseller, including a new Foreword by Paulo Coelho. A fable about following your dream. Paulo Coelho\'s masterpiece tells the mystical story of Santiago, an Andalusian shepherd boy.',
     'price': 299, 'original_price': 499, 'stock': 180, 'rating': 4.6, 'rating_count': 38921},
    {'name': 'Rich Dad Poor Dad', 'slug': 'rich-dad-poor-dad', 'category': 'books',
     'description': 'Robert Kiyosaki\'s Rich Dad Poor Dad is the #1 Personal Finance book of all time. It has challenged and changed the way tens of millions of people around the world think about money. It advocates financial literacy and financial independence through investing in assets.',
     'price': 249, 'original_price': 495, 'stock': 220, 'rating': 4.5, 'rating_count': 52109},

    # Sports
    {'name': 'Nivia Storm Football', 'slug': 'nivia-storm-football', 'category': 'sports-fitness',
     'description': 'Nivia Storm football, Size 5, made from PVC material with hand-stitched panels. Latex rubber bladder for better air retention. Suitable for casual and recreational play on any surface.',
     'price': 599, 'original_price': 999, 'stock': 100, 'rating': 4.0, 'rating_count': 3421},
    {'name': 'Boldfit Adjustable Dumbbells Set', 'slug': 'boldfit-adjustable-dumbbells', 'category': 'sports-fitness',
     'description': 'Adjustable dumbbell set with weight plates from 2kg to 20kg. Chrome plated solid steel handles with non-slip grip. Rubber encased weight plates for noise-free workouts. Ideal for home gym use.',
     'price': 3499, 'original_price': 5999, 'stock': 45, 'rating': 4.3, 'rating_count': 2187, 'is_featured': True},

    # Beauty
    {'name': 'Lakme Absolute Skin Natural Mousse', 'slug': 'lakme-skin-natural-mousse', 'category': 'beauty-health',
     'description': 'Lakme Absolute Skin Natural Mousse Foundation with SPF 8 PA++. Lightweight, breathable mousse texture gives a natural, dewy finish. Buildable coverage from light to medium. Available in 6 shades.',
     'price': 549, 'original_price': 749, 'stock': 90, 'rating': 4.1, 'rating_count': 6543},
    {'name': 'Mamaearth Vitamin C Face Serum', 'slug': 'mamaearth-vitamin-c-serum', 'category': 'beauty-health',
     'description': 'Mamaearth Skin Illuminate Face Serum with Vitamin C and Turmeric for Radiant Skin. Reduces pigmentation, dark spots, and blemishes. Made with goodness of 82% natural ingredients. Paraben-free, silicone-free.',
     'price': 399, 'original_price': 599, 'stock': 120, 'rating': 4.2, 'rating_count': 11234, 'is_featured': True},

    # Toys
    {'name': 'LEGO Classic Medium Creative Brick Box', 'slug': 'lego-classic-medium-creative', 'category': 'toys-games',
     'description': 'The LEGO Classic Medium Creative Brick Box features 484 pieces in 35 different colors. Build and rebuild endless different models including a car, a windmill, and a crocodile. Includes building ideas booklet.',
     'price': 2999, 'original_price': 3999, 'stock': 35, 'rating': 4.7, 'rating_count': 4321},

    # Grocery
    {'name': 'Tata Tea Gold 1kg', 'slug': 'tata-tea-gold-1kg', 'category': 'grocery',
     'description': 'Tata Tea Gold is made from premium long leaf tea that is specially blended to give a strong and aromatic cup. A blend of finest long leaf teas from Assam, Darjeeling and Nilgiris.',
     'price': 399, 'original_price': 460, 'stock': 500, 'rating': 4.4, 'rating_count': 28341},
]


class Command(BaseCommand):
    help = 'Seed the database with sample categories and products'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database...')

        # Create categories
        cat_map = {}
        for cat_data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            cat_map[cat_data['slug']] = cat
            action = '✅ Created' if created else '⏭  Exists'
            self.stdout.write(f'{action}: Category "{cat.name}"')

        # Create products
        for p in PRODUCTS:
            cat = cat_map.get(p['category'])
            if not cat:
                self.stdout.write(f'⚠  Skipping {p["name"]}: category not found')
                continue

            product, created = Product.objects.get_or_create(
                slug=p['slug'],
                defaults={
                    'category': cat,
                    'name': p['name'],
                    'description': p['description'],
                    'price': p['price'],
                    'original_price': p.get('original_price'),
                    'stock': p.get('stock', 10),
                    'rating': p.get('rating', 4.0),
                    'rating_count': p.get('rating_count', 0),
                    'is_featured': p.get('is_featured', False),
                }
            )
            action = '✅ Created' if created else '⏭  Exists'
            self.stdout.write(f'{action}: Product "{product.name}"')

        self.stdout.write(self.style.SUCCESS('\n🎉 Database seeded successfully!'))
        self.stdout.write(f'   {Category.objects.count()} categories, {Product.objects.count()} products')
