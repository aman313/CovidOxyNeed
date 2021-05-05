from mongoengine import DynamicDocument, StringField, GeoPointField, DateTimeField, DateField


class CovidResource(DynamicDocument):
    resource_source = StringField(required=True)
    resource_location_name = StringField()
    resource_location_geo = GeoPointField()
    resource_type = StringField()
    resource_text = StringField()
    resource_time = DateTimeField()
    resource_url = StringField()
