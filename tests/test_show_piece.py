"""
Use "nosetests -s" to display data
Not proper unit tests: no fixture data.
"""

# let django know where its settings are
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'symphony.settings'


def test_piece_serializer():
    from library import serializers as S
    po = S.Piece.objects.all()
    p = po[0]

    # model -> dict
    s = S.PieceSerializer(p)
    print s.data

    # dict -> new model
    s.data['id'] = 21347265 # so doesn't conflict with existing model
    z = S.PieceSerializer(data=s.data)
    print "Is it valid? {}".format(z.is_valid())

