"""Internationalization setup using gettext."""

import os
import gettext
import locale

DOMAIN = "mediremind"


def get_locale_dir():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "po"
    )


def setup_i18n():
    try:
        locale.setlocale(locale.LC_ALL, "")
    except locale.Error:
        pass

    locale_dir = get_locale_dir()
    lang = gettext.translation(DOMAIN, locale_dir, fallback=True)
    lang.install()

    import builtins
    builtins._ = lang.gettext
