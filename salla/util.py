from salla.types import Skus, Option


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
