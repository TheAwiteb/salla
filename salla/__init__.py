from pydantic import BaseModel
from typing import Optional
from os import getenv
import salla.exceptions
import salla.product
import salla.version
import salla.apihelper
import salla.types
import salla.validators

version_info = salla.version.version_info

version = salla.version.__version__
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

    details: Optional[salla.types.Store]
    """ تفاصيل المتجر """

    def __init__(
        self, token, enable_logging: bool = True, logging_filename: str = "logging.log"
    ) -> None:

        if token == "TOKEN":
            token = getenv("SALLA_TOKEN")
            if not token:
                raise salla.exceptions.EnvironmentVariableError(
                    name="token", env_variable="SALLA_TOKEN"
                )

        super(Salla, self).__init__(
            token=token,
            enable_logging=enable_logging,
            logging_filename=logging_filename,
        )
        salla.apihelper.apihelper.token = token
        salla.apihelper.apihelper.enable_logging = enable_logging
        salla.apihelper.apihelper.logging_filename = logging_filename

        self.details = salla.apihelper.apihelper.store_details()

    def products(
        self,
        category: str = None,
        keyword: str = None,
        page: int = None,
        per_page: int = None,
        status: str = None,
    ) -> salla.product.ProductList:
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

        response_json = salla.apihelper.apihelper.products(params=params)
        products = response_json.get("data", [])
        pagination = response_json.get("pagination", {})
        return salla.product.ProductList(products=products, pagination=pagination)
