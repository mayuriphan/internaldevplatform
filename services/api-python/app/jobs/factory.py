from app.jobs.payment_job import PaymentJob
from app.jobs.deployment_job import DeploymentJob

class JobFactory:

    @staticmethod
    def get(job_type: str):
        if job_type == "payment":
            return PaymentJob()
        if job_type == "deployment":
            return DeploymentJob()
        raise Exception("Unknown job type")