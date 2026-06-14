import requests

print('Testing deployed backend with VALID GitHub user...')
r = requests.post(
    'https://skillforge-wngd.onrender.com/api/analyze',
    json={
        'resume_text': 'I know React and Python',
        'github_username': 'Jeffreyryan2005',
        'job_description': 'React Node.js Python Docker AWS'
    },
    timeout=15
)

print(f'Status: {r.status_code}')
data = r.json()
print(f'Response: {str(data)[:200]}...')
if r.status_code == 200:
    print(f'Match Score: {data.get("match_score")}%')
    print('✓ Deployed backend working')
elif r.status_code == 400:
    print(f'Error: {data.get("error")}')
