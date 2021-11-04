__all__ = "version", "version_info"

__version__ = "0.0.0"


def version_info() -> str:
    """اظهار تفاصيل الاصدار والعتاد الذي عليه

    المخرجات:
        str: تفاصيل الاصدار والعتاد الذي عليه
    """
    import platform
    import sys
    from pathlib import Path

    info = {
        "salla version": __version__,
        "install path": Path(__file__).resolve().parent,
        "python version": sys.version,
        "platform": platform.platform(),
    }
    return "\n".join(f"{key}:{val}" for key, val in info.items())
