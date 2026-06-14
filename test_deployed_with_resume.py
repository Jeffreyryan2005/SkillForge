import requests

print('Testing deployed backend with invalid GitHub ID + resume...')
r = requests.post(
    'https://skillforge-wngd.onrender.com/api/analyze',
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
    print(f'\n✓ Properly rejected: {data.get("error", "")}')
else:
    print(f'Match Score: {data.get("match_score")}%')
    if data.get("match_score") == 60:
        print('⚠️  Still returning dummy 60% score - need to redeploy')
