from django.core.management.base import BaseCommand, CommandError

from apps.notifications.models import Notification
from apps.users.models import User

SAMPLE_PAYLOADS = [
    {'bid_title': 'Пшеница 3 класс', 'sender_first_name': 'Иван'},
    {'bid_title': 'Ячмень кормовой', 'sender_first_name': 'Алексей'},
    {'bid_title': 'Подсолнечник', 'sender_first_name': 'Дмитрий'},
    {'bid_title': 'Кукуруза', 'sender_first_name': 'Сергей'},
    {'bid_title': 'Соя', 'sender_first_name': 'Николай'},
    {'bid_title': 'Рапс озимый', 'sender_first_name': 'Андрей'},
    {'bid_title': 'Горох', 'sender_first_name': 'Михаил'},
    {'bid_title': 'Гречиха', 'sender_first_name': 'Владимир'},
    {'bid_title': 'Рожь', 'sender_first_name': 'Павел'},
    {'bid_title': 'Овёс', 'sender_first_name': 'Роман'},
]


class Command(BaseCommand):
    help = 'Создаёт 10 тестовых непрочитанных уведомлений для указанного пользователя'

    def add_arguments(self, parser):
        parser.add_argument('--phone', type=str, help='Номер телефона получателя')

    def handle(self, *args, **options):
        phone = options.get('phone')

        if phone:
            try:
                user = User.objects.get(phone_number=phone)
            except User.DoesNotExist:
                raise CommandError(f'Пользователь с номером {phone} не найден')
        else:
            user = User.objects.first()
            if not user:
                raise CommandError('В БД нет ни одного пользователя')
            self.stdout.write(f'--phone не указан, используется первый пользователь: {user.phone_number}')

        notifications = [
            Notification(
                recipient=user,
                type=Notification.TYPE_CONTACT_REQUEST_CREATED,
                payload=SAMPLE_PAYLOADS[i],
                is_read=False,
            )
            for i in range(10)
        ]
        Notification.objects.bulk_create(notifications)

        self.stdout.write(self.style.SUCCESS(
            f'Создано 10 уведомлений для пользователя {user.phone_number}'
        ))
