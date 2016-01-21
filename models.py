from google.appengine.ext import ndb

class MarketInformation(ndb.Model):
    name_farmer = ndb.StringProperty()
    location_village = ndb.StringProperty()
    location_district = ndb.StringProperty()
    location_state = ndb.StringProperty()
    area = ndb.FloatProperty()
    number_of_dfls = ndb.IntegerProperty()
    actual_yield = ndb.FloatProperty()
    price_per_kg = ndb.FloatProperty()
    type_of_dfl = ndb.StringProperty()
    yield_per_100 = ndb.FloatProperty()
    total_amount = ndb.FloatProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)



