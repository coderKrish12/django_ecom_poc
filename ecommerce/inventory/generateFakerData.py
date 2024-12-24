import json
from faker import Faker
import random
from datetime import datetime

faker = Faker()

data = []

# Generate Categories
category_ids = []
for i in range(1, 11):  # 5 categories
    category_ids.append(i)
    timestamp = faker.date_time_this_decade()
    data.append({
        "model": "app_name.category",
        "pk": i,
        "fields": {
            "name": faker.word().capitalize(),
            "description": faker.text(),
            "slug": faker.slug(),
            "created_at": timestamp.isoformat(),
            "updated_at": timestamp.isoformat(),
            "is_active": True
        }
    })

# Generate Products
product_ids = []
product_pk = 1
for i in range(1, 101):  # 20 products
    category_id = random.choice(category_ids)
    timestamp = faker.date_time_this_decade()
    product_ids.append(product_pk)
    data.append({
        "model": "app_name.product",
        "pk": product_pk,
        "fields": {
            "name": faker.word().capitalize(),
            "description": faker.text(),
            "slug": faker.slug(),
            "category": category_id,
            "created_at": timestamp.isoformat(),
            "updated_at": timestamp.isoformat(),
            "is_active": True
        }
    })
    product_pk += 1

# Generate Product Images
image_pk = 1
image_map = {}  # To map products to their images
for product_id in product_ids:
    image_map[product_id] = []
    for _ in range(random.randint(1, 3)):  # Each product has 1-3 images
        timestamp = faker.date_time_this_decade()
        image_map[product_id].append(image_pk)
        data.append({
            "model": "app_name.productimage",
            "pk": image_pk,
            "fields": {
                "product": product_id,
                "url": faker.image_url(),
                "alt_text": faker.sentence(),
                "created_at": timestamp.isoformat(),
                "updated_at": timestamp.isoformat()
            }
        })
        image_pk += 1

# Generate Attributes and Attribute Values
attribute_ids = []
attribute_value_pk = 1
for i in range(1, 6):  # 5 attributes
    attribute_ids.append(i)
    timestamp = faker.date_time_this_decade()
    data.append({
        "model": "app_name.attribute",
        "pk": i,
        "fields": {
            "name": faker.word().capitalize(),
            "description": faker.text(),
            "created_at": timestamp.isoformat(),
            "updated_at": timestamp.isoformat()
        }
    })

    for _ in range(3):  # Each attribute has 3 values
        timestamp = faker.date_time_this_decade()
        data.append({
            "model": "app_name.attributevalue",
            "pk": attribute_value_pk,
            "fields": {
                "attribute": i,
                "value": faker.word().capitalize(),
                "created_at": timestamp.isoformat(),
                "updated_at": timestamp.isoformat()
            }
        })
        attribute_value_pk += 1

# Generate Inventory and Stock
inventory_pk = 1
stock_pk = 1
attribute_value_ids = list(range(1, attribute_value_pk))  # All attribute values

for product_id in product_ids:
    for _ in range(random.randint(1, 3)):  # Each product has 1-3 inventory items
        inventory_attributes = random.sample(attribute_value_ids, random.randint(1, 3))
        inventory_images = image_map[product_id]
        timestamp = faker.date_time_this_decade()

        data.append({
            "model": "app_name.inventory",
            "pk": inventory_pk,
            "fields": {
                "product": product_id,
                "sku": faker.unique.lexify(text="SKU-????"),
                "price": round(random.uniform(10, 500), 2),
                "created_at": timestamp.isoformat(),
                "updated_at": timestamp.isoformat(),
                "is_active": True,
                "attributes": inventory_attributes,
                "images": inventory_images
            }
        })

        # Generate Stock for the Inventory
        timestamp = faker.date_time_this_decade()
        data.append({
            "model": "app_name.stock",
            "pk": stock_pk,
            "fields": {
                "inventory": inventory_pk,
                "quantity": random.randint(10, 100),
                "created_at": timestamp.isoformat(),
                "updated_at": timestamp.isoformat(),
                "is_active": True
            }
        })

        inventory_pk += 1
        stock_pk += 1

# Save the JSON
with open("products_fixture.json", "w") as file:
    json.dump(data, file, indent=4)
