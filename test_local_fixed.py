import requests

print('Testing local backend with invalid GitHub ID + resume...')
r = requests.post(
    'http://localhost:5000/api/analyze',
    json={
        'resume_text': 'I know React and Python',
        'github_username': 'fakeuserxyz',
        'job_description': 'React Node.js Python Docker AWS Kubernetes'
    },
    timeout=10
)

print(f'Status: {r.status_code}')
data = r.json()
print(f'Response: {data}')

if r.status_code == 400:
    print(f'\n✓ FIXED! Properly rejected: {data.get("error", "")}')
else:
    print(f'\nMatch Score: {data.get("match_score")}%')
