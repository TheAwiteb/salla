from threading import Thread
from typing import List, Any, Optional, Union
from datetime import datetime
from salla.types import Skus, Option, Value

date_format = "%Y-%m-%d %X"


def add_skus_to_option(skus: Skus, option: Option) -> Option:
    """الخاصة بالقيم التي بالاوبشن اليها لانها تكون افتراضسا منفصلة Skus اضافة تفاصيل ال

    المتغيرات:
        skus (Skus): الخاصة بالقيمSkus تفاصيل ال
        option (Option): الاختيار الموجود فيه القيم

    المخرجات:
        Option: الاختيار بعد التعديل
    """
    for value in option.values:
        value.skus = (
            None
            if not (
                skus_ := [skus_ for skus_ in skus if value.id in skus_.related_options]
            )
            else skus_[0]
        )
    return option


def values2dict(values: List[Value]) -> List:
    """تحويل القيم الى مصفوفة مكونة من قواميس

    المتغيرات:
        values (List[Value]): القيم

    المخرجات:
        List: مصفوفة تحتوي القيم بعد تحويلها الى قواميس
    """
    return [
        {
            "name": value.name,
            "price": value.price.amount,
            "display_value": value.display_value,
        }
        for value in values
    ]


def get_dict_of(keys: List, dct: dict) -> dict:
    """اخراج القيم الموجودة في القاموس ومعالجتها وارجاعها كقاموس

    المتغيرات:
        keys (List): القيم المراد اخراجها من القاموس
        dct (dict): القاموس المراد اخراج القيم منه

    المخرجات:
        dict: القيم بعد معالجتها
    """

    def dict_parser(value: Any) -> Any:
        """ارجاع المتغير بعد التعديل عليه او عدم التعديل اذ لم يلزم

        المتغيرات:
            value (Any): القيمة المراد التعديل عليها ان لزم

        المخرجات:
            Any: القيمة بعد التعديل عليها ان لزم
        """
        if type(value) is list:
            return [elm.get("id") for elm in value]
        elif type(value) is dict and "amount" in value:
            return value.get("amount")
        elif type(value) is datetime:
            return value.strftime(date_format)
        else:
            return value

    return {key: dict_parser(val) for key, val in dct.items() if key in keys}


def join_threads(threads: List[Union[Thread, List]]) -> None:
    """لجميع الثريدس حتى لو كانت داخل مصفوفةjoin عمل

    المتغيرات:
        threads (List[Union[Thread, List]]): مصفوفة تحتوي ثريد او مصفوفة تحتوي ثريد
    """
    for thread in threads:
        if thread:
            if type(thread) is list:
                join_threads(thread)
            else:
                thread.join()
