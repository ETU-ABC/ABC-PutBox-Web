from flask_marshmallow import Schema
from putbox import ma


class AlbumSchema(Schema):
    class Meta:
        fields = ('album_name', 'album_id', 'owner', 'photos')
    photos = ma.Nested('PhotoSchema', many=True, exclude=('album_id',))


album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)
