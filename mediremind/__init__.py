"""MediRemind - Simple medication reminder."""

import gettext
import locale
from pathlib import Path

__version__ = "0.1.0"
__app_id__ = "se.mediremind.app"

# i18n setup
LOCALE_DIR = Path(__file__).parent.parent / "po"
if not (LOCALE_DIR / "sv" / "LC_MESSAGES" / "mediremind.mo").exists():
    LOCALE_DIR = Path("/usr/share/locale")

try:
    locale.setlocale(locale.LC_ALL, "")
except locale.Error:
    pass

gettext.bindtextdomain("mediremind", str(LOCALE_DIR))
gettext.textdomain("mediremind")
_ = gettext.gettext

import builtins
builtins._ = _
