from app.database import test_db_connection as check_database_connection


def test_database_connection():
    result = check_database_connection()

    assert result["status"] == "connected"
    assert result["database"] == "WageWise"