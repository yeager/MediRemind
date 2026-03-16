"""Sound playback for reminders using GStreamer."""

import os

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

from mediremind.utils.paths import get_app_data_dir

_pipeline = None
_initialized = False


def _ensure_init():
    global _initialized
    if not _initialized:
        Gst.init(None)
        _initialized = True


def play_reminder():
    global _pipeline
    _ensure_init()
    stop_reminder()

    sound_dir = os.path.join(get_app_data_dir(), "sounds")
    for ext in ("wav", "ogg"):
        sound_path = os.path.join(sound_dir, f"reminder.{ext}")
        if os.path.exists(sound_path):
            break
    else:
        return

    _pipeline = Gst.parse_launch(
        f'filesrc location="{sound_path}" ! decodebin ! audioconvert ! autoaudiosink'
    )

    bus = _pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message::eos", _on_eos)

    _pipeline.set_state(Gst.State.PLAYING)


def _on_eos(bus, message):
    global _pipeline
    if _pipeline:
        _pipeline.set_state(Gst.State.NULL)
        _pipeline.set_state(Gst.State.PLAYING)


def stop_reminder():
    global _pipeline
    if _pipeline:
        _pipeline.set_state(Gst.State.NULL)
        _pipeline = None
