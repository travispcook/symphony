"""
Check the new serializer field
"""

# let django know where its settings are
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'symphony.settings'

from nose import tools
from django.core.exceptions import ValidationError



def test_integer_choices_field():
    """docstring for test_integer_choices_field"""
    from library import serializers as S

    CHOICES = ((0, 'Apple'), (1, 'Berry'))

    z = S.IntegerChoicesField(choices=CHOICES)

    # check to_native [json] is sending a string
    tools.assert_equal(z.to_native(0), 'Apple')

    # check that from_native is returning the integer
    tools.assert_equal(z.from_native('Apple'), 0)

    # check validation errors
    tools.assert_raises(ValidationError, z.to_native, 'RandomString')

