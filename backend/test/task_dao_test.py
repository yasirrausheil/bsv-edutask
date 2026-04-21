import pytest
from datetime import datetime
from src.util.dao import DAO


@pytest.fixture
def dao_task():
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


def test_create_valid_task_required_fields_only(dao_task):
    data = {
        "title": "Task 1",
        "description": "This is a task"
    }

    result = dao_task.create(data)

    assert result is not None
    assert result["title"] == "Task 1"
    assert result["description"] == "This is a task"
    assert "_id" in result


def test_create_task_missing_title(dao_task):
    data = {
        "description": "This is a task"
    }

    with pytest.raises(Exception):
        dao_task.create(data)


def test_create_task_missing_description(dao_task):
    data = {
        "title": "Task without description"
    }

    with pytest.raises(Exception):
        dao_task.create(data)


def test_create_task_title_wrong_type(dao_task):
    data = {
        "title": 123,
        "description": "This is a task"
    }

    with pytest.raises(Exception):
        dao_task.create(data)


def test_create_task_description_wrong_type(dao_task):
    data = {
        "title": "Task 2",
        "description": 456
    }

    with pytest.raises(Exception):
        dao_task.create(data)


def test_create_task_categories_wrong_type(dao_task):
    data = {
        "title": "Task 3",
        "description": "This is a task",
        "categories": "school"
    }

    with pytest.raises(Exception):
        dao_task.create(data)


def test_create_valid_task_with_optional_fields(dao_task):
    data = {
        "title": "Task 4",
        "description": "Task with optional fields",
        "startdate": datetime(2026, 4, 20),
        "duedate": datetime(2026, 4, 30),
        "categories": ["school", "testing"]
    }

    result = dao_task.create(data)

    assert result is not None
    assert result["title"] == "Task 4"
    assert result["description"] == "Task with optional fields"
    assert "_id" in result