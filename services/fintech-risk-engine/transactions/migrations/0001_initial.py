from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                (id, models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(db_index=True, max_length=128)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('currency', models.CharField(default='USD', max_length=8)),
                ('raw_payload', models.JSONField()),
                ('risk_score', models.FloatField()),
                ('risk_level', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=8)),
                ('reasons', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['risk_level', '-created_at'], name='transaction_risk_le_5bdfd8_idx')],
            },
        ),
    ]