from pydantic import PydanticValueError
from typing import Union, List, Optional


class InvalidValueError(PydanticValueError):
    """
    خطأ اذ لم تكن القيمة ضمن اقيم المسموحة
    """

    code = "invalid_value_error"
    choices: List[Union[str, int, float]]
    wrong_value: Union[str, int, float]
    msg_template = '"{wrong_value}" is invalid value, the value should be in {choices}.'


class SaveProductErorr(PydanticValueError):
    """
    خطأ في حفط المنتج
    """

    code = "product_save_error"
    message: str
    msg_template = "Cannot save product, {message}"


class PaginationError(PydanticValueError):
    """
    خطأ في الصفحات
    """

    code = "pagination_error"
    type: Optional[str]
    message: Optional[str] = None

    def __init__(self, message: Optional[str] = None, **kwargs) -> None:
        msg_template = message or "There is no {type} page."
        kwargs.update(msg_template=msg_template, message=message)
        super(PaginationError, self).__init__(**kwargs)


class RateLimitError(PydanticValueError):
    """
    خطأ عند تعدي حد الطلبات
    """

    code = "ratelimit_error"
    ratelimit_limit: int
    msg_template = "You have exceeded the Rate limit which was {ratelimit_limit}, it will renew after a second to {ratelimit_limit}"


class AuthorizationError(PydanticValueError):
    """
    خطأ التعرف على المتجر (التوكن غير صحيح)
    """

    code = "unauthorized"
    msg_template = "Please provide a valid authorization token"


class APIError(PydanticValueError):
    """
    API خطأ من ال
    """

    code = "api_error"
    msg_template: str
