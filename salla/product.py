from datetime import datetime
from pydantic import BaseModel, validator
from typing import Optional, Union, List, Any
from threading import Thread
from salla.apihelper import apihelper
from salla.exceptions import PaginationError, SaveProductErorr
from salla.validators import date_parser, choice_validator
from salla import util
from salla.types import (
    Promotion,
    Urls,
    Price,
    Rating,
    Brand,
    Image,
    ImageList,
    Option,
    OptionList,
    Skus,
    Value,
    Categories,
    Pagination,
    ListHelper,
)

update_product_keys = [
    "name",
    "price",
    "status",
    "quantity",
    "unlimited_quantity",
    "description",
    "categories",
    "min_amount_donating",
    "max_amount_donating",
    "sale_price",
    "cost_price",
    "sale_end",
    "require_shipping",
    "maximum_quantity_per_order",
    "weight",
    "sku",
    "with_tax",
    "hide_quantity",
    "enable_upload_image",
    "enable_note",
    "pinned",
    "active_advance",
    "subtitle",
    "promotion_title",
    "metadata_title",
    "metadata_description",
    "brand_id",
    "tags",
]


class Product(BaseModel):
    """
    المنتج
    https://docs.salla.dev/docs/merchent/b3A6MTMzOTUw-list-products
    """

    # TODO:
    # اضافة الميثودز الخاصة بالمنتج

    date_format = "%Y-%m-%d %X"
    """ تنسيق الوقت """

    previous_dict: Optional[dict]
    """ القاموس السابق الخاص بالمنتج """

    id: int
    """ ايدي المنتج """

    promotion: Promotion
    """ تفاصيل ترويج المنتج """

    sku: str
    """ الرقم التعريفي للمنتج """

    type: str
    """ نوع المنتج\n
    القيم المسموحة\n
    ("product", "service", "group_products", "codes", "digital", "food", "donating")
    """

    name: str
    """ اسم المنتج """

    short_link_code: str
    """ الكود الخاص بالرابط المختصر """

    urls: Urls
    """ الروابط الخاصة بالمنتج """

    price: Price
    """ سعر المنتج """

    taxed_price: Price
    # """ """

    pre_tax_price: Price
    # """ """

    tax: Price
    # """ """

    description: Optional[str]
    """ وصف المنتج """

    quantity: Optional[int]
    """ كمية المنتج """

    unlimited_quantity: bool
    """ اظهار اذا كان المنتج يحتوي كمية محدودة ام لا """

    status: str
    """ حالة المنتج \n
    القيم المسموحة: \n
    ("none", "sale", "out", "hidden", "deleted")
    """

    is_available: bool
    """ المنتج متوفؤ ام لا """

    views: int
    """ عدد مشاهدي المنتج """

    sale_price: Price
    """ سعر تخفيض المنتج """

    sale_end: Optional[datetime]
    """ تاريخ نهاية التخفيض """

    require_shipping: bool
    """ تحديد اذا كان المنتج يتطلب شحن ام لا """

    cost_price: Optional[float]
    """ سعر التكلفة """

    weight: float
    """ وزن المنتج """

    with_tax: bool
    """ مع ضريبة ام لا """

    url: str
    """ رابط المنتج """

    images: Optional[ImageList]
    """ الصور والفديوهات الخاصة بالمنتج """

    sold_quantity: int
    """ الكمية المباعة من المنتج """

    sold_quantity_desc: Optional[str]
    """ وصف كمية المنتج المباعة """

    rating: Rating
    """ تفاصيل تقيمات المنتج """

    show_purchase_count: Optional[bool]
    """ اطهار عدد الشراء موجود ام لا """

    has_special_price: Optional[bool]
    """ المنتج لديه سعر مخصص """

    max_items_per_user: int
    """ اكبر كمية يمكن شراؤها للشخص الواحد """

    allow_attachments: bool
    """ السماح بالمرفقات أم لا """

    is_pinned: bool
    """ المنتج مثبت ام لا """

    pinned_date: Union[datetime, str]
    """التاريخ الذي تم تثبيت المنتج فيه """

    active_advance: Optional[bool]
    """تفاصيل المنتج المتقدمة نشطة أم لا """

    enable_upload_image: bool
    """السماح بالمستخدمين برفع الصور """

    updated_at: datetime
    """ تاريخ اخر تعديل على المنتج"""

    options: OptionList
    """ خيارات المنتج مثل الالوان والمقاسات """

    categories: List[Categories]
    """ الفئات التي يتبع لها المنتج """

    brand: Optional[Brand]
    """ العلامة التجارية الخاصة بالمنتج """

    def __init__(self, skus: list, options: list, images: list, **kwargs):
        """
        options في الـ value الخاصة بكل skus تم انشاء دالة التهيئة هاذيه لكي يتم اسناد فيم ال
        ومن اجل تعيين بعض القيمة الافتراضية

        المتغيرات:
            skus (list): الخاص بجميع القيم skus الـ
            options (list):  خيارات المنتج مثل الالوان والمقاسات
        """
        images = ImageList(images=images)
        skus: List[Skus] = [Skus(**skus_) for skus_ in skus]
        options: List[Option] = [Option(**option) for option in options]

        for option in options:
            option = util.add_skus_to_option(skus, option)

        options: OptionList = OptionList(options=options)
        kwargs.update(options=options, images=images)
        super(Product, self).__init__(**kwargs)
        self.previous_dict: dict = self.dict().copy()

    def get_changed_values(self) -> List[str]:
        """ارجاع العناصر التي تم تعديلها

        المخرجات:
            List[str]: مصفوفة تحتوي العناصر التي تم تعديلها
        """
        return list(
            map(
                lambda key: key,
                filter(
                    lambda key: self.dict().get(key) != self.previous_dict.get(key)
                    and key != "previous_dict",
                    self.previous_dict,
                ),
            )
        )

    def get_update_product_dict(self) -> dict:
        """ارجاع القاموس الخاص بميثود تعديل المنتج

        المخرجات:
            dict: القاموس الخاص بميثود تعديل المنتج
        """
        return util.get_dict_of(update_product_keys, self.dict())

    def change_status(self, new_status: str) -> None:
        """تغير حالة المنتج

        المتغيرات:
            new_status (str): الحالة الجديدة
        """
        if Product.status_validator(new_status):
            self.status = new_status
            apihelper.change_status(self.id, new_status)

    def attach_youtube_video(
        self,
        youtube_video_url: str,
        default: bool = False,
        alt: str = str(),
        sort: int = 0,
    ) -> None:
        """اضافة مقطع يوتيوب الى المنتج

        المتغيرات:
            youtube_video_url (str): رابط مقطع اليوتيوب المراد اضافته الى المنتج
            default (bool, optional): جعل الفديو هو الميديا الافتراضية للمنتج. Defaults to False.
            alt (str, optional): وصف الفديو (سوف يظهر عندما يتعطل الرابط). Defaults to str().
            sort (int, optional): ترتيب الفديو بين الميديا الخاصة بالمنتج. Defaults to 0.
        """
        data = {}
        data.update(video_url=youtube_video_url, default=default, alt=alt, sort=sort)
        image = Image(**apihelper.attach_youtube_video(product_id=self.id, json=data))
        self.images.images.append(image)

    def create_option(
        self,
        name: str,
        values: List[Value],
        display_type: Optional[str] = None,
    ) -> Option:
        """انشاء اختيار للمنتج

        المتغيرات:
            name (str): اسم الاختيار
            values (List[Value]): القيم الخاصة بالاختيار
            display_type (Optional[str], optional): نوع الاختيار ( text - image - color). Defaults to None.

        المخرجات:
            Option: الاختيار الذي تم انشائه
        """
        kwargs = {
            key: val for key, val in locals().items() if key not in ["kwargs", "self"]
        }
        option = self.options.create(self.id, **kwargs)
        self.previous_dict = self.dict().copy()
        return option

    def __save(self) -> None:
        """
        ميثود خاصة تقوم بحفظ التغيرات التي حدثت على المنتج
        """
        product_dict = self.get_update_product_dict()
        self = Product(**apihelper.update_product(self.id, product_dict).get("data"))

    def save(self):
        """
        حفط التغيرات التي حدثت على المنتج
        """
        has_changed = self.get_changed_values()

        if has_changed:
            threads = []
            if "options" in has_changed:
                threads.append(
                    self.options._save(self.previous_dict.get("options").get("options"))
                )
            if any(key in update_product_keys for key in has_changed):
                thread = Thread(target=self.__save)
                thread.start()
                threads.append(thread)

            util.join_threads(threads)

            self.previous_dict = self.dict().copy()
        else:
            raise SaveProductErorr(message="No changes have been made to the product.")

    @validator("updated_at", "pinned_date", "sale_end", pre=True)
    @classmethod
    def parse_date(cls, date: str) -> datetime:
        """datetime تحويل التاريخ من نص الى

        المتغيرات:
            date (str): التاريخ بشكل نص

        المخرجات:
            datetime: التاريخ بعد تحويله
        """
        return date_parser(cls, date)

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
        return choice_validator(
            cls, status_value, ["none", "sale", "out", "hidden", "deleted"]
        )

    @validator("type")
    @classmethod
    def type_validator(cls, type_value: str) -> str:
        """من ضمن القيم المسموحة type التحقق ان الـ

        المتغيرات:
            type_value (str): type قيمة ال

        الاخطاء:
            InvalidValueError: من ضمن القيم المسموحة type خطأ بعدم وجود ال

        المخرجات:
            str: بعد التحقق من وجوده ضمن القيم المسموحة type ال
        """
        return choice_validator(
            cls,
            type_value,
            [
                "product",
                "service",
                "group_products",
                "codes",
                "digital",
                "food",
                "donating",
            ],
        )


