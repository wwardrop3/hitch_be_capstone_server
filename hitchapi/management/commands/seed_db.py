# import random
# from datetime import datetime
# from sqlite3 import Date
# import faker_commerce
# from faker import Faker
# from django.contrib.auth.models import User
# from django.core.management.base import BaseCommand
# from rest_framework.authtoken.models import Token
# from hitchapi.models import (
#     TripTag, Tag, Trip, PassengerTrip, Member)


# class Command(BaseCommand):
#     faker = Faker()
#     faker.add_provider(faker_commerce.Provider)
#     faker.add_provider(faker_date_time.Provider)

#     def add_arguments(self, parser):
#         # Positional arguments
#         parser.add_argument(
#             '--user_count',
#             help='Count of users to seed',
#         )

#     def handle(self, *args, **options):
#         if options['user_count']:
#             user_count = int(options['user_count'])
#             if user_count < 3:
#                 raise ValueError("user_count must be greater than 3")
#             self.create_users(int(options['user_count']))
#         else:
#             self.create_users()

#     def create_users(self, user_count=8):
#         """Create random users"""
#         for _ in range(user_count):
#             first_name = self.faker.first_name()
#             last_name = self.faker.last_name()
#             username = f'{first_name}_{last_name}@example.com'
#             user = User.objects.create_user(
#                 first_name=first_name,
#                 last_name=last_name,
#                 password="password",
#                 username=username,
#             )
            
            


#             Token.objects.create(
#                 user=user
#             )

          
#             users = User.objects.all()

#         for user in users:
#             self.create_member(user)


#     def create_member(self, user):
#         """Create random stores in the database"""
#         return Member.objects.create(
#             user=user,
#             bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas pellentesque.",
#             is_active=True,
#             created_on = self.faker.
#         )

#     def create_products(self, store, count):
#         """Create Random Products in the database"""
#         for _ in range(count):
#             Product.objects.create(
#                 name=self.faker.ecommerce_name(),
#                 store=store,
#                 price=random.randint(50, 1000),
#                 description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam elit.",
#                 quantity=random.randint(2, 20),
#                 location=random.choice(STATE_NAMES),
#                 image_path="",
#                 category=Category.objects.get_or_create(
#                     name=self.faker.ecommerce_category())[0]
#             )

#     def create_closed_orders(self, user):
#         """Create closed orders for the user"""
#         order = Order.objects.create(
#             user=user,
#             payment_type=user.payment_types.first(),
#             completed_on=datetime.now()
#         )
#         category = random.randint(1, Category.objects.count())
#         products = [product.id for product in Product.objects.filter(
#             category_id=category)]
#         order.products.set(products)

#     def create_open_orders(self, user):
#         """Create open orders for the user"""
#         order = Order.objects.create(
#             user=user
#         )
#         category = random.randint(1, Category.objects.count())
#         products = [product.id for product in Product.objects.filter(
#             category_id=category)]
#         order.products.set(products)

#     def create_favorite(self, user):
#         """Create Favorites for the user"""
#         store = Store.objects.get(pk=random.randint(1, Store.objects.count()))

#         Favorite.objects.create(
#             customer=user,
#             store=store
#         )

#     def create_ratings(self, user):
#         """Add ratings to products"""
#         for product in Product.objects.all():
#             Rating.objects.create(
#                 customer=user,
#                 product=product,
#                 score=random.randint(1, 5),
#                 review=self.faker.paragraph()
#             )
