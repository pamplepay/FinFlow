# Generated by Django 4.1.5 on 2024-03-20 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodefToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codef_token', models.CharField(max_length=1024, verbose_name='Codef Token')),
            ],
            options={
                'verbose_name': '카드정보',
                'verbose_name_plural': '카드정보',
                'db_table': 'FinFolw_Control_TB',
            },
        ),
    ]
