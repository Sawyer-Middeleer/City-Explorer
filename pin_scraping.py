"""
Do some mapping or scraping if I have time --- how many addresses per tax code?
"""
from bs4 import BeautifulSoup
import urllib

url = "https://datacatalog.cookcountyil.gov/api/geospatial/7832-c962?method=export&format=GeoJSON"
cc_spss_03 = gpd.read_file(url)
first5 = cc_spss_03.pin[0:5]
first5
geojson_url_dict = {'https://datacatalog.cookcountyil.gov/api/geospatial/qzpp-jhf6?method=export&format=GeoJSON': 'cc-plss-01',
                    'https://datacatalog.cookcountyil.gov/api/geospatial/4977-ijic?method=export&format=GeoJSON': 'cc-plss-02',
                    'https://datacatalog.cookcountyil.gov/api/geospatial/7832-c962?method=export&format=GeoJSON': 'cc-plss-03'}
cc_plss_list = []

for key in geojson_url_dict:
    geodf = gpd.read_file(key)
    cc_plss_list.append(geodf)


def get_tax_code(pins_list):
    """Scrapes the Cook County Assessor's website to grab the PIN's tax code"""
    pass


url = "https://datacatalog.cookcountyil.gov/api/geospatial/7832-c962?method=export&format=GeoJSON"
cc_spss_03 = gpd.read_file(url)
first5 = cc_spss_03.pin[0:5]
first5


chars_list = []
more_chars_list = []

for pin in first5:
    with urllib.request.urlopen('http://www.cookcountyassessor.com/Property.aspx?mode=details&pin='+pin) as url:
        html = url.read()
    bsObj = BeautifulSoup(html)
    table = bsObj.findAll('div', {'class':'characteristics'})
    tablex = bsObj.find_all('div', {'class':'row-fluid tablix'})
    for item in table:
        print(item)
        #print(item.get_text())

    # for item in tablex:
    #     print(item.get_text())
    #     row = [item.children for item in tablex]
    #     chars_list.append(row)
chars_list
pd.DataFrame(chars_list, columns=['pin', 'address', 'city', 'township', 'property classification', 'land square footage',
                                  'neighborhood', 'tax code'])


    tax_code_obj = bsObj.find(id="ctl00_phArticle_ctlPropertyDetails_lblPropInfoTaxcode")
    tax_code = tax_code_obj.get_text()
    chars_text = chars_obj.get_text()
    chars_also_text = chars_also_obj.get_text()
    tax_code_list.append(tax_code)
    chars_list.append(chars_text)
    chars_als_list.append(chars_also_text)
