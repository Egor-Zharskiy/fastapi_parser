from pymongo import MongoClient
from datetime import datetime

client = MongoClient("localhost", 27017)

db = client.parser_db

for cat in [{'name': 'Школа',
             'url': '/c/4154/default-kids/?keep_filters=property_school&l=1&property_school=37833%2C37831%2C37832%2C37829%2C37830%2C37828%2C36045&sitelink=topmenuK'},
            {'name': 'Новинки', 'url': '/c/4154/default-kids/?genders=boys%2Cgirls&is_new=1&l=2&sitelink=topmenuK'},
            {'name': 'Девочкам', 'url': '/c/5379/default-devochkam/?genders=girls&l=3&sitelink=topmenuK'},
            {'name': 'Мальчикам', 'url': '/c/5378/default-malchikam/?genders=boys&l=4&sitelink=topmenuK'},
            {'name': 'Малышам', 'url': '/c/5414/default-novorozhdennym/?l=5&sitelink=topmenuK'},
            {'name': 'Бренды', 'url': '/brands/?b=kids&l=6&sitelink=topmenuK'},
            {'name': 'Premium', 'url': '/c/4154/default-kids/?l=7&labels=32246&sf=381&sitelink=topmenuK'},
            {'name': 'Спорт', 'url': '/c/4154/default-kids/?l=8&labels=5649&sf=221&sitelink=topmenuK'},
            {'name': 'Уход', 'url': '/c/6815/default-uhod_za_rebenkom/?l=9&sitelink=topmenuK'},
            {'name': 'Sale%',
             'url': '/c/4154/default-kids/?display_locations=outlet&is_sale=1&l=10&sitelink=topmenuK'}]:
    cat['created_at'] = datetime.now()
    cat['sex'] = 'kids'
    db.categories.insert_one(cat)

