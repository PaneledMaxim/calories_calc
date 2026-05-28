import importlib

from diary.apps import DiaryConfig


def test_diary_app_config_name():
    assert DiaryConfig.name == "diary"


def test_diary_modules_import():
    assert importlib.import_module("diary.models") is not None
    assert importlib.import_module("diary.views") is not None
