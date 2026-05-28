import importlib

from recipes.apps import RecipesConfig


def test_recipes_app_config_name():
    assert RecipesConfig.name == "recipes"


def test_recipes_modules_import():
    assert importlib.import_module("recipes.models") is not None
    assert importlib.import_module("recipes.views") is not None
