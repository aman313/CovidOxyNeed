from mongoengine import Document, ObjectIdField, StringField


class Response(Document):
    original_request_id = ObjectIdField(required=True)
    original_resource_id = ObjectIdField(required=True)
    response_text = StringField(required=True)