"""
بسم الله الرحمن الرحيم
في هذا المثال سوف يتم توضيح طريقة الوصول الى بيانات المتجر
"""

from salla import Salla

store = Salla(token="TOKEN")

## طباعة رابط المتجر
print(store.details.url)

## طباعة اسم المتجر
print(store.details.name)

## طباعة اسم صاحب المتجر
print(store.details.owner.name)

## طباعة ايميل صاحب المتجر
print(store.details.owner.email)

# والمزيد
"""
store.details.avatar
store.details.created_at
store.details.id
store.details.name
store.details.owner
store.details.plan
store.details.status
store.details.store_location
store.details.url
store.details.username
"""
"""
store.details.owner.created_at
store.details.owner.email
store.details.owner.id
store.details.owner.mobile
store.details.owner.name
store.details.owner.role
"""
