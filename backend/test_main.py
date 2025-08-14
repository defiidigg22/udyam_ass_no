import requests
import random
import string

# The URL where your FastAPI server is running
BASE_URL = "http://127.0.0.1:8000"

def generate_random_aadhaar():
    """Generates a random 12-digit string for testing."""
    return ''.join(random.choices(string.digits, k=12))

def test_successful_submission():
    """
    Tests if a new, unique submission is successful (should return 200 OK).
    """
    # Create a unique aadhaar number for this test run
    unique_aadhaar = generate_random_aadhaar()

    # The data we want to send
    payload = {
        "aadhaar_number": unique_aadhaar,
        "owner_name": "Test User"
    }

    # Send the POST request to the /submit/ endpoint
    response = requests.post(f"{BASE_URL}/submit/", json=payload)

    # Assert that the status code is 200 (Success)
    assert response.status_code == 200

    # Assert that the returned data matches what we sent
    response_data = response.json()
    assert response_data["aadhaar_number"] == payload["aadhaar_number"]
    assert response_data["owner_name"] == payload["owner_name"]
    assert "id" in response_data # Check that an ID was assigned

def test_duplicate_submission():
    """
    Tests if submitting a duplicate aadhaar number fails (should return 400).
    """
    # Create a unique aadhaar number to use for this test
    unique_aadhaar = generate_random_aadhaar()

    payload = {
        "aadhaar_number": unique_aadhaar,
        "owner_name": "Duplicate Test"
    }

    # First submission: should be successful
    response1 = requests.post(f"{BASE_URL}/submit/", json=payload)
    assert response1.status_code == 200

    # Second submission (with the same data): should fail
    response2 = requests.post(f"{BASE_URL}/submit/", json=payload)

    # Assert that the status code is 400 (Bad Request)
    assert response2.status_code == 400

    # Assert that the error message is correct
    response_data = response2.json()
    assert response_data["detail"] == "This Aadhaar number has already been submitted."