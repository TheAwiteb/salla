from .product import ProductList
from .apihelper import apihelper


class Salla:
    """
    المتجر الخاص بك يمكنك القيام بالعمليات التي توفرها سلة من خلاله
    https://docs.salla.dev/docs/merchent/
    """

    def __init__(
        self,
        token: str,
        enable_logging: bool = True,
        logging_filename: str = "logging.log",
    ) -> None:

        self.token = token
        self.apihelper = apihelper
        self.apihelper.token = token
        self.apihelper.enable_logging = (enable_logging,)
        self.apihelper.logging_filename = (logging_filename,)

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

        response_json = self.apihelper.products(params=params)
        products = response_json.get("data", [])
        pagination = response_json.get("pagination", {})
        return ProductList(products=products, pagination=pagination)
