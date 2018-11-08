from flask_marshmallow import Schema
from putbox import ma


class TagSchema(Schema):
    class Meta:
        fields = ('photo_id', 'tag_desc')


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)


class PhotoSchema(Schema):
    class Meta:
        fields = ('photo_id', 'album_id', 'photo_path', 'upload_date', 'uploaded_by', 'tags')
    tags = ma.Nested('TagSchema', many=True, only=['tag_desc'])


photo_schema = PhotoSchema()
photos_schema = PhotoSchema(many=True)
