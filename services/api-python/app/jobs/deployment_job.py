from app.jobs.base import BaseJob

class DeploymentJob(BaseJob):
    def execute(self, job):
        print(f"Deploying service for job {job.id}")