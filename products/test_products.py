import importlib

from products.apps import ProductsConfig


def test_products_app_config_name():
    assert ProductsConfig.name == "products"


def test_products_modules_import():
    assert importlib.import_module("products.models") is not None
    assert importlib.import_module("products.views") is not None
