import pytest
from unittest.mock import patch
from src.util.dao import DAO


@pytest.fixture
def dao_task():
    with patch("src.util.dao.getValidator", return_value={}):
        dao = DAO("task")

        try:
            dao.drop()
        except Exception:
            pass

        dao = DAO("task")

        yield dao

        try:
            dao.drop()
        except Exception:
            pass


def test_create_task_success_with_mocked_validator(dao_task):
    data = {
        "title": "Task 1",
        "description": "This is a task"
    }

    result = dao_task.create(data)

    assert result is not None
    assert result["title"] == "Task 1"
    assert result["description"] == "This is a task"
    assert "_id" in result


def test_create_task_without_real_validator_rules(dao_task):
    data = {
        "title": 123,
        "description": 456
    }

    result = dao_task.create(data)

    assert result is not None
    assert result["title"] == 123
    assert result["description"] == 456
    assert "_id" in result


def test_create_task_database_error(dao_task):
    data = {
        "title": "Task 3",
        "description": "This task should fail because of database error"
    }

    with patch.object(
        dao_task.collection,
        "insert_one",
        side_effect=Exception("Database error")
    ):
        with pytest.raises(Exception):
            dao_task.create(data)