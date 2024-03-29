# Generated by Django 4.1.5 on 2024-03-13 02:46

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthSMS',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('hp', models.CharField(max_length=11, primary_key=True, serialize=False, verbose_name='휴대폰번호')),
                ('auth', models.IntegerField(verbose_name='인증번호')),
            ],
            options={
                'db_table': 'AUTH_TB',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.CharField(max_length=17, unique=True, verbose_name='아이디')),
                ('password', models.CharField(max_length=255, verbose_name='비밀번호')),
                ('hp', models.CharField(max_length=11, null=True, unique=True, verbose_name='휴대폰번호')),
                ('auth', models.CharField(max_length=6, null=True, verbose_name='인증번호')),
                ('user_email', models.CharField(max_length=255, null=True, unique=True, verbose_name='이메일')),
                ('level', models.CharField(choices=[('2', 'Lv2_사용자'), ('1', 'Lv1_관리자'), ('0', 'Lv0_개발자')], default=2, max_length=18, verbose_name='등급')),
                ('date_joined', models.DateTimeField(auto_now_add=True, null=True, verbose_name='가입일')),
                ('card_user_id', models.CharField(max_length=20, unique=True, verbose_name='카드아이디')),
                ('card_user_pw', models.CharField(max_length=255, verbose_name='카드비밀번호')),
                ('bank_user_id', models.CharField(max_length=20, unique=True, verbose_name='뱅크아이디')),
                ('bank_user_pw', models.CharField(max_length=255, verbose_name='뱅크비밀번호')),
                ('agree_UserInfo', models.BooleanField(default=False, verbose_name='개인정보이용동의')),
                ('agree_Marketing', models.BooleanField(default=False, verbose_name='마케팅동의')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '모든 사용자',
                'verbose_name_plural': '모든 사용자',
                'db_table': 'finflow_user',
                'managed': True,
            },
        ),
    ]
