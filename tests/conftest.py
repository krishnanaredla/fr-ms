from fastapi import FastAPI
from fastapi.testclient import TestClient
import requests
import pytest
import os
from app.main import app


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:
        yield client
