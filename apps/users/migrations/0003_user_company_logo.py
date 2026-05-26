from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_phoneotp_id_alter_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos/'),
        ),
    ]
