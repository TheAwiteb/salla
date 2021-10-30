from pydantic import BaseModel
from typing import Optional
from os import getenv
from .exceptions import EnvironmentVariableError
from .product import ProductList
from .version import __version__
from .apihelper import apihelper
from .types import Store

version = __version__
""" اصدار المكتبة """

SALLA_URL = "https://salla.sa/"
""" الرابط الخاص بموقع سلة """


class Salla(BaseModel):
    """
    المتجر الخاص بك يمكنك القيام بالعمليات التي توفرها سلة من خلاله
    https://docs.salla.dev/docs/merchent/
    """

    class Config:
        validate_assignment = True

    token: str
    """ التوكن الخاص بالمتجر"""

    enable_logging: Optional[bool]
    """ تسجيل الاحداث """

    logging_filename: Optional[str]
    """ اسم ملف الاحداث """

    details: Optional[Store]
    """ تفاصيل المتجر """

    def __init__(
        self, token, enable_logging: bool = True, logging_filename: str = "logging.log"
    ) -> None:

        if token == "TOKEN":
            token = getenv("SALLA_TOKEN")
            if not token:
                raise EnvironmentVariableError(name="token", env_variable="SALLA_TOKEN")

        super(Salla, self).__init__(
            token=token,
            enable_logging=enable_logging,
            logging_filename=logging_filename,
        )
        apihelper.token = token
        apihelper.enable_logging = enable_logging
        apihelper.logging_filename = logging_filename

        self.details = apihelper.store_details()

    def products(
        self,
        category: str = None,
        keyword: str = None,
        page: int = None,
        per_page: int = None,
        status: str = None,
    ) -> ProductList:
        """
        يمكنك سرد جميع المنتجات المتاحة المتعلقة بمتجرك مباشرة
            أيضًا ، يسمح لك بتصفية الكلمات الرئيسية والحالة والفئة.

        المدخلات:
            category (str): احصل على المنتجات المدرجة في فئة معينة.
            keyword (str): تصفية المنتجات مع اسم محدد أو SKU.
            page (int): رقم الصفحة.
            per_page (int): حد المنتجات لكل صفحة.
            status (str): احصل على منتجات مطابقة للحالة المحددة. القيم المتاحة (hidden,sale,out)

        مثال:
            store = salla.Salla("TOKEN")
            for product in store.products():
                print(product.name)

        مثال:
            store = salla.Salla("TOKEN")
            #حفط المنتجات في مصفوفة
            products = list(store.products())

        المخرجات:
            ProductList: المنتجات
        """

        # تحويل الباراميترس الى قاموس
        params = {
            key: val for key, val in locals().items() if key not in ["params", "self"]
        }

        response_json = apihelper.products(params=params)
        products = response_json.get("data", [])
        pagination = response_json.get("pagination", {})
        return ProductList(products=products, pagination=pagination)
