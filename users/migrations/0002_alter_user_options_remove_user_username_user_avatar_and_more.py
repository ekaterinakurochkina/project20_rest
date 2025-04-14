# Generated by Django 5.2 on 2025-04-13 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['email'], 'permissions': [('can_inactivate', 'Can inactivate')], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, help_text='Загрузите свой аватар', null=True, upload_to='users/avatars', verbose_name='Аватар'),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, help_text='Введите название города', max_length=50, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, help_text='Введите номер телефона', max_length=35, null=True, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Token'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='Укажите почту', max_length=254, unique=True, verbose_name='Email'),
        ),
    ]
