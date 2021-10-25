"""
بسم الله الرحمن الرحيم
في هذا المثال سوف يتم توضيح طريقة تحديث المنتج
"""

from salla import Salla
from datetime import datetime, timedelta

store = Salla(token="TOKEN")

# جلب المنتج المراد اجرا التحديثات عليه
product = store.products().first()

# اجراء التحديثات على المنتج
product.name = "New name for product"
product.status = "hidden"
product.price.amount = 120
product.sale_price.amount = 100
product.sale_end = datetime.now() + timedelta(days=1)

# بعد اجراء التحديثات يتم حفظها عبر الميثود التالية
product.save()

# يمكنك تحديث حالة المنتج عبر الميثود التالية
product.change_status("sale")
