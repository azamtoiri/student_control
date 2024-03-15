from typing import cast, TypeVar, NewType, overload, Union, Callable, Optional

from decouple import config
from flet import colors

LOGO_PATH = '/Fox_Hub_logo.png'
SHEET = '#9FA2B4'
PRIMARY = colors.PRIMARY
BORDER_COLOR = colors.GREY
BG_COLOR = colors.WHITE

SHEET_BG_COLOR = colors.with_opacity(0.1, color=SHEET)


class Fonts:
    URLS = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "/fonts/OpenSans-Regular.ttf"
    }


T = TypeVar("T")
V = TypeVar("V")
Sentinel = NewType("Sentinel", object)
_MISSING = cast(Sentinel, object())


@overload
def _get_config(search_path: str, cast: None = None, default: Union[V, Sentinel] = _MISSING) -> Union[str, V]:
    ...


@overload
def _get_config(search_path: str, cast: Callable[[str], T], default: Union[V, Sentinel] = _MISSING) -> Union[T, V]:
    ...


def _get_config(
        search_path: str,
        cast: Optional[Callable[[str], object]] = None,
        default: object = _MISSING,
) -> object:
    """Wrapper around decouple.config that can handle typing better."""
    if cast is None:
        cast = lambda x: x

    if default is not _MISSING:
        obj = config(search_path, cast=cast, default=default)
    else:
        obj = config(search_path, cast=cast)

    return obj


class Settings:
    DEBUG = _get_config("DEBUG", bool, default=False)


class Connection:
    """Config connection to database"""

    DEV = _get_config("DEV", bool, False)
    if DEV:
        DATABASE_URL = _get_config("DATABASE_URL")  # postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}
    else:
        DATABASE_URL = _get_config("LOCAL_DB_URL")

    DATABASE_USERNAME = _get_config("DATABASE_USERNAME", str, "postgres")
    DATABASE_PASSWORD = _get_config("DATABASE_PASSWORD", str, "12345678")
    DATABASE_PORT = _get_config("DATABASE_PORT", str, "5432")
    DATABASE_HOSTNAME = _get_config("DATABASE_HOSTNAME", str, "postgres")
    DATABASE_NAME = _get_config("DATABASE_NAME", str, default="postgres")


class UserDefaults:
    """User default setting"""
    DEFAULT_USERNAME = _get_config("DEFAULT_USERNAME", str, "admin")
    DEFAULT_PASSWORD = _get_config("DEFAULT_PASSWORD", str, "admin")
