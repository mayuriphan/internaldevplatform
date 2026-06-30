from app.jobs.base import BaseJob

class PaymentJob(BaseJob):
    def execute(self, job):
        print(f"Processing payment job {job.id}")