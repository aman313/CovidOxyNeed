from mongoengine import DynamicDocument, StringField, GeoPointField, DateTimeField, DateField


class CovidRequest(DynamicDocument):
    request_source = StringField(required=True)
    request_location_name = StringField()
    request_location_geo = GeoPointField()
    requested_resource_type = StringField()
    request_text = StringField()
    request_time = DateTimeField()
    request_url = StringField()
