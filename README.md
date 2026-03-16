# MediRemind - Medicinpåminnare

Enkel medicinpåminnare byggd med GTK4/Adwaita i Python.

## Funktioner

- Lägg till och ta bort mediciner med namn och tid
- Påminnelser via desktop-notifikationer
- JSON-baserad datalagring
- Svenskt och engelskt gränssnitt (gettext)

## Systemkrav

- Python 3.10+
- GTK4
- libadwaita

### Installation av systempaket

**Ubuntu/Debian:**

```bash
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1
```

**Fedora:**

```bash
sudo dnf install python3-gobject gtk4 libadwaita
```

**Arch Linux:**

```bash
sudo pacman -S python-gobject gtk4 libadwaita
```

**macOS (Homebrew):**

```bash
brew install pygobject3 gtk4 libadwaita
```

## Installation

```bash
pip install .
```

## Användning

```bash
python3 -m mediremind
# eller efter installation:
mediremind
```

## Kompilera översättningar

```bash
msgfmt po/sv.po -o po/sv/LC_MESSAGES/mediremind.mo
```

## Datalagring

Mediciner sparas i `~/.local/share/mediremind/medications.json`.

**OBS:** Appen måste vara igång för att påminnelser ska fungera.

## Projektstruktur

```
MediRemind/
├── mediremind/
│   ├── __init__.py       # Paket, i18n-setup
│   ├── __main__.py       # Entry point
│   ├── application.py    # Adw.Application
│   ├── window.py         # Huvudfönster med medicinlista
│   ├── store.py          # JSON persistence
│   └── reminder.py       # Notifikationstimer
├── data/
│   └── se.mediremind.app.desktop
├── po/
│   ├── mediremind.pot    # Gettext-mall
│   └── sv.po             # Svensk översättning
├── tests/
│   └── test_store.py
├── setup.py
├── requirements.txt
└── README.md
```

## Licens

GPL-3.0
