from fastapi.testclient import TestClient
import pytest

from vjemmieapi import app

client = TestClient(app)
