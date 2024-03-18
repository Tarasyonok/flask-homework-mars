from requests import get, post, delete

print('GET')
# print(get('http://localhost:5000/api/jobs').json())
# print(get('http://localhost:5000/api/jobs/2').json())
# print(get('http://localhost:5000/api/jobs/999').json())
# print(get('http://localhost:5000/api/jobs/asd').json())

print('POST')
# print(post('http://localhost:5000/api/jobs').json())
print(post('http://localhost:5000/api/jobs', json={}).json())
print(post('http://localhost:5000/api/jobs', json={'job': 'Destroy enemy base'}).json())
print(post('http://localhost:5000/api/jobs', json={
    'team_leader': 3,
    'job': 'Destroy enemy base',
    'work_size': 10,
    'collaborators': '2, 3',
    'is_finished': 0,
}).json())
