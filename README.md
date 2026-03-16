# MediRemind - Medicinpåminnare

Medicinpåminnare med piktogram, ljud och bekräftelse. Designad för tillgänglighet med ARASAAC-kompatibla piktogram och stora, tydliga knappar.

## Funktioner

- **Dagligt schema** - Visar alla medicindoser för dagen med piktogram och tider
- **Påminnelser** - Ljud- och systemnotiser när det är dags för medicin
- **Bekräftelse** - Stora knappar för att bekräfta tagen dos
- **Anhörigvarning** - E-post/SMS till anhörig vid missad dos
- **Historik** - Logg över tagna och missade doser
- **Piktogram** - ARASAAC-stöd och inbyggda fallback-ikoner
- **Tillgänglighet** - ARASAAC-kompatibel design för kognitiva funktionshinder
- **Internationalisering** - Svenska som huvudspråk, stöd för engelska

## Systemkrav

- Python 3.10+
- GTK4
- libadwaita
- GStreamer 1.0

### Installation av systempaket

**Ubuntu/Debian:**

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 \
    gir1.2-gst-plugins-base-1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good
```

**Fedora:**

```bash
sudo dnf install python3-gobject gtk4 libadwaita gstreamer1-plugins-base gstreamer1-plugins-good
```

**Arch Linux:**

```bash
sudo pacman -S python-gobject gtk4 libadwaita gstreamer gst-plugins-base gst-plugins-good
```

**macOS (Homebrew):**

```bash
brew install pygobject3 gtk4 libadwaita gstreamer gst-plugins-base gst-plugins-good
```

## Installation

```bash
git clone https://github.com/yeager/MediRemind.git
cd MediRemind
pip install -r requirements.txt
# eller:
pip install .
```

## Användning

```bash
python3 -m mediremind
# eller efter installation:
mediremind
```

## Konfiguration

Vid första start skapas exempeldata med tre mediciner. Gå till **Inställningar** för att:

1. Lägg till/ta bort mediciner med namn, typ och doseringsschema
2. Konfigurera anhörigkontakt med e-post och telefonnummer
3. Ställ in SMTP för e-postnotifieringar
4. Justera påminnelsetider och ljudinställningar

### Datalagring

All data lagras som JSON under `~/.local/share/mediremind/`:
- `schedule.json` - Mediciner och doseringsscheman
- `history.json` - Bekräftelsehistorik
- `settings.json` - Inställningar och kontaktinfo

## Kompilera översättningar

```bash
mkdir -p po/sv/LC_MESSAGES
msgfmt po/sv.po -o po/sv/LC_MESSAGES/mediremind.mo
```

## Projektstruktur

```
MediRemind/
├── mediremind/
│   ├── __init__.py          # Paket, i18n-setup
│   ├── __main__.py          # Entry point
│   ├── application.py       # Adw.Application med CSS och tjänster
│   ├── window.py            # Huvudfönster med ViewStack
│   ├── models/              # Datamodeller (Medication, DoseSchedule, HistoryEntry)
│   ├── services/            # Tjänster (persistence, scheduler, notification, alert, pictogram)
│   ├── views/               # UI-vyer (schema, historik, inställningar, påminnelse)
│   └── widgets/             # Anpassade widgets (MedCard, ConfirmButton, PictogramImage)
├── data/
│   ├── icons/fallback/      # SVG fallback-ikoner för medicintyper
│   ├── sounds/              # Påminnelseljud
│   └── se.mediremind.app.desktop
├── po/
│   ├── mediremind.pot       # Gettext-mall
│   ├── sv.po                # Svensk översättning
│   └── POTFILES.in
├── tests/                   # Enhetstester
├── setup.py
├── requirements.txt
└── README.md
```

## Licens

GPL-3.0
