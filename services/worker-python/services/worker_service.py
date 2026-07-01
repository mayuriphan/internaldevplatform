class WorkerService:

    def __init__(self, worker):
        self.worker = worker

    def start(self):

        print("Worker service started")

        while True:
            self.worker.poll()