from requests import get, post, delete, put

print('GET')
# print(get('http://localhost:5000/api/jobs').json())
# print(get('http://localhost:5000/api/jobs/2').json())
# print(get('http://localhost:5000/api/jobs/999').json())
# print(get('http://localhost:5000/api/jobs/asd').json())

print('POST')
# print(post('http://localhost:5000/api/jobs', json={}).json())
# print(post('http://localhost:5000/api/jobs', json={'job': 'Destroy enemy base'}).json())
# print(post('http://localhost:5000/api/jobs', json={
#     'team_leader': 3,
#     'job': 'Destroy enemy base',
#     'work_size': 10,
#     'collaborators': '2, 3',
#     'is_finished': 0,
# }).json())

# print('DELETE')
# print(delete('http://localhost:5000/api/jobs/3').json())
# print(delete('http://localhost:5000/api/jobs/999').json())
# print(delete('http://localhost:5000/api/jobs/asd').json())

print('PUT')
print(put('http://localhost:5000/api/jobs/asd', json={}).json())
print(put('http://localhost:5000/api/jobs/999', json={}).json())
print(put('http://localhost:5000/api/jobs/999',  json={
    'team_leader': 1,
    'job': 'test 2 put',
    'work_size': 10,
    'collaborators': '1, 2',
    'is_finished': 0,
}).json())
print(put('http://localhost:5000/api/jobs/5',  json={}).json())
print(put('http://localhost:5000/api/jobs/5',  json={'title': 'test put'}).json())
print(put('http://localhost:5000/api/jobs/5',  json={
    'team_leader': 1,
    'job': 'test 2 put',
    'work_size': 10,
    'collaborators': '1, 2',
    'is_finished': 0,
}).json())