"""
بسم الله الرحمن الرحيم
في هذا المثال سوف يتم توضيح طريقة عمل فور لوب على المنتجات
"""

from salla import Salla

store = Salla(token="TOKEN")

# عمل فور لوب على المنتاجات
for product in store.products():
    print(product.name)
