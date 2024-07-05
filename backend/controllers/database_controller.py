from services.database_service import query

def query_database(intent):
    result = query(intent)
    return result