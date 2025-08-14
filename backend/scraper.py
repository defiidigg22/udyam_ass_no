import requests
from bs4 import BeautifulSoup
import json

URL = "https://udyamregistration.gov.in/UdyamRegistration.aspx"
form_fields = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(URL, headers=headers)
    response.raise_for_status() 
    soup = BeautifulSoup(response.content, "html.parser")

    # --- Field 1: Aadhaar Number ---
    aadhaar_input = soup.find('input', id='ctl00_ContentPlaceHolder1_txtadharno')
    if aadhaar_input:
        form_fields.append({
            'id': aadhaar_input.get('id'),
            'name': aadhaar_input.get('name'),
            'label': "1. Aadhaar Number/ आधार संख्या", 
            'placeholder': aadhaar_input.get('placeholder'), 
            'type': 'text',
            'validation': {
                'required': True,
                'maxLength': aadhaar_input.get('maxlength')
            }
        })

    # --- Field 2: Name as per Aadhaar ---
    name_input = soup.find('input', id='ctl00_ContentPlaceHolder1_txtownername')
    if name_input:
        form_fields.append({
            'id': name_input.get('id'),
            'name': name_input.get('name'),
            'label': "2. Name of Entrepreneur / उद्यमी का नाम",
            'placeholder': name_input.get('placeholder'),
            'type': 'text',
            'validation': {
                'required': True
            }
        })
    
    # Check if we found fields and save to JSON
    if form_fields:
        with open('form-schema.json', 'w') as f:
            json.dump(form_fields, f, indent=4)
        print("✅ Successfully created form-schema.json!")
    else:
        print("❌ Could not find any form fields. The website structure may have changed.")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")