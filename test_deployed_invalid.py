import requests

print('Testing deployed backend with invalid GitHub ID...')
r = requests.post(
    'https://skillforge-wngd.onrender.com/api/analyze',
    json={
        'github_username': 'fakeuserxyz',
        'job_description': 'React Node.js Python Docker AWS Kubernetes'
    },
    timeout=10
)

print(f'Status: {r.status_code}')
data = r.json()

if r.status_code == 400:
    print(f'✓ Error (as expected): {data.get("error", "")}')
else:
    print(f'Match Score: {data.get("match_score")}%')
