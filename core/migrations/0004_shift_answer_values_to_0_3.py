from django.db import migrations
from django.db.models import F


def shift_to_zero_based(apps, schema_editor):
    """
    Items 1-39 moved from a 1-4 scale to a 0-3 scale.

    Existing answers are shifted down by one so their scores are preserved.
    Item 40 stores a count and is not modified.
    """
    Answer = apps.get_model("core", "Answer")
    Answer.objects.filter(item_number__lt=40, value__gte=1).update(value=F("value") - 1)


def shift_to_one_based(apps, schema_editor):
    Answer = apps.get_model("core", "Answer")
    Answer.objects.filter(item_number__lt=40).update(value=F("value") + 1)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_answer_other_detail"),
    ]

    operations = [
        migrations.RunPython(shift_to_zero_based, shift_to_one_based),
    ]
