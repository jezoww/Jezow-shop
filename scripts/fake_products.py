import os
import random
from faker import Faker
from apps.product.models import Product, ProductImage, AboutProduct, Category

fake = Faker()

def create_fake_categories(num_categories=10):
    for i in range(num_categories):
        name_uz = fake.word().capitalize() + " uz"
        name_ru = fake.word().capitalize() + " ru"
        name_en = fake.word().capitalize() + " en"

        Category.objects.create(
            name=name_en,
            name_uz=name_uz,
            name_ru=name_ru,
            name_en=name_en,
        )
        print(i)

def create_fake_products(num_products=10):
    categories = list(Category.objects.all())
    if not categories:
        print("Kategoriya mavjud emas. Iltimos, kamida bitta kategoriya yarating!")
        return

    image_folder = 'media/product'
    if not os.path.exists(image_folder):
        print(f"{image_folder} papkasi topilmadi! Iltimos, ushbu papkani yarating va rasmlarni joylashtiring.")
        return

    # Rasmlar ro'yxatini olish
    available_images = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    if not available_images:
        print(f"{image_folder} papkasida hech qanday rasm topilmadi.")
        return

    for i in range(num_products):
        name_uz = fake.word().capitalize() + " uz"
        name_ru = fake.word().capitalize() + " ru"
        name_en = fake.word().capitalize() + " en"
        description_uz = fake.text(max_nb_chars=200) + " (uz)"
        description_ru = fake.text(max_nb_chars=200) + " (ru)"
        description_en = fake.text(max_nb_chars=200) + " (en)"

        # Product yaratish
        product = Product.objects.create(
            name=name_uz,  # Asosiy `name` - name_uz bo'lsin
            name_uz=name_uz,
            name_ru=name_ru,
            name_en=name_en,
            price=random.randint(10000, 100000),
            description=description_uz,  # Asosiy `description` - description_uz bo'lsin
            description_uz=description_uz,
            description_ru=description_ru,
            description_en=description_en,
            category=random.choice(categories),
            gender=random.choice(['male', 'female', 'unisex'])  # ProductGenderChoice uchun
        )
        # print(f"Yaratildi: {product.name}")

        # Har bir mahsulot uchun rasm yaratish
        for _ in range(random.randint(1, 5)):  # Har bir mahsulotga 1-5 ta rasm
            image_name = random.choice(available_images)  # Tasodifiy rasm tanlash
            ProductImage.objects.create(
                product=product,
                image=f"product/{image_name}"  # Fayl yo'li: 'product/<file_name>'
            )
            # print(f"   Rasm yaratildi: {image_name}")

        # Har bir mahsulot uchun qo'shimcha ma'lumotlar (AboutProduct)
        sizes = []
        for _ in range(random.randint(1, 3)):  # Har bir mahsulotga 1-3 ta o'lcham
            size = random.choice(['S', 'M', 'L', 'XL', 'XXL'])
            while size in sizes:
                size = random.choice(['S', 'M', 'L', 'XL', 'XXL'])
            sizes.append(size)
            AboutProduct.objects.create(
                product=product,
                size=size,
                quantity=random.randint(1, 50)
            )
            # print(f"   Qo'shimcha ma'lumot yaratildi: {product.name}")
        print(i)