import psycopg2

from idp_common.config.settings import settings


class PostgresAdmin:

    def get_connection(self):

        return psycopg2.connect(

            host=settings.POSTGRES_HOST,

            port=settings.POSTGRES_PORT,

            user=settings.POSTGRES_USER,

            password=settings.POSTGRES_PASSWORD,

            database=settings.POSTGRES_ADMIN_DB,
        )


    def create_database(
        self,
        database_name: str,
    ):

        conn = self.get_connection()

        conn.autocommit = True

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM pg_database
            WHERE datname=%s
            """,
            (database_name,)
        )

        exists = cursor.fetchone()


        if not exists:

            cursor.execute(
                f'CREATE DATABASE "{database_name}"'
            )

            print(
                f"Created database {database_name}"
            )

        else:

            print(
                f"Database {database_name} already exists"
            )


        cursor.close()
        conn.close()


    def create_user(
        self,
        username: str,
        password: str,
        database_name: str,
    ):

        conn = self.get_connection()

        conn.autocommit = True

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT 1
            FROM pg_roles
            WHERE rolname=%s
            """,
            (username,)
        )


        exists = cursor.fetchone()


        if not exists:

            cursor.execute(
                f"""
                CREATE USER "{username}"
                WITH PASSWORD %s
                """,
                (password,)
            )

            print(
                f"Created user {username}"
            )


        cursor.execute(
            f"""
            GRANT ALL PRIVILEGES
            ON DATABASE "{database_name}"
            TO "{username}"
            """
        )


        cursor.close()
        conn.close()