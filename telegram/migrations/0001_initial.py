# Generated by Django 4.0 on 2022-03-17 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delete_Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_at', models.DateTimeField(auto_now_add=True)),
                ('deleter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deleter', to='auth.user')),
                ('other', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Chat_Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('unread', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='auth.user')),
                ('transmitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transmitter', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Active_Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latest_activate', models.DateTimeField()),
                ('Rx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Rx', to='auth.user')),
                ('Tx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Tx', to='auth.user')),
            ],
        ),
    ]
