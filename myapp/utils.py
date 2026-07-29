from django.db import connection


def check_database_storage():

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT pg_size_pretty(
                pg_database_size(current_database())
            );
            """
        )

        size = cursor.fetchone()[0]


    return size