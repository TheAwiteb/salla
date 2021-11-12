import requests
from pydantic import BaseModel
from typing import Optional, Union
from salla.exceptions import APIError, RateLimitError, AuthorizationError
import salla


class ErrorResponse(BaseModel):
    """
    API خطأ مصدره الـ
    """

    class Error(BaseModel):
        code: str
        """ رمز الخطأ """

        message: Optional[str]
        """ رسالة الخطأ """

        fields: dict = dict()
        """ الحقول التي توجد بها الخطأ """

    status: int
    """ الحالة رمز الرسبونس """

    success: bool
    """ حالة الرسبونس تم ام لم يتم """

    error: Error
    """ الخطأ """


class ApiHelper(BaseModel):
    """
    API يساعدك هذا الكلاس بالتحكم في الـ
    """

    api = "https://api.salla.dev/admin/v2/{method}/"
    """ API الرابط الخاص ب ال """

    token: Optional[str]
    """ التوكن الخاص بالمتجر """

    ratelimit_limit: Optional[int]
    """ اجمالي عدد الطلبات المسموح للمتجر """

    ratelimit_remaining: Optional[int]
    """ العدد المتبقي من الطلبات """

    @property
    def header(self) -> dict:
        """ارجاع الهيدرز مكونة من التوكن ونوع المحتوى

        Returns:
            dict: الهيدرز
        """

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        return headers

    def make_request(self, method_name: str, method: str, **kwargs) -> dict:
        """انشاء ركوست وارجاع الرسبونس

        المدخلات:
            method_name (str): الميثود المراد عمل ركوست عليه
            method (str): 👇 نوع الميثود القيم المسموحة

            ("get", "post", "put", "delete")

        الاخطاء:
            Exception: نوع الميثود غير موجود
            Exception: API خطأ من ال

            👇 وصف الاخطاء

            https://docs.salla.dev/docs/merchent/ZG9jOjIzMjE3MjM5-responses

        المخرجات:
            dict: API الجسون القادم من ال
        """

        request: Union[requests.get, requests.post, requests.put, requests.delete]

        url = self.api.format(method=method_name.strip("/"))

        salla.logger.debug(
            f"request '{method}' {method_name} {kwargs}"
        ) if salla.enable_logging else None

        if (method := method.upper()) == "GET":
            request = requests.get
        elif method == "POST":
            request = requests.post
        elif method == "PUT":
            request = requests.put
        elif method == "DELETE":
            request = requests.delete
        else:
            error_message = f"Invalid method '{method}' unknown method."
            salla.logger.error(error_message) if salla.enable_logging else None
            raise Exception(error_message)

        response = request(url, headers=self.header, **kwargs)

        if (response_json := response.json()).get("success"):
            self.ratelimit_remaining = response.headers.get("x-ratelimit-remaining")
            self.ratelimit_limit = response.headers.get(
                "x-ratelimit-limit", self.ratelimit_limit
            )
            salla.logger.debug(
                f"Successful request, ratelimit remaining: {self.ratelimit_remaining} ratelimit limit: {self.ratelimit_limit}"
            ) if salla.enable_logging else None
            return response_json
        else:
            salla.logger.debug(
                f"Unsuccessful request, ratelimit remaining: {self.ratelimit_remaining} ratelimit limit: {self.ratelimit_limit}"
            ) if salla.enable_logging else None
            self.error_handler(ErrorResponse(**response_json))

    def error_handler(self, error: ErrorResponse) -> None:
        """ميثود تستقبل الاخطأ ومعالجتها

        المتغيرات:
            error (ErrorResponse): الخطأ المراد معالجته

        الاخطأ:
            AuthorizationError: خطأ بالتعرف على المتجر (التوكن غير صحيح)
            RateLimitError: تعدي حد الطلبات
            APIError: API خطأ من ال
        """
        message = error.error.message
        salla.logger.error(
            f"Code: {error.error.code}, status: {error.status}, message:{message}"
        ) if salla.enable_logging else None
        if error.error.code == "Unauthorized":
            raise AuthorizationError
        elif error.status == 429:
            raise RateLimitError(sratelimit_limit=self.ratelimit_limit)
        else:
            raise APIError(
                msg_template=f"""{message}\r
                \r{', ' if error.error.fields else '' + ' ,'.join(msg for lst in error.error.fields.values() for msg in lst)}
                \r""".strip()
            )

    def query2dict(self, query: str) -> dict:
        """تحويل الباراميتر حقت الرابط الى قاموس

        المتغيرات:
            query (str): النص الخاص بالباراميترات

        المخرجات:
            dict: قاموس يحتوي الباراميترات التي كانت بالنص

        مثال:
            apihelper.query2dict("per_page=2&page=2")

            >> {'per_page': '2', 'page': '2'}
        """
        params = {
            key: val
            for param in query.split("&")
            for key, val in zip(param.split("=")[:1], param.split("=")[1:2])
        }
        return params

    def __delete(self, method_name: str) -> None:
        """مسح عبر اسم الميثود

        المتغيرات:
            method_name (str): الميثود المراد المسح منها
        """
        method = "DELETE"
        self.make_request(method_name, method)

    def __create(self, method_name: str, **kwargs) -> dict:
        """انشاء عبر اسم الميثود والمعطيات

        المتغيرات:
            method_name (str): الميثود المراد الانشاء منها

        المخرجات:
            dict: القاموس المرجع من الميثود
        """
        method = "POST"
        return self.make_request(method_name, method, **kwargs)

    def __update(self, method_name: str, **kwargs) -> dict:
        """تحديث عبر اسم الميثود والمعطيات

        المتغيرات:
            method_name (str): الميثود المراد التحديث منها

        المخرجات:
            dict: القاموس المرجع من الميثود
        """
        method = "PUT"
        return self.make_request(method_name, method, **kwargs)

    def products(self, params: dict) -> dict:
        """جلب المنتجات

        المتغيرات:
            params (dict): الباراميتر التي سوف توضع في الرابط

        المخرجات:
            dict: المنتجات
        """
        method_name = "products"
        method = "GET"
        return self.make_request(method_name, method, params=params)

    def change_status(self, product_id: str, new_status: str) -> None:
        """تغير حالة المنتج

        المتغيرات:
            product_id (str): ايدي المنتج
            new_status (str): الحالة الجديدة
        """
        method_name = f"products/{product_id}/status"
        method = "POST"
        params = {"status": new_status}
        self.make_request(method_name, method, params=params)

    def update_product(self, product_id: str, update_dict: dict) -> dict:
        """تعديل المنتج

        المتغيرات:
            product_id (str): ايدي المنتج المراد تعديله
            update_dict (dict): قاموس يحتوي الخيارات المراد تعديلها

        المخرجات:
            dict: المنتج بعد تعديله
        """
        method_name = f"products/{product_id}"
        return self.__update(method_name, json=update_dict)

    def update_option(self, option_id: str, data: dict) -> dict:
        """تحديث محتوى الاختيار

        المتغيرات:
            option_id (str): ايدي الاختيار المراد تحديثه
            data (dict): المحتوى الجديد الخاص بالاختيار

        المخرجات:
            dict: الاختيار بعد تحديثه
        """
        method_name = f"products/options/{option_id}"
        return self.__update(method_name, json=data)

    def delete_product(self, product_id: str) -> None:
        """مسح المنتج

        المتغيرات:
            product_id (str): ايدي المنتج المراد مسحه
        """
        method_name = f"products/{product_id}"
        self.__delete(method_name)

    def delete_image(self, image_id: int) -> None:
        """مسخ الصورة الخاصة بالمنتج

        المتغيرات:
            image_id (int): ايدي الصورة المراد حذفها
        """
        method_name = f"products/images/{image_id}"
        self.__delete(method_name)

    def delete_option(self, option_id: str) -> None:
        """مسح الاختيار عبر الايدي الخاص به

        المتغيرات:
            option_id (str): ايدي الاختيار المراد مسحه
        """
        method_name = f"products/options/{option_id}"
        self.__delete(method_name)

    def create_option(self, product_id: str, data: dict) -> dict:
        """انشاء اختيار جديد في المنتج

        المتغيرات:
            product_id (str): ايدي المنتج المراد انشاء الاختيار له
            data (dict): بيانات الاختيار

        المخرجات:
            dict: محتوى الاختيار
        """
        method_name = f"products/{product_id}/options"
        return self.__create(method_name, json=data)

    def create_product(self, data: dict) -> dict:
        """انشاء منتج

        المتغيرات:
            data (dict): بيانات المنتج المراد انشائه

        المخرجات:
            dict: المنتج بعد انشائه
        """
        method_name = "products"
        return self.__create(method_name, json=data)

    def store_details(self) -> dict:
        """ارجاع تفاصيل المتجر

        المخرجات:
            dict: تفاصيل المتجر
        """
        method_name = "oauth2/user/info"
        method = "GET"
        response_dct = self.make_request(method_name, method).get("data")
        details = response_dct.pop("store")
        details.update(owner=response_dct)
        return details

    def attach_youtube_video(self, product_id: str, **kwargs) -> dict:
        """اضافة مقطع يوتيوب الى المنتج

        المتغيرات:
            product_id (str): ايدي المنتج المراد اضافة الفديو له

        المخرجات:
            dict: قاموس يحتوي الفديو اللذي تم اضافته
        """
        method_name = f"products/{product_id}/video"
        method = "POST"
        response_dict = self.make_request(method_name, method, **kwargs).get("data")
        response_dict["sort"] = response_dict.get("sort") or 0
        response_dict.update(url=response_dict["image"]["original"].get("url"))
        return response_dict


apihelper = ApiHelper()
""" API الوسيط بين المتجر و ال"""
