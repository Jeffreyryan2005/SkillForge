import time
import requests

print('Waiting 20 more seconds for Render to redeploy...')
time.sleep(20)

print('Testing deployed backend now...')
try:
    r = requests.post(
        'https://skillforge-wngd.onrender.com/api/analyze',
        json={
            'resume_text': 'I know React',
            'github_username': 'fakeuser999fake',
            'job_description': 'React Python Docker'
        },
        timeout=15
    )

    print(f'Status: {r.status_code}')
    data = r.json()
    if r.status_code == 400:
        error_msg = data.get('error', '')
        print(f'✓ Error (fix deployed): {error_msg}')
    else:
        match = data.get('match_score')
        print(f'Match: {match}%')
        print(f'Note: If this is 25% instead of error, deployment still pending')
except Exception as e:
    print(f'Error: {str(e)[:100]}')
    print('Render server may still be starting...')
