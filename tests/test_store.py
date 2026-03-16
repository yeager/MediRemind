"""Tests for medication store."""

import json
from unittest import mock

from mediremind import store


def test_validate_empty_name():
    assert store.validate("", "08:00") is not None


def test_validate_bad_time():
    assert store.validate("Aspirin", "25:00") is not None
    assert store.validate("Aspirin", "abc") is not None
    assert store.validate("Aspirin", "8:00") is not None


def test_validate_ok():
    assert store.validate("Aspirin", "08:00") is None
    assert store.validate("Vitamin D", "23:59") is None


def test_load_missing_file(tmp_path):
    with mock.patch.object(store, "DATA_FILE", tmp_path / "missing.json"):
        assert store.load() == []


def test_save_and_load(tmp_path):
    data_file = tmp_path / "medications.json"
    meds = [{"name": "Aspirin", "time": "08:00"}]
    with mock.patch.object(store, "DATA_DIR", tmp_path), \
         mock.patch.object(store, "DATA_FILE", data_file):
        store.save(meds)
        assert store.load() == meds


def test_load_corrupt_json(tmp_path):
    data_file = tmp_path / "medications.json"
    data_file.write_text("not json")
    with mock.patch.object(store, "DATA_FILE", data_file):
        assert store.load() == []
