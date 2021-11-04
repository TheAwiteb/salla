

<div align="center">
<img src="https://i.suar.me/mKLad/l" width=400>
</div>

# <p align="center">Salla 🛍️ 

<p align="center">
  <a href="https://pypi.org/project/salla/">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/salla?color=9cf">
  </a>
  <a href="https://pypi.org/project/salla/">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/salla?color=9cf">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/pypi/l/salla?color=9cf&label=License" alt="License">
  </a>
  <a href="https://github.com/psf/black">
    <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
  </a>
</p>

## <p dir="rtl" align="center"> تحت التطوير 👨‍💻


### <p dir="rtl" align="center"> مكتبة بايثون بسيطة، ولاكن قابلة للتوسع، خاصة بـ <a href="https://docs.salla.dev/">واجهة برمجة تطبيقات سلة</a> 👏.


## <p dir="rtl" align="center">المكتبة تحت التطوير الى الان ولم يتم دعم اي اصدار من  <a href="https://docs.salla.dev/">سلة</a> بشكل كامل ⏳

<div dir="rtl">

## المحتوى

<!-- 
* []()
-->

  * [البداية](#البداية)
  * [كتابة كودك الاول](#كتابة-كودك-الاول)
    * [المتطلبات](#المتطلبات)
    * [كود بسيط لعرض المنتجات](#كود-بسيط-لعرض-المنتجات)
  * [الوثائق العامة](#الوثائق-العامة)
    * [الانواع - Types](#الانواع---types)
    * [الاستخدام العام للمكتبة](#الاستخدام-العام-للمكتبة)
      * [متغيرات البيئة](#متغيرات-البيئة)
      * [مصفوفة المنتجات - productlist](#مصفوفة-المنتجات---productlist)
        * [التعامل مع الصفحات - pagination](#التعامل-مع-الصفحات---pagination)
      * [جلب المنتجات](#جلب-المنتجات)
      * [بيانات المتجر](#بيانات-المتجر)
      * [المنتج - product](#المنتج---product)
        * [انشاء منتج - create_product](#انشاء-منتج---create-product)
        * [تحديث المنتج](#تحديث-المنتج)
        * [مسح المنتج](#مسح-المنتج)
        * [مسح صورة المنتج](#مسح-صورة-المنتج)

  * [المزيد من الامثلة](#المزيد-من-الامثلة)
  * [لديك فكرة؟ او تريد اجابة لسؤالك](#لديك-فكرة-او-تريد-اجابة-لسؤالك)
  * [مجموعة التيليجرام](#مجموعة-التيليجرام)
  * [عند مواجهة مشكلة](#عند-مواجهة-مشكلة)
  * [مشاريع استخدمت المكتبة](#مشاريع-استخدمت-المكتبة)

## البداية

تحتاج اصدار [بايثون](https://python.org) اكبر من او يساوي 3.8


هناك طريقتين لتنزيل المكتبة

* تنزيلها باستخدام pip ([مدير حزم بايثون](https://pip.pypa.io/en/stable/cli/pip_install/))*:
</div>

```bash
pip3 install salla
```

<div dir="rtl">


* التنزيل من السورس كود ([git](https://git-scm.com/downloads))*:

</div>


```bash
git clone https://github.com/TheAwiteb/salla
cd salla
python3 setup.py install
```
<div dir="rtl">
<b>يوصى باستخدام الخيار الأول.</b>
<br><br>

> <b>المكتبة لاتزال تحت التطوير ولديها تحديثات منتظمة ، لا تنسى تحديثها بانتظام عن طريق  <b>

</div>


```bash
pip3 install salla --upgrade
```
<div dir="rtl">

### [الرجوع للاعلى ⬆️](#المحتوى)

## كتابة كودك الاول

### المتطلبات

من المفترض أنك [حصلت على رمز واجهة برمجة التطبيقات](https://docs.salla.dev/docs/merchent/ZG9jOjIzMjE3MjMy-authorization). سوف نسمي هذا الرمز المميز "TOKEN".
علاوة على ذلك ، لديك معرفة أساسية بلغة برمجة Python والأهم من ذلك [واجهة برمجة تطبيقات سلة](https://docs.salla.dev/).


### كود بسيط لعرض المنتجات

انشاء ملف جديد اسمه `salla_products_list.py`
وبعد ذالك افتح الملف واستدع فيه مكتبة سلة 

</div>

```python
from salla import Salla

store = Salla(token="TOKEN")

# عمل فور لوب على المنتاجات
for product in store.products():
    print(product.name)

```
<div dir="rtl">

بسيط جدا  🎉

*تنويه: تاكد من انك قمت باستبدال  الـ TOKEN مع الرمز الخاص بك.*

*تنويه: `salla.Salla.products` ترجع لك نوع `ProductList` وليس مصفوفة اذ كنت تريد تحويلها الى المصفوفة انظر الى المثال 👇 .*

</div>

```python
import salla

store = salla.SallaStore(token="TOKEN")

# وضع المنتجات في مصفوفة
products = list(store.products())
```
<div dir="rtl">

**يمكنك تصفية الكلمات الرئيسية والحالة والفئة انظر الى [salla.Salla.products](#جلب-المنتجات)**


## الوثائق العامة

### [الرجوع للاعلى ⬆️](#المحتوى)

### الانواع - types

جميع الانواع متعرفة في [salla_types.py](salla/types.py) ومشروحة هناك القي نظرة

ويمكنك العثور على نوع المنتجات هنا [product.py](salla/product.py)

### الاستخدام العام للمكتبة

تم توضيح بعض حالات الاستخدام العامة لواجهة برمجة التطبيقات أدناه.

#### متغيرات البيئة
متغيرات البيئة هي متغيرات يتم تعريفها في البيئة واستدعئها في الكود <br> تساعدك في الاتمتة بحيث انك ماتدخل المتغير في 
الكود كل شوي فقط تعرفه في البيئة وتفيدك كمان <br> في الخصوصية بحيث اذا كان متغير خاص مثل التوكن مايظهر في الكود

في الاسفل توضيح طريقة استخدام متغيرات البيئة
##### التوكن
طريقة تعريف التوكن في البيئة بسيطة جدا يتم وضع هذا الامر في الترمنال <br>
</div>

`export SALLA_TOKEN=ضع التوكن هنا`

```python
from salla import Salla

# لكي يتم جلبه من البيئة TOKEN يجب جعل قيمة التوكن 
store = Salla(token="TOKEN")

```

<div dir="rtl">

يجب ان تجعل قيمة التوكن `TOKEN` لكي يتم جلب قيمته من البيئة

يتم الاشارة الى التوكن بهذا الاسم `SALLA_TOKEN` في البيئة

> تنويه: لاتقم بتغير الاسم الذي يشير الى التوكن اجعله فقط SALLA_TOKEN

#### مصفوفة المنتجات - productlist
<p>
ProductList
هو الكلاس الذي يحتوي المنتجات لديه مميزات كثيرة سوف يتم التطرق لها في الاسفل
<p>

##### التعامل مع الصفحات - pagination
pagination
وهي من اهم المميزات في الكلاس حيث تسمح لك بالتحكم بصفحات المنتجات بعض الامثلة في الاسفل

</div>

```python
from salla import Salla

store = Salla(token="TOKEN")

# تقسيم المنتجات في صفحات كل صفحة تحتوي 5 منتجات
products = store.products(per_page=5)

# طباعة رقم الصفحة الحالية
print(products.pagination.current_page)

# 👇 توجد طريقتين للتنقل بين الصفحات تم سردها ادناه

# الطريقة الاولى: عبر الميثودين التالية
# next: تعني الذهاب الى الصفحة التالية (ترجع خطأ اذ لم توجد صفحة تالية)
# previous: تعني الذهاب الى الصفحة السابقة (ترجع خطأ اذ لم توجد صفحة سابقة)
# 👇 طريقة استخدامهم

# الذهاب الى الصفحة التالية
products.next()
# طباعة رقم الصفحة الحالية
print(products.pagination.current_page)

# الذهاب الى الصفحة السابقة
products.previous()
# طباعة رقم الصفحة الحالية
print(products.pagination.current_page)

# الطريقة الثانية: عبر الميثود التالية
# page: تستقبل ارجيمنت (معطى) واحد وهو رقم الصفحة المراد الذهاب اليها
# 👇 طريقة استخدامها

products.page(2)
# طباعة رقم الصفحة الحالية
print(products.pagination.current_page)
```
<div dir="rtl">

وبالمثال ادناه بعض الميثودات التي سوف تساعدك عند التعامل مع كلاس 
ProductList

### [الرجوع للاعلى ⬆️](#المحتوى)

</div>

```python
from salla import Salla

store = Salla(token="TOKEN")
products = store.products(per_page=5)

# جلب اول عنصر في المصفوفة
first_product = products.first()
# او
first_product = products[0]

# جلب اخر عنصر في المصفوفة
first_product = products.last()
# او
first_product = products[-1]

# معرفة اذ كان يوجد صفحة تالية
products.have_next()

# معرفة اذ كان يوجد صفحة سابقة
products.have_previous()

```
<div dir="rtl">

#### جلب المنتجات

فيما يلي بعض الأمثلة على استخدام عوامل التصفية ومعالجات جلب المنتجات

### [الرجوع للاعلى ⬆️](#المحتوى)

</div>

```python

from salla import Salla

store = Salla(token="TOKEN")


# جلب المنتجات بدون تصفية
products = store.products()

# SKU تصفية المنتجات مع اسم محدد أو.
products = store.products(keyword="هنا SKU يتم وضع الاسم او ال")

# التصفية بحسب رقم الصفحة
products = store.products(page=1)


# وضع حد للمنتجات لكل صفحة
products = store.products(per_page=3)


# (hidden,sale,out) تصفية بحسب حالة المنتج
products = store.products(status="out")

```

<div dir="rtl">

#### بيانات المتجر
يمكنك الوصول الى بيانات المتجر مثل اسمه او الرابط الخاص به او الصورة الخاصة به انظر الى المثال ادناه

</div>

```python
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

```

<div dir="rtl">

للمزيد يمكنك الاطلاع على [هذاالمثال](examples/store_detalis.py)

#### المنتج - product
المنتج هو اهم كلاس في المكتبة حيث يرتكز عليه كل شي ادناه طريقة التعامل معه

##### انشاء منتج - create product
...

##### تحديث المنتج
في المثال ادناه سوف يتم توضيح طريقة تحديث المنتج

</div>


```python
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

```
<div dir="rtl">

##### مسح المنتج
في المثال ادناه سوف يتم توضيح طريقة مسح المنتج

### [الرجوع للاعلى ⬆️](#المحتوى)

</div>


```python
from salla import Salla

store = Salla(token="TOKEN")

# جلب المنتج المراد مسحه
product = store.products().first()

product.delete()

```

<div dir="rtl">

##### مسح صورة المنتج
في المثال ادناه سوف يتم توضيح طريقة مسح صورة المنتج

### [الرجوع للاعلى ⬆️](#المحتوى)

</div>


```python
from salla import Salla

store = Salla(token="TOKEN")

# جلب المنتج المراد مسح صورته
product = store.products().first()

# جلب الصورة المراد مسحها
image = product.images[0]

image.delete()

```

<div dir="rtl">

وبالمثال ادناه بعض الميثودات التي سوف تساعدك عند التعامل مع المنتج
</div>

```python
from salla import Salla

store = Salla(token="TOKEN")

# جلب المنتج المراد اجرا الميثودات عليه
product = store.products().first()

# جلب اسماء العناصر التي تم تحديثها
product.get_changed_values()

```
<div dir="rtl">

### [الرجوع للاعلى ⬆️](#المحتوى)

## المزيد من الامثلة

يمكنك العثور على المزيد من الامثلة في [مجلد الامثلة](examples)


## مجموعة التيليجرام

احصل على مساعدة. مناقشة. دردشة.

* انضم الى [مجموعة دردشة  تيليجرام الخاصة بواجهة برمجة تطبيقات سلة](https://t.me/salladev)

## لديك فكرة او تريد اجابة لسؤالك
يمكنك المناقشة في الغرفة المخصصة للنقاش من [](https)[هنا](https://github.com/TheAwiteb/salla/discussions)

## عند مواجهة مشكلة

لاتتردد في رفع [issues](https://github.com/TheAwiteb/salla/issues) عند مواجهة اي مشكلة

## الرخصة
هذا المشروع تحت رخصة ([MIT](https://opensource.org/licenses/MIT))


## مشاريع استخدمت المكتبة
* لايوجد بعد


**تريد ان تكون في القائمة؟ فقط قم بعمل طلب سحب (PR) ، سوف يتم قبول المشاريع مفتوحة المصدر فقط.**

يجب ان يكون التنسيق هكذا 👇

* [اسم المشروع هنا](https://examples.com) 
من قبل [ضع اسمك هنا](https://examples.com) 
(وصف المشروع هنا)