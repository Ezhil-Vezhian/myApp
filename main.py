
import webapp2
from models import MarketInformation
import mockdata

from google.appengine.api import users
import os
import jinja2
import csv
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

marketResults = None





class MarketData:

    def __init__(self,name,location_village,location_district,location_state,area,no_of_dfls,type_of_dfl,actual_yield,price):
        self.name_farmer = name
        self.location_village = location_village
        self.location_district = location_district
        self.location_state = location_state
        self.area = area
        self.no_of_dfls = no_of_dfls
        self.type_of_dfl = type_of_dfl
        self.actual_yield = actual_yield
        self.price = price


    def yield_per_100_dfls(self):
        yield_per_100 = ((self.actual_yield * 1.0)/self.no_of_dfls) * 100.0
        return round(yield_per_100,3)

    def total_amount(self):
        return round(self.actual_yield * self.price,2)






class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect("/report")


    def post(self):
        _name = str(self.request.get('name_farmer'))
        _location_village = str(self.request.get('location_village'))
        _location_district = str(self.request.get('location_district'))
        _location_state = str(self.request.get('location_state'))
        _area = float(self.request.get('area'))
        _type_of_dfl = str(self.request.get('type_of_dfl'))
        _number_of_dfls = int(self.request.get('number_of_dfls'))
        _actual_yield = float(self.request.get('actual_yield'))
        _price_per_kg = float(self.request.get('price_per_kg'))

        marketData = MarketData(_name,_location_village,_location_district,_location_state,_area,_number_of_dfls,_type_of_dfl,_actual_yield,_price_per_kg)


        market_info = MarketInformation(name_farmer = _name,
                                        location_village = _location_village,
                                        location_district = _location_district,
                                        location_state = _location_state,
                                        area = _area,
                                        number_of_dfls = _number_of_dfls,
                                        actual_yield = _actual_yield,
                                        price_per_kg = _price_per_kg,
                                        type_of_dfl = _type_of_dfl,
                                        yield_per_100 = marketData.yield_per_100_dfls(),
                                        total_amount = marketData.total_amount())

        market_info.put()

        self.response.out.write("Success")




class ReportHandler(webapp2.RequestHandler):


    def write(self,msg):
        self.response.out.write(msg)


    def get(self):
        global  marketResults

        self.write(self.request.get('start_date'))
        self.write(self.request.get('end_date'))


        type_of_dfl = str(self.request.get("type_of_dfl"))

        if not(type_of_dfl == 'BV' or type_of_dfl == 'CB'):
            marketResults = MarketInformation.query().order(-MarketInformation.timestamp)

        else:
            marketResults = MarketInformation.query().order(-MarketInformation.timestamp)
            marketResults = marketResults.filter(MarketInformation.type_of_dfl == type_of_dfl)



        context = {
            'marketResults':marketResults
        }

        template = jinja_env.get_template("report.html")
        self.response.out.write(template.render(context))




class ReportCSVHandler(webapp2.RequestHandler):

    def get(self):


        fileName = str(self.request.get('fileName'))
        if not fileName:
            fileName = "report"

        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=%s.csv'%fileName
        writer = csv.writer(self.response.out)
        writer.writerow(["Farmer Name",
                         "Village",
                         "District",
                         'State',
                         'Area under Mulberry',
                         'Type of DFL',
                         'Number of DFLs',
                         'Actual Yield',
                         'Yield per 100 DFLs',
                         'Price per Kg',
                         'Total Amount'])

        for data in marketResults:
            writer.writerow([data.name_farmer,
                             data.location_village,
                             data.location_district,
                             data.location_state,
                             data.area,
                             data.type_of_dfl,
                             data.number_of_dfls,
                             data.actual_yield,
                             data.yield_per_100,
                             data.price_per_kg,
                             data.total_amount])


class MockDataHandler(webapp2.RequestHandler):

    def write(self,msg):
        self.response.out.write(msg)

    def get(self):
        for data in mockdata.mock_data:
            mock_marketData = MarketData(data[0],
                                         data[1],
                                         data[2],
                                         data[3],
                                         data[4],
                                         data[5],
                                         data[6],
                                         data[7],
                                         data[8]
                                         )

            market_info = MarketInformation(name_farmer = mock_marketData.name_farmer,
                                        location_village = mock_marketData.location_village,
                                        location_district = mock_marketData.location_district,
                                        location_state = mock_marketData.location_state,
                                        area = mock_marketData.area,
                                        number_of_dfls = mock_marketData.no_of_dfls,
                                        actual_yield = mock_marketData.actual_yield,
                                        price_per_kg = mock_marketData.actual_yield,
                                        type_of_dfl = mock_marketData.type_of_dfl,
                                        yield_per_100 = mock_marketData.yield_per_100_dfls(),
                                        total_amount = mock_marketData.total_amount())

            market_info.put()

        self.write("Done populating mock data")



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/report',ReportHandler),
    ('/reportCSV',ReportCSVHandler),
    ('/populateMockData',MockDataHandler)
], debug=True)
