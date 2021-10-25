from salla import types


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


def test_promotion():
    promotion_dict1 = {"title": 9347932222, "sub_title": 8368237}

    promotion1 = types.Promotion(**promotion_dict1)

    assert promotion1.title == "9347932222"
    assert promotion1.sub_title == "8368237"


def test_urls():
    urls_dict1 = {
        "customer": "https://s.salla.sa",
        "admin": "https://s.salla.sa/categories",
    }
    urls_dict2 = {
        "customer": "invalid://url.com",
        "admin": "https://invalidUrl",
    }

    assert must_be_error(types.Urls)
    assert must_be_error(types.Urls, **urls_dict2)

    assert types.Urls(**urls_dict1)


def test_price():
    price_dict1 = {"amount": "300", "currency": "SAR"}
    price_dict2 = {"amount": 250.50, "currency": 2324}

    assert must_be_error(types.Price)

    assert types.Price(**price_dict1)
    assert types.Price(**price_dict2)


def test_image():
    image_dict1 = {
        "id": "1453162244j",
        "url": "79339}}{{{[[*&&",
        "alt": "some()({{{",
        "video_url": "82738?>?><M",
        "type": "12323",
        "sort": 33,
    }

    image_dict2 = {
        "id": 874585853,
        "url": "https://example.com/",
        "type": "some-random-type",
        "sort": 33,
    }

    image_dict3 = {
        "id": 874585853,
        "url": "https://example.com/",
        "type": "video",
        "sort": 33,
    }

    assert must_be_error(types.Image, **image_dict1)
    assert must_be_error(types.Image, **image_dict2)
    assert must_be_error(types.Image)
    assert types.Image(**image_dict3)


def test_rating():
    rating_dict1 = {"total": "300", "count": 434, "rate": 10}
    rating_dict2 = {"total": "3004c", "count": "SAR", "rate": "3s.3"}

    assert must_be_error(types.Rating, **rating_dict2)
    assert must_be_error(types.Rating)

    assert types.Rating(**rating_dict1)


def test_skus():
    skus_dict1 = {
        "id": 119086587,
        "price": {"amount": 299, "currency": "SAR"},
        "regular_price": {"amount": 300, "currency": "SAR"},
        "stock_quantity": 0,
        "barcode": "https://google.com",
        "sku": "njnnfjndjnfn",
        "related_options": [893081174, 814614882, 1546663788],
    }

    skus_dict2 = {
        "price": {"amount": 299, "currency": "SAR"},
        "regular_price": {"amount": 300, "currency": "SAR"},
        "stock_quantity": 0,
        "barcode": "https:google.com",
        "sku": "njnnfjndjnfn",
        "related_options": [893081174, 814614882, 1546663788],
    }

    assert types.Skus(**skus_dict1)
    assert must_be_error(types.Skus, **skus_dict2)
    assert must_be_error(types.Skus)


def test_value():
    value_dict1 = {
        "id": 893081174,
        "name": "44 - XL",
        "price": {"amount": 0, "currency": "SAR"},
        "display_value": None,
        "advance": True,
        "option_id": 2088876887,
        "image_url": None,
        "hashed_display_value": None,
        "translations": {"ar": {"option_details_name": "44 - XL"}},
    }

    value_dict2 = {
        "id": 893081174,
        "price": {"amount": 0, "currency": "SAR"},
        "option_id": "2088876887h",
        "image_url": "invalid url",
        "hashed_display_value": None,
        "translations": {"ar": {"option_details_name": "44 - XL"}},
    }

    assert types.Value(**value_dict1)
    assert must_be_error(types.Value, **value_dict2)
    assert must_be_error(types.Value)


def test_option():
    option_dict1 = {
        "id": 2088876887,
        "name": "المقاس",
        "description": None,
        "type": "radio",
        "required": True,
        "associated_with_order_time": 0,
        "choose_date_time": None,
        "from_date_time": None,
        "to_date_time": None,
        "sort": None,
        "advance": True,
        "display_type": "text",
        "visibility": "always",
        "translations": {"ar": {"option_name": "المقاس", "description": None}},
        "values": [
            {
                "id": 893081174,
                "name": "44 - XL",
                "price": {"amount": 0, "currency": "SAR"},
                "display_value": None,
                "advance": True,
                "option_id": 2088876887,
                "image_url": None,
                "hashed_display_value": None,
                "translations": {"ar": {"option_details_name": "44 - XL"}},
            },
            {
                "id": 117470551,
                "name": "42 - L",
                "price": {"amount": 0, "currency": "SAR"},
                "display_value": None,
                "advance": True,
                "option_id": 2088876887,
                "image_url": None,
                "hashed_display_value": None,
                "translations": {"ar": {"option_details_name": "42 - L"}},
            },
        ],
    }

    option_dict2 = option_dict1.copy()
    option_dict2["display_type"] = "random type"

    assert (option1 := types.Option(**option_dict1))
    assert must_be_error(types.Option, **option_dict2)
    assert must_be_error(types.Option)

    assert option1.values[0].price.amount == 0
    assert option1.values[0].id == 893081174


def test_categories():
    categories_dict1 = {
        "id": 1532791945,
        "name": "قصير",
        "urls": {
            "customer": "https://salla.sa/dev-testPythonStore/قصير/c1532791945",
            "admin": "https://s.salla.sa/categories",
        },
        "items": [
            {
                "id": 2090145686,
                "name": "قصير",
                "urls": {
                    "customer": "https://salla.sa/dev-testPythonStore/قصير/c2090145686",
                    "admin": "https://s.salla.sa/categories",
                },
                "items": [],
                "parent_id": 1532791945,
                "status": "active",
                "sort_order": 0,
                "sub_categories": [],
            }
        ],
        "parent_id": 99911771,
        "status": "active",
        "sort_order": 0,
        "sub_categories": [
            {
                "id": 2090145686,
                "name": "قصير",
                "urls": {
                    "customer": "https://salla.sa/dev-testPythonStore/قصير/c2090145686",
                    "admin": "https://s.salla.sa/categories",
                },
                "items": [],
                "parent_id": 1532791945,
                "status": "active",
                "sort_order": 0,
                "sub_categories": [],
            }
        ],
    }

    categories_dict2 = {
        "id": 1842098062,
        "name": "وردي",
        "urls": {
            "customer": "https://salla.sa/dev-testPythonStore/وردي/c1842098062",
            "admin": "https://s.salla.sa/categories",
        },
        "items": [],
        "parent_id": 99911771,
        "status": "invalid-status",
        "sort_order": 0,
        "sub_categories": [],
    }

    assert (categirie := types.Categories(**categories_dict1))
    assert must_be_error(types.Categories, **categories_dict2)
    assert must_be_error(types.Categories)

    assert categirie.sub_categories[0].parent_id == categirie.id


def test_brand():
    brand_dict1 = {
        "id": 59262354,
        "name": "Awiteb",
        "description": "",
        "banner": None,
        "logo": "https://example.com/",
        "ar_char": "أ",
        "en_char": "a",
    }

    assert types.Brand(**brand_dict1)
    assert must_be_error(types.Brand)
