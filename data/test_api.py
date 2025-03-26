from requests import get, post, put, delete

BASE_URL = 'http://localhost:5000/api/v2'

print("===== ТЕСТИРОВАНИЕ API ПОЛЬЗОВАТЕЛЕЙ =====")

# 1. Получение всех пользователей
print("\n1. Получение всех пользователей:")
response = get(f'{BASE_URL}/users')
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

# 2. Создание нового пользователя
print("\n2. Создание нового пользователя:")
new_user_data = {
    'surname': 'Иванов',
    'name': 'Иван',
    'age': 30,
    'position': 'инженер',
    'speciality': 'строитель',
    'address': 'марс, база №1',
    'email': 'ivan@mars.org',
    'password': 'password123'
}
response = post(f'{BASE_URL}/users', json=new_user_data)
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

# Сохраним id созданного пользователя для последующих тестов
if response.status_code == 200:
    created_user_id = response.json()['id']
else:
    # Если создание не удалось, возьмем id = 1 для тестов
    created_user_id = 1

# 3. Получение информации о конкретном пользователе
print(f"\n3. Получение информации о пользователе с id={created_user_id}:")
response = get(f'{BASE_URL}/users/{created_user_id}')
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

# 4. Попытка создать пользователя с тем же email (должна вернуть ошибку)
print("\n4. Попытка создать пользователя с тем же email:")
duplicate_user_data = new_user_data.copy()
duplicate_user_data['surname'] = 'Петров'
duplicate_user_data['name'] = 'Петр'
response = post(f'{BASE_URL}/users', json=duplicate_user_data)
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

# 5. Создание пользователя с другим email
print("\n5. Создание пользователя с другим email:")
new_user_data2 = new_user_data.copy()
new_user_data2['email'] = 'petr@mars.org'
response = post(f'{BASE_URL}/users', json=new_user_data2)
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

# Сохраним id второго пользователя
if response.status_code == 200:
    second_user_id = response.json()['id']
else:
    second_user_id = 2

print(f"\n6. Удаление пользователя с id={second_user_id}:")
response = delete(f'{BASE_URL}/users/{second_user_id}')
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

print("\n7. Попытка получить несуществующего пользователя:")
response = get(f'{BASE_URL}/users/999')
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

print("\n8. Попытка удалить несуществующего пользователя:")
response = delete(f'{BASE_URL}/users/999')
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)


print("\n\n===== ТЕСТИРОВАНИЕ API РАБОТ =====")

print("\n1. Получение всех работ:")
response = get(f'{BASE_URL}/jobs')
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

print("\n2. Создание новой работы:")
new_job_data = {
    'team_leader': created_user_id,
    'job': 'Исследование кратера',
    'work_size': 15,
    'collaborators': '2, 3',
    'is_finished': False
}
response = post(f'{BASE_URL}/jobs', json=new_job_data)
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

if response.status_code == 200:
    created_job_id = response.json()['id']
else:
    created_job_id = 1

print(f"\n3. Получение информации о работе с id={created_job_id}:")
response = get(f'{BASE_URL}/jobs/{created_job_id}')
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

print(f"\n4. Изменение работы с id={created_job_id}:")
updated_job_data = {
    'team_leader': created_user_id,
    'job': 'Исследование кратера (обновлено)',
    'work_size': 20,
    'collaborators': '2, 3, 4',
    'is_finished': True
}
response = put(f'{BASE_URL}/jobs/{created_job_id}', json=updated_job_data)
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

print(f"\n5. Проверка изменений в работе с id={created_job_id}:")
response = get(f'{BASE_URL}/jobs/{created_job_id}')
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

print("\n6. Попытка изменить несуществующую работу:")
response = put(f'{BASE_URL}/jobs/999', json=updated_job_data)
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

print(f"\n7. Удаление работы с id={created_job_id}:")
response = delete(f'{BASE_URL}/jobs/{created_job_id}')
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

print(f"\n8. Проверка, что работа с id={created_job_id} удалена:")
response = get(f'{BASE_URL}/jobs/{created_job_id}')
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

print("\n9. Создание работы с некорректными данными (отсутствующие поля):")
incomplete_job_data = {
    'job': 'Неполные данные',
    'work_size': 5
}
response = post(f'{BASE_URL}/jobs', json=incomplete_job_data)
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

print("\n10. Создание работы с некорректными типами данных:")
invalid_job_data = {
    'team_leader': 'не число',
    'job': 'Некорректные типы',
    'work_size': 'не число',
    'collaborators': 5,  # должна быть строка
    'is_finished': 'не булево'
}
response = post(f'{BASE_URL}/jobs', json=invalid_job_data)
print(f"Статус код: {response.status_code}")
print(response.json())
print('-' * 50)

print("\nТестирование API завершено!")