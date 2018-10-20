# Generated by Django 2.1.2 on 2018-10-18 14:31

import datetime
from django.conf import settings
from django.db import migrations, models


def forwards_env_to_tag(apps, schema_editor):
    """
        Converts all EnvValue(s) to Tag(s)
    """
    Tag = apps.get_model('management', 'Tag')
    TestRun = apps.get_model('testruns', 'TestRun')
    TestRunTag = apps.get_model('testruns', 'TestRunTag')

    for test_run in TestRun.objects.all():
        for env_value in test_run.env_value.all():
            tag_name = "%s: %s" % (env_value.property.name, env_value.value)
            tag, _ = Tag.objects.get_or_create(name=tag_name)

            # do it like this b/c the above TestRun class is a __fake__
            # which doesn't have the add_tag() method
            TestRunTag.objects.get_or_create(run=test_run, tag=tag)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testruns', '0002_squashed'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalTestRun',
            fields=[
                ('run_id', models.IntegerField(blank=True, db_index=True)),
                ('start_date', models.DateTimeField(blank=True, db_index=True, editable=False)),
                ('stop_date', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('summary', models.TextField()),
                ('notes', models.TextField(blank=True)),
                ('estimated_time', models.DurationField(default=datetime.timedelta(0))),
                ('environment_id', models.IntegerField(default=0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.TextField(null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[
                 ('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('build', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                            on_delete=models.deletion.DO_NOTHING,
                                            related_name='+', to='management.Build')),
                ('default_tester', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                                     on_delete=models.deletion.DO_NOTHING,
                                                     related_name='+',
                                                     to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=models.deletion.SET_NULL,
                                                   related_name='+', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                              on_delete=models.deletion.DO_NOTHING,
                                              related_name='+', to=settings.AUTH_USER_MODEL)),
                ('plan', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                           on_delete=models.deletion.DO_NOTHING, related_name='+',
                                           to='testplans.TestPlan')),
                ('product_version', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                                      on_delete=models.deletion.DO_NOTHING,
                                                      related_name='+', to='management.Version')),
            ],
            options={
                'verbose_name': 'historical test run',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='auto_update_run_status',
        ),

        migrations.RunPython(forwards_env_to_tag),

        migrations.RemoveField(
            model_name='historicaltestcaserun',
            name='environment_id',
        ),
        migrations.RemoveField(
            model_name='historicaltestrun',
            name='environment_id',
        ),
        migrations.RemoveField(
            model_name='testcaserun',
            name='environment_id',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='environment_id',
        ),
        migrations.RemoveField(
            model_name='envrunvaluemap',
            name='run',
        ),
        migrations.RemoveField(
            model_name='envrunvaluemap',
            name='value',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='env_value',
        ),
        migrations.DeleteModel(
            name='EnvRunValueMap',
        ),
        migrations.RemoveField(
            model_name='historicaltestrun',
            name='estimated_time',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='estimated_time',
        ),
        migrations.RemoveField(
            model_name='testruntag',
            name='user',
        ),
    ]
