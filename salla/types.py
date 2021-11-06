## في هذا الملف المهم سوف تتواجد اغلب التايبس الخاصة بسلة
## لماذا الاغلب لانه فيه تايب تكون كبيرة، المنتج مثلا ماينفع نحطه مع التايبس الصغيرة

from pydantic import BaseModel, validator, HttpUrl, Field
from typing import Optional, List, Any, Union
from datetime import datetime
import salla
from salla.validators import choice_validator, date_parser
from salla.apihelper import apihelper


class Promotion(BaseModel):
    """تفاصيل ترويج المنتج"""

    title: Optional[str]
    """ عنوان الترويج """

    sub_title: Optional[str]
    """ العنوان الفرعي للترويج """


class Urls(BaseModel):
    """
    لمساعدة الشركات والتجار،توفر سلة  سمة "الروابط"
    التي تمت إضافتها إلى وحدات مختلفة لتوجيه التجار للحصول على العنوان (الرابط)
    الكامل لهذه الوحدة من كلا النطاقين ونطاق لوحة المعلومات كمسؤول متجر وكعميل.
    """

    customer: HttpUrl
    """ الرابط الخاص بالعميل """

    admin: HttpUrl
    """ الرابط الخاص بالتاجر """


class Price(BaseModel):
    """تفاصيل السعر"""

    amount: float
    """ السعر """

    currency: str
    """ العملة """


class ImageDetails(BaseModel):
    """تفاصيل الصورة"""

    class Details(BaseModel):
        """التفاصيل"""

        url: HttpUrl
        """ رابط الصورة """

        width: int
        """ عرض الصورة """

        height: int
        """ طول الصورة """

    original: Details
    """ الصورة الاصلية """

    standard_resolution: Details
    """ الصورة بجودة متوسطة """

    low_resolution: Details
    """ الصورة بجودة منخفضة """

    thumbnail: Details
    """ الثامنيل """


class Image(BaseModel):
    """الصورة او الفديو الخاصة بالمنتج"""

    id: int
    """ الايدي الخاص بالصورة او الفديو """

    image: Optional[ImageDetails]
    """ تفاصيل صورة المنتج """

    url: HttpUrl
    """ الرابط الخاص بالصورة """

    alt: Optional[str]
    """ النص بديل الصورة اذ لم تكن تعمل """

    alt_seo: Optional[str]
    """ وصف الفديو """

    video_url: Optional[str]  # Optional[HttpUrl]
    """ الرابط الخاص بالفديو """

    type: str
    """ النوع صورة ام فديو\n
    القيم المسموحة\n
    ["image", "video"]
    """

    sort: int
    """ ترتيب الصورة او الفديو بين باقي الصور """

    default: Optional[bool]
    """ الصورة هي الصورة الافتراضية للمنتج """

    @validator("type")
    @classmethod
    def type_validator(cls, type_value: str) -> str:
        return choice_validator(cls, type_value, ["image", "video"])


class Rating(BaseModel):
    """تفاصيل تقيمات المنتج"""

    total: int
    """ مجموع التقيمات """

    count: int
    """ عدد الاشخاص الذين قامو بالتقييم """

    rate: float
    """ تقييم المنتج """


class Skus(BaseModel):
    """الخاصة بالقيمة الخاصة الاختيار الخاص بالمنتج Skus تفاصيل ال"""

    id: int
    """ skus الايدي الخاص بـ """

    price: Price
    """ سعر المنتج """

    regular_price: Price
    """ skus سعر الـ \n
    (skus سوف يتم اضافة هاذه السعر عند اختيار ال القيمة التي يتبع لها هذا الـ )
    """

    sale_price: Optional[Price]
    """ سعر الخصم """

    stock_quantity: Optional[int]
    """ الكمية الموجودة من هذه القيمة """

    barcode: Optional[str]  # Optional[HttpUrl]
    """  الخاص بالقيمة barcode الـ """

    sku: Optional[str]
    """ sku رمز الـ"""

    related_options: List[int]
    """ الاختيارات التي تعود لها هذه القيمة """


