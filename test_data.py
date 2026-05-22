from projects.models import Project
from users.models import User

users_data = [
    {
        'email': 'lev@yandex.ru',
        'name': 'Lev',
        'surname': 'K',
        'about': 'Python-разработчик',
        'password': 'password123',
    },
    {
        'email': 'sacha@gmail.com',
        'name': 'Sacha',
        'surname': 'B',
        'about': 'ML-инженер',
        'password': 'password123',
    },
    {
        'email': 'vitalik@mail.ru',
        'name': 'Vitalik',
        'surname': 'P',
        'about': 'UX/UI дизайнер',
        'password': 'password123',
    },
]

created_users = []
for ud in users_data:
    pwd = ud.pop('password')
    user, created = User.objects.get_or_create(email=ud['email'], defaults=ud)
    if created:
        user.set_password(pwd)
        user.save()
    created_users.append(user)

projects_data = [
    {
        'name': 'HLTV',
        'description': 'Сайт про Counter-Strike',
        'owner_idx': 0,
    },
    {
        'name': 'Genius',
        'description': 'Платформа для просмотра текстов песен',
        'owner_idx': 0,
    },
    {
        'name': 'Songless',
        'description': 'Сайт по угадыванию песен',
        'owner_idx': 1,
    },
    {
        'name': 'Twitch',
        'description': 'Стриминговая платформа',
        'owner_idx': 1,
    },
    {
        'name': 'Max',
        'description': 'Мессенджер для общения',
        'owner_idx': 2,
    },
]

for pd in projects_data:
    owner = created_users[pd.pop('owner_idx')]
    project, created = Project.objects.get_or_create(
        name=pd['name'],
        defaults={**pd, 'owner': owner, 'status': 'open'},
    )
    if created:
        project.participants.add(owner)

created_users[1].favorites.add(Project.objects.first())
print('Все пользователи и проекты созданы')
