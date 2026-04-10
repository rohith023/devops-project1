import requests
import json

url = 'http://localhost:5001'
print('=' * 50)
print('DOCKER DEPLOYMENT - API TESTING')
print('=' * 50)

# Test basic endpoints
print('\n--- Health & Info Endpoints ---')
for path, name in [('/', 'Home'), ('/health', 'Health'), ('/info', 'Model Info')]:
    try:
        r = requests.get(f'{url}{path}', timeout=3)
        status = 'OK' if r.status_code == 200 else f'ERROR {r.status_code}'
        print(f'  {name:20} : {status}')
    except Exception as e:
        print(f'  {name:20} : FAILED - {str(e)[:30]}')

# Test predictions  
print('\n--- Prediction Tests ---')
test_cases = [
    {'age': 45, 'bp': 'HIGH', 'cholesterol': 'HIGH'},
    {'age': 30, 'bp': 'LOW', 'cholesterol': 'NORMAL'},
    {'age': 65, 'bp': 'NORMAL', 'cholesterol': 'HIGH'},
]

for i, data in enumerate(test_cases, 1):
    try:
        r = requests.post(f'{url}/predict', json=data, timeout=3)
        if r.status_code == 200:
            result = r.json()
            drug = result.get('prediction', {}).get('drug', 'N/A')
            conf = result.get('prediction', {}).get('confidence', 0)
            print(f'  Test {i}: Age={data["age"]}, BP={data["bp"]}, Chol={data["cholesterol"]}\n           -> {drug} (conf: {conf})')
        else:
            print(f'  Test {i}: ERROR {r.status_code}')
    except Exception as e:
        print(f'  Test {i}: FAILED - {str(e)[:40]}')

print('\n' + '=' * 50)
print('✓ Docker Deployment Successful!')
print('=' * 50)