class Value(BaseModel):
    """القيمة الخاصة الاختيار الخاص بالمنتج"""

    id: int
    """ ايدي القيمة """

    name: str
    """ القيمة يتم حفظها هنا """

    price: Price
    """ سعر المضاف من اجل الاختيار """

    display_value: Optional[str]
    """ ستستخدم قيمة العرض في واجهة المستخدم بناءً على نوع عرض الخيار
    ، بشكل افتراضي ، ستستخدم اسم القيمة كقيمة عرض عندما تكون "display_value = text" ،
    ولكن في حالة استخدامك لـ "image" ، فأنت بحاجة إلى تعيين معرف الصورة كقيمة """

    advance: bool
    """ """

    option_id: int
    """ ايدي الاختيار """

    image_url: Optional[HttpUrl]
    """ رابط الصورة """

    hashed_display_value: Optional[str]
    """ اللون """

    translations: dict
    """ قاموس تحتوي على اللغات المترجمة لها القيمة """

    # product.py@Product تم اسناد القيم لها في
    skus: Optional[Skus]
    """ الخاص بالقيمة skus الـ """


class Option(BaseModel):
    """الاختيار الخاص بالمنتج"""

    id: int
    """ الايدي الخاص بالاختيار """

    name: str
    """ اسم الاختيار """

    description: Optional[str]
    """ وصف الاختيار """

    type: str
    """ نوع الاختيار """

    required: bool
    """ الاختيار مطلوب ام لا """

    associated_with_order_time: bool
    """ هو خيار متعلق بوقت استلام الطلب. لخيارات التاريخ والوقت فقط """

    # choose_date_time
    # """ """

    # from_date_time
    # """ """

    # to_date_time
    # """ """

    advance: bool
    # """ """

    sort: Optional[int]
    """ فرز الاختيار """

    display_type: str
    """ نوع عرض الاختيار\n
    ("color", "image", "text") """

    visibility: str
    """ .رؤية  الاختيار على أساس الشرط\n
    تستخدم فقط للمنتجات مع نوع \n
    (food, service)\n
    القيم المسموحة:
    ("always", "on_condition")
    """

    translations: dict
    """ قاموس على اللغات المترجم لها الاختيار """

    values: List[Value]
    """ القيم الخاصة بالاختيار """

    @validator("display_type")
    @classmethod
    def display_type_validator(cls, display_type_value: str) -> str:
        """من ضمن القيم المسموحة display_type التحقق ان الـ

        المتغيرات:
            display_type_value (str): display_type قيمة ال

        الاخطاء:
            InvalidValueError: من ضمن القيم المسموحة display_type خطأ بعدم وجود ال

        المخرجات:
            str: بعد التحقق من وجوده ضمن القيم المسموحة display_type ال
        """
        return choice_validator(cls, display_type_value, ["color", "image", "text"])

    @validator("visibility")
    @classmethod
    def visibility_validator(cls, visibility_value: str) -> str:
        """من ضمن القيم المسموحة visibility التحقق ان الـ

        المتغيرات:
            visibility_value (str): visibility قيمة ال

        الاخطاء:
            InvalidValueError: من ضمن القيم المسموحة visibility خطأ بعدم وجود ال

        المخرجات:
            str: بعد التحقق من وجوده ضمن القيم المسموحة visibility ال
        """
        return choice_validator(cls, visibility_value, ["always", "on_condition"])


class Categories(BaseModel):
    """
    تفاصيل فئة المنتج
    """

    id: int
    """ ايدي الفئة """

    name: str
    """ اسم الفئة """

    urls: Urls
    """ الروابط الخاصة بالفئة """

    parent_id: int
    """ ايدي الفئة الاصلي (الي متفرعة منها هاذه الفئة)"""

    status: str
    """ حالة الفئة\n
    القيم المسموحة: \n 
    ("active", "hidden")
    """

    sort_order: int
    """ ايدي فرز الفئة - يُستخدم لتعيين ترتيب الفئة """

    sub_categories: list
    """ الفئات الفرعية """

    def __init__(self, sub_categories: list, **kwargs) -> None:
        """
        تم استخدام ميثود التهيئة هاذه لان نوع الفئات الفرعية هو نفس نوع فئة المنتج
        ولايمكن استدعاء الكلاس داخل نفسه لهذا تم اسناد فيمة الفئات الفرعية في هاذه الميثود

        المتغيرات:
            sub_categories (list): مصفوفة تحتوي الفئات الفرعية
        """
        sub_categories: List[Categories] = [
            Categories(**sub_categorie) for sub_categorie in sub_categories
        ]
        super(Categories, self).__init__(sub_categories=sub_categories, **kwargs)

    @validator("status")
    @classmethod
    def status_validator(cls, status_value: str) -> str:
        """من ضمن القيم المسموحة status التحقق ان الـ

        المتغيرات:
            status_value (str): status قيمة ال

        الاخطاء:
            InvalidValueError: من ضمن القيم المسموحة status خطأ بعدم وجود ال

        المخرجات:
            str: بعد التحقق من وجوده ضمن القيم المسموحة status ال
        """
        return choice_validator(cls, status_value, ["active", "hidden"])


