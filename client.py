import requests

response = requests.post('http://127.0.0.1:8000/api/predictor/upload',
    files={
        'file': open('content/people.csv', 'rb')
    }
)

print("Status Code: ", response.status_code)
print("Response Text: ", response.text)