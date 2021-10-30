from typing import Any, List
from datetime import datetime
from salla import exceptions


def date_parser(cls, date: str) -> datetime:
    """datetime تحويل التاريخ من نص الى

    المتغيرات:
        date (str): التاريخ بشكل نص

    المخرجات:
        datetime: التاريخ بعد تحويله
    """
    if date:
        try:
            return datetime.strptime(
                date, "%Y-%m-%d %X" if len(date) > 12 else "%Y-%m-%d"
            )
        except:
            return date


def choice_validator(cls, value: Any, choices: List[Any]) -> Any:
    """التحقق من صحة النوع فديو ام صورة

    المتغيرات:
        value (Any): القيمة المراد التحقق منها

    الاخطاء:
        InvalidValueError: حطأ بعدم صحة قيمة النوع

    المخرجات:
        Any: القيمة بعد التاكد من صحته
    """
    if value not in choices:
        raise exceptions.InvalidValueError(wrong_value=value, choices=choices)
    return value
