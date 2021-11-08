from salla import Salla
from salla.product import Product
from salla.types import Option, Value, Price, Image, ImageList
from datetime import datetime, timedelta

store = Salla(token="TOKEN")
products = store.products(per_page=1)


def must_be_error(func, *args, **kwargs) -> bool:
    """اذ لم يحصل False اذ حدث خطأ وارجاع True ارجاع

    المتغيرات:
        func (function): الدالة او الكلاس المراد اختباره

    Returns:
        bool: قيمة صحيحة اذ حدث خطأ وقيمة خاطئة اذ لم يحدث
    """
    try:
        func(*args, **kwargs)
    except:
        return True
    else:
        return False


def test_product_list():
    current_page = products.pagination.current_page

    if products.have_next():
        products.next()
        assert products.pagination.current_page == current_page + 1
    else:
        print("Dont have next page!")

    if products.have_previous():
        products.previous()
        assert products.pagination.current_page == current_page
    else:
        print("Dont have previous page!")

    assert products.first() == products.products[0]
    assert products.last() == products.products[-1]


def test_create_product():
    # سيتم كتابتها بعد انشاء المنتج
    pass


def test_update_product():
    product: Product = products.first()

    product.name = "new product name"
    product.price.amount = 12
    product.status = "hidden"
    product.quantity = 10
    product.unlimited_quantity = True
    product.description = "new product description"
    # product.categories =
    # product.min_amount_donating = 99
    # product.max_amount_donating = 1000
    product.sale_price.amount = 5
    product.cost_price = 8
    product.sale_end = datetime.now() + timedelta(days=1, hours=1)
    product.require_shipping = True
    # product.maximum_quantity_per_order =
    product.weight = 10
    product.sku = "new product sku"
    product.with_tax = True
    # product.hide_quantity =
    product.enable_upload_image = True
    # product.enable_note =
    # product.pinned =
    product.active_advance = True
    # product.subtitle =
    # product.promotion_title =
    # product.metadata_title =
    # product.metadata_description =
    # product.brand_id =
    # product.tags =

    product.save()

    assert must_be_error(product.save)

    new_product: Product = store.products(per_page=1).first()

    assert new_product.name == "new product name"
    assert new_product.price.amount == 5  # تم تحديث سعر الخصم في الاعلى
    assert new_product.status == "hidden"
    assert new_product.quantity == 10
    assert new_product.unlimited_quantity == True
    assert new_product.description == "new product description"
    assert new_product.sale_price.amount == 5
    assert new_product.cost_price == 8
    assert new_product.sale_end < datetime.now() + timedelta(days=1)
    assert new_product.require_shipping == True
    assert new_product.weight == 10
    assert new_product.sku == "new product sku"
    assert new_product.with_tax == True
    assert new_product.enable_upload_image == True
    # assert new_product.active_advance == True # bug in api

    new_product.name = "old product name"
    new_product.price.amount = 120
    new_product.status = "sale"
    new_product.quantity = 100
    new_product.unlimited_quantity = False
    new_product.description = "old product description"
    # new_product.categories =
    # new_product.min_amount_donating = 100
    # new_product.max_amount_donating = 200
    new_product.sale_price.amount = 10
    new_product.cost_price = 6
    new_product.sale_end = datetime.now()
    new_product.require_shipping = False
    # new_product.maximum_quantity_per_order =
    new_product.weight = 100
    new_product.sku = "old product sku"
    new_product.with_tax = False
    # new_product.hide_quantity =
    new_product.enable_upload_image = False
    # new_product.enable_note =
    # new_product.pinned =
    new_product.active_advance = False
    # new_product.subtitle =
    # new_product.promotion_title =
    # new_product.metadata_title =
    # new_product.metadata_description =
    # new_product.brand_id =
    # new_product.tags =

    new_product.save()

    assert must_be_error(product.save)


def test_delete_product():
    # سيتم كتابتها بعد انشاء المنتج
    pass


def test_create_option():
    product: Product = products.first()

    price = Price(amount=0, currency="SAR")

    value = Value(
        id=0000000000000000,
        name="new value",
        advance=True,
        price=price,
        option_id=0000000,
        translations={},
    )

    option = product.create_option(
        "new option!",
        values=[
            value,
        ],
    )

    new_product: Product = store.products(per_page=1).first()

    assert product.options.last().id == option.id
    assert new_product.options.last().id == option.id


def test_update_option():
    product: Product = products.first()

    option: Option = product.options.last()
    option.name = "new option name"
    option.display_type = "color"

    # option.values =

    product.save()

    assert must_be_error(product.save)

    new_product: Product = store.products(per_page=1).first()

    option: Option = new_product.options.last()

    assert option.name == "new option name" and option.display_type == "color"

    option.name = "old option name"
    option.display_type = "text"

    # option.values =

    new_product.save()


def test_delete_option():
    product: Product = products.first()

    option = product.options.last()
    product.options.delete(option)

    new_product: Product = store.products(per_page=1).first()

    assert option not in product.options
    assert option not in new_product.options


def test_attach_youtube_video():
    product: Product = products.first()

    url = "https://www.youtube.com/watch?v=FUKmyRLOlAA"

    product.attach_youtube_video(url)

    new_product: Product = store.products(per_page=1).first()
    video: Image = product.images.last()
    new_video: Image = new_product.images.last()

    # assert type(video) is Image and type(new_video) is Image
    assert video.video_url == url
    assert new_video.video_url == url


def test_delete_image():
    product: Product = products.first()
    images = product.images
    image: Image = images.last()

    images.delete(image)

    new_images: ImageList = store.products(per_page=1).first().images

    assert image not in images
    assert image not in new_images
