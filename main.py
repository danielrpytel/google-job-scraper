from google.bot import Bot
from database.MySQLDatabase import MySQLDatabase

bot = Bot()
db = MySQLDatabase()
db.connect_db()

processed_jobs = bot._get_all_jobs("Software Engineer")

for job_data in processed_jobs:

    if not db.check_job_exists_in_database(job_data['identifier']):
        db.insert_job(job_data)

db.exit_db()
