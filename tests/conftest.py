import importlib

import pytest

import database


@pytest.fixture
def app_module(monkeypatch, tmp_path):
    """Fresh app module bound to an isolated temporary SQLite file."""
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    module = importlib.import_module("app")
    module = importlib.reload(module)
    yield module


@pytest.fixture
def client(app_module):
    return app_module.app.test_client()
