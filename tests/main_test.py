valid_data = {
    "filename": "wildflower/WFH_ALPHA_RegistrationDetail_SRC_20190430.zip",
    "source_ip": "10.11.12.13",
    "file_size": 1153434,
    "bucket_name": "bcbsnc-dna-dl-sandbox-landing-us-east-1",
    "event_name": "ObjectCreated:Put",
    "event_ts": "2021-01-11T10:34:11",
    "fp_id": 351,
}

invalid_data = {
    "filename": "wildflower/WFH_ALPHA_RegistrationDetail_SRC_20190430.zip",
    "source_ip": "10.11.12.13",
    "file_size": "1153434",
    "bucket_name": "bcbsnc-dna-dl-sandbox-landing-us-east-1",
    "event_name": "ObjectCreated:Put",
    "event_ts": "2021-01-11",
    "fp_id": 351,
}


def test_validData(test_app):
    response = test_app.post("/api/v1/fileregister/", json=valid_data)
    assert response.status_code == 201
    returnData = response.json()
    del returnData['id']['file_process_id']
    assert returnData == {
        "Status": "Success",
        "Message": "Inserted into DB",
        "id": {"step_id": 1},
    }



def test_validRecord(test_app):
    response = test_app.get("/api/v1/fileregister/files")
    returnData = response.json()
    del returnData[0]["create_ts"]
    assert response.status_code == 200
    assert returnData[0] == {
        "filename": "wildflower/WFH_alpha_RegistrationDetail_SRC_20190430.zip",
        "source_ip": "10.11.12.13",
        "file_size": 1153434,
        "bucket_name": "alpha-dna-dl-sandbox-landing-us-east-1",
        "event_name": "ObjectCreated:Put",
        "event_ts": "2021-01-11T10:34:11",
        "fp_id": 351,
        "create_by": "FileRegisterMS",
    }


def test_validStep(test_app):
    response = test_app.get("/api/v1/fileregister/steps")
    returnData = response.json()
    del returnData[0]["create_ts"]
    del returnData[0]["step_start_ts"]
    del returnData[0]["file_process_id"]
    del returnData[0]["step_end_ts"]
    assert response.status_code == 200
    assert returnData == {
        "step_name": "File Registration",
        "step_status": "DONE",
        "create_by": "FileRegisterMS",
    }

def test_repeatedData(test_app):
    response = test_app.post("/api/v1/fileregister/", json=valid_data)
    assert response.status_code == 201
    returnData = response.json()
    del returnData['id']['file_process_id']
    assert returnData == {
        "Status": "Failure",
        "Message": "File already exists",
        "id": {"step_id": 2},
    }

def test_invalidData(test_app):
    """
    Invalid event_ts format
    """
    response = test_app.post("/api/v1/fileregister/", json=invalid_data)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "event_ts"],
                "msg": "invalid datetime format",
                "type": "value_error.datetime",
            }
        ]
    }
