import snowflake.connector


snowflake_config = {
    "user": " ",
    "password": " ",
    "account": " ",
    "warehouse": " ",
    "database": " ",
    "schema": " "
}


def get_snowflake_connection():
    return snowflake.connector.connect(**snowflake_config)


def execute_query(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()