class Brand(BaseModel):
    """تفاصيل العلامة التجارية"""

    id: int
    """ الايدي الخاص بالعلامة التجارية """

    name: str
    """ اسم العلامة التجارية"""

    description: Optional[str]
    """ وصف العلامة التجارية"""

    banner: Optional[str]  # Optional[HttpUrl]
    """ شعار العلامة التجارية """

    logo: Optional[str]  # Optional[HttpUrl]
    """ شعار العلامة التجارية """

    ar_char: str
    """ الرمز العربي الخاص بالعلامة التجارية """

    en_char: str
    """ الرمز الانجليزي الخاص بالعلامة التجارية """


class Pagination(BaseModel):
    """ترقيم الصفحات"""

    class Links(BaseModel):
        """الروابط، التالي والسابق"""

        previous: Optional[HttpUrl]
        """ الرابط السابق"""

        next: Optional[HttpUrl]
        """ الرابط التالي """

    count: int
    """ عدد العناصر في الصفحة """

    total: int
    """ اجمالي عدد العناصر في جميع الصفحات """

    per_page: int = Field(alias="perPage")
    """ عدد العناصر في كل صفحة """

    current_page: int = Field(alias="currentPage")
    """ رقم الصفحة الحالية """

    total_pages: int = Field(alias="totalPages")
    """ اجمالي عدد الصفحات """

    links: Links
    """ الروابط، التالي والسابق"""


class Store(BaseModel):
    """
    بيانات المتجر
    """

    class Owner(BaseModel):
        """
        بيانات صاحب المتجر
        """

        id: int
        """ الايدي الخاص بصاحب المتجر """

        name: str
        """ اسم صاحب المتجر """

        email: str
        """ الايميل الخاص بصاحب المتجر"""

        mobile: str
        """ رقم صاحب المتجر """

        role: str

        created_at: datetime
        """ تاريخ انشاء حساب صاحب المتجر """

        @validator("created_at", pre=True)
        @classmethod
        def date_parser(cls, date):
            return date_parser(cls, date)

    id: int
    """ ايدي المتجر """

    owner: Owner
    """ معلومات صاحب المتجر """

    username: str
    """ اسم المتجر (يظهر في الرابط)"""

    url: Optional[str]
    """ الرابط الخاص بالمتجر """

    name: str
    """ اسم المتجر (يظهر في المتجر)"""

    avatar: Optional[str]
    """ الصورة الخاصة بالمتجر """

    store_location: Optional[str]
    """ موقع المتجر """

    plan: str
    """ خطة المتجر """

    status: str
    """ حالة المتجر """

    created_at: datetime
    """ تاريخ انشاء المتجر"""

    def __init__(self, **kwargs) -> None:
        super(Store, self).__init__(**kwargs)
        self.url = salla.SALLA_URL + self.username

    @validator("created_at", pre=True)
    @classmethod
    def date_parser(cls, date) -> datetime:
        """datetime تحويل التاريخ من نص الى

        المتغيرات:
            date (str): التاريخ بشكل نص

        المخرجات:
            datetime: التاريخ بعد تحويله
        """
        return date_parser(cls, date)


