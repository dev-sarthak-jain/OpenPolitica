# Generated by Django 4.0.1 on 2023-11-13 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('policycard', '0003_policycard_alter_comment_post_delete_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNeeds',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField()),
                ('context', models.CharField(max_length=255)),
                ('asc_pc_id', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UserNeeds',
            },
        ),
    ]