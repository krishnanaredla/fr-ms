from locust import HttpUser, task,between
import datetime
import random
import uuid


class LoadTesting(HttpUser):
    wait_time = between(1, 2)
    @task
    def fileregisterloadtest(self):
        data = {
            "source_ip": "kafka",
            "filename": "SRC{0}.zip".format(str(random.randint(10000,20000))),
            "file_size": random.randint(1,2000000),
            "bucket_name": "DISC",
            "event_ts": str(datetime.datetime.now()),
            "event_name": "stream",
            "fp_id": random.randint(1,200000)
        }
        self.client.post("api/v1/fileregister/", json=data)