class ListHelper:
    """
    كلاس مساعد لادارة مصفوفة داخل كلاس

    تنويه:
        يجب ان يكون الكلاس هو اول كلاس ترث منه

    مثال:
        class Foo(ListHelper, Another)
    """

    def __init__(self, **kwargs):
        """
        يجب عليك تمرير المصفوفة مثل بالاسفل لكي يتمكن الكلاس من الوصول لها
        ListHelper.__init__(self, lst_name=lst_name)
        """
        self.list_name = list(kwargs.keys())[0]
        """ اسم المصفوفة """

    def first(self) -> Any:
        """ارجاع اول عنصر في المصفوفة

        المخرجات:
            Any: العنصر
        """
        return self.__dict__.get(self.list_name)[0]

    def last(self) -> Any:
        """ارجاع اخر عنصر في المصفوفة

        المخرجات:
            Any: العنصر
        """
        return self.__dict__.get(self.list_name)[-1]

    def __iter__(self):
        return self.__dict__.get(self.list_name).__iter__()

    def __len__(self) -> int:
        """ارجاع عدد العنصرات التي في المصفوفة

        المخرجات:
            int: عدد العنصرات
        """
        return len(self.__dict__.get(self.list_name))

    def __eq__(self, other) -> bool:
        """ارجاع صحيح اذا تطابقت المصفوفة مع المصفوفة المعطاء

        المتغيرات:
            other: اوبجكت المصفوفة المراد التحقق من عنصراتها

        الاخطاء:
            TypeError: المصفوفة المعطاء ليست نفس كلاس المصفوفة الموجودة

        المخرجات:
            bool: صحيح اذا كانت متطابقة
        """
        if type(other) == self.__class__:
            return len(self.__dict__.get(self.list_name)) == len(
                other.__dict__.get(other.list_name)
            ) and all(
                elm == other_elm
                for elm, other_elm in zip(
                    self.__dict__.get(self.list_name),
                    other.__dict__.get(other.list_name),
                )
            )
        else:
            raise TypeError

    def __getitem__(self, index: int) -> Any:
        """جلب عنصر من المصفوفة

        المتغيرات:
            index (int): الاندكس

        الاخطاء:
            IndexError: الاندكس ليس موجود في المصفوفة (اكبر من حجمها)

        المخرجات:
            Any: العنصر بحسب الاندكس اعلاه
        """
        return self.__dict__.get(self.list_name).__getitem__(index)


class ImageList(ListHelper, BaseModel):
    """
    كلاس يحتوي مصفوفة الصور، ويمكنك من خلاله مسح الميدياء
    """

    images: List[Image]
    """ الميدياء """

    list_name: Optional[str]
    """اسم المصفوفة التي تحتوي الميدياء"""

    def __init__(self, **kwargs) -> None:
        BaseModel.__init__(self, **kwargs)
        ListHelper.__init__(self, images=self.images)

    @classmethod
    def delete_(cls, image: Union[int, Image]) -> None:
        """مسح الميدياء عبر تمرير الايدي او الاوبجكت المراد مسحه

        المتغيرات:
            image (Union[str, Image]): الميدياء المراد مسحه او الايدي الخاص بها
        """
        apihelper.delete_image(image.id if type(image) is Image else image)

    def delete(self, image: Union[int, Image]) -> None:
        """مسح الميدياء عبر تمرير الايدي او الاوبجكت المراد مسحه

        المتغيرات:
            image (Union[str, Image]): الميدياء المراد مسحه او الايدي الخاص بها
        """
        self.__class__.delete_(image)
        if image := list(
            filter(
                lambda image_: (image_.id == image.id)
                if type(image) is Image
                else (image_.id == image),
                self.images,
            )
        ):
            self.images.remove(image[0])


class OptionList(ListHelper, BaseModel):
    """
    كلاس يحتوي مصفوفة الاختيارات يمكنك من خلاله بسح وانشاء اختيار جديد
    """

    options: List[Option]
    """ مصفوفة الاختيارات """

    list_name: Optional[str]

    def __init__(self, **kwargs) -> None:
        BaseModel.__init__(self, **kwargs)
        ListHelper.__init__(self, options=self.options)

    @classmethod
    def delete_(cls, option: Union[int, Option]) -> None:
        """مسح الاختيار عبر تمرير الايدي او الاوبجكت المراد مسحه

        المتغيرات:
            option (Union[str, Option]): الاختيار المراد مسحه او الايدي الخاص به
        """
        apihelper.delete_option(option.id if type(option) is Option else option)

    def delete(self, option: Union[int, Option]) -> None:
        """مسح الاختيار عبر تمرير الايدي او الاوبجكت المراد مسحه

        المتغيرات:
            option (Union[str, Option]): الاختيار المراد مسحه او الايدي الخاص بها
        """
        self.__class__.delete_(option)
        if option := list(
            filter(
                lambda option_: (option_.id == option.id)
                if type(option) is Option
                else (option_.id == option),
                self.options,
            )
        ):
            self.options.remove(option[0])