class ProductList(ListHelper, BaseModel):
    """
    كلاس يحتوي مصفوفة المنتجات، ويمكنك من خلاله التحكم بالصفحات
    """

    products: List[Product]
    """ المنتجات """

    pagination: Pagination
    """ ترقيم الصفحات """

    list_name: Optional[str]
    """ اسم المصفوفة التي تحتوي المنتجات """

    def __init__(self, **kwargs) -> None:
        BaseModel.__init__(self, **kwargs)
        ListHelper.__init__(self, products=self.products)

    def have_next(self) -> bool:
        """ارجاع قيمة صحيحة اذ وجد صفحة تالية

        المخرجات:
            bool: ارجاع قيمة صحيحة اذ وجد صفحة تالية
        """
        return not not self.pagination.links.next

    def have_previous(self) -> bool:
        """ارجاع قيمة صحيحة اذ وجد صفحة سابقة

        المخرجات:
            bool: ارجاع قيمة صحيحة اذ وجد صفحة سابقة
        """
        return not not self.pagination.links.previous

    def next(self) -> "ProductList":
        """تغير الصفحة الى الصفحة التالية

        الاخطاء:
            PaginationError: عدم وجود صفحة تالية

        المخرجات:
            ProductList: المنتجات بعد تغير الصفحة
        """
        if self.have_next():
            return self.page(self.pagination.current_page + 1)
        else:
            raise PaginationError(type="next")

    def previous(self) -> "ProductList":
        """تغير الصفحة الى الصفحة السابقة

        الاخطاء:
            PaginationError: عدم وجود صفحة سابقة

        المخرجات:
            ProductList: المنتجات بعد تغير الصفحة
        """
        if self.have_previous():
            self.page(self.pagination.current_page - 1)
        else:
            raise PaginationError(type="previous")

    def page(self, page_number: int) -> "ProductList":
        """الانتقال الى الصفحة المعطى رقمها

        الاخطأ:
            PaginationError: رقم صفحة غير صحيح
            TypeError: المعطى ليس رقم

        المخرجات:
            ProductList: المنتجات بعد تغير الصفحة
        """
        if type(page_number) is int:
            if 1 <= page_number <= self.pagination.total_pages:
                param = {
                    "per_page": self.pagination.per_page,
                    "page": page_number,
                }
                response_json = apihelper.products(param)
                self.products = [
                    Product(**dct) for dct in response_json.get("data", [])
                ]
                self.pagination = Pagination(**response_json.get("pagination", {}))
                return self
            else:
                raise PaginationError(message=f"Invalid page number, {page_number}.")
        else:
            raise TypeError

    @classmethod
    def delete_(cls, product: Union[str, Product]) -> None:
        """مسح المنتج

        المتغيرات:
            product (Union[str, Product]): المنتج المراد مسحه او الايدي الخاص به
        """
        apihelper.delete_product(product.id if type(product) is Product else product)

    def delete(self, product: Union[str, Product]) -> None:
        """مسح المنتج

        المتغيرات:
            product (Union[str, Product]): المنتج المراد مسحه او الايدي الخاص به
        """
        self.__class__.delete_(product)
        if product := list(
            filter(
                lambda product_: (product_.id == product.id)
                if type(product) is Product
                else (product_.id == product),
                self.products,
            )
        ):
            self.products.remove(product[0])

        if len(self.products) == 0:
            if self.have_previous():
                self.previous()
            elif self.have_next():
                self.next()
