import mysql.connector
import os
from dotenv import load_dotenv


class MySQLDatabase:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_DATABASE")
        self.conn = None
        self.cursor = None

    def connect_db(self):
        try:
            print(self.user)
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor()
            print(f"Connected to the database: {self.database}")
        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            print("Querry executed")
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error executing the query: {err}")
            return None

    def insert_job(self, job_data):

        query = "INSERT INTO google_scraped_jobs (title, company_name, location, description, posting_url, identifier)" \
            "VALUES (%s, %s, %s, %s, %s, %s)"

        values = (job_data['title'], job_data['company_name'],
                  job_data['location'], job_data['description'], job_data['posting_url'], job_data['identifier'])

        try:

            self.cursor.execute(query, values)
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print("Job data inserted successfully.")
            else:
                print("Job data insertion failed")
        except mysql.connector.Error as err:
            print(f"Error during job data insertion: {err}")

    def check_job_exists_in_database(self, identifier):
        db = MySQLDatabase()
        db.connect_db()

        query = f"SELECT identifier FROM google_scraped_jobs WHERE identifier = %s"
        result = db.execute_query(query, (identifier,))
        db.exit_db()
        return result is not None and len(result) > 0

    def exit_db(self):
        if self.conn is not None and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Database connection closed")
