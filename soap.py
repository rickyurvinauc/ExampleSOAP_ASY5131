import zeep
import requests
import xml.etree.ElementTree as ET

def soap_request():
    # SOAP request URL
    url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"

    # structured XML
    payload = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
                <soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">
                    <soap:Body>
                        <CountryIntPhoneCode xmlns=\"http://www.oorsprong.org/websamples.countryinfo\">
                            <sCountryISOCode>CL</sCountryISOCode>
                        </CountryIntPhoneCode>
                    </soap:Body>
                </soap:Envelope>"""
    # headers
    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }
    # POST request
    response = requests.request("POST", url, headers=headers, data=payload)

    # prints the response
    print("xml response",response.text)
    print("status response", response)

    root = ET.fromstring(response.text)

    # Find the CountryIntPhoneCodeResult element
    country_code_result = root.find(".//{http://www.oorsprong.org/websamples.countryinfo}CountryIntPhoneCodeResult")

    # If the element was found, print its text
    if country_code_result is not None:
        print(country_code_result.text)
    else:
        print("CountryIntPhoneCodeResult not found in the response")


def soap_zeep():
    # set the WSDL URL
    wsdl_url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"

    # set method URL
    method_url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryIntPhoneCode"

    # set service URL
    service_url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"

    # create the header element
    header = zeep.xsd.Element(
        "Header",
        zeep.xsd.ComplexType(
            [
                zeep.xsd.Element(
                    "{http://www.w3.org/2005/08/addressing}Action", zeep.xsd.String()
                ),
                zeep.xsd.Element(
                    "{http://www.w3.org/2005/08/addressing}To", zeep.xsd.String()
                ),
            ]
        ),
    )
    # set the header value from header element
    header_value = header(Action=method_url, To=service_url)

    # initialize zeep client
    client = zeep.Client(wsdl=wsdl_url)

    # set country code for India
    country_code = "IN"

    # make the service call
    result = client.service.CountryIntPhoneCode(
        sCountryISOCode=country_code,
        _soapheaders=[header_value]
    )
    # print the result
    print(f"Phone Code for {country_code} is {result}")

    # set country code for United States
    country_code = "US"

    # make the service call
    result = client.service.CountryIntPhoneCode(
        sCountryISOCode=country_code,
        _soapheaders=[header_value]
    )

    # POST request
    response = client.service.CountryIntPhoneCode(
        sCountryISOCode=country_code,
        _soapheaders=[header_value]
    )

    # print the result
    print(f"Phone Code for {country_code} is {result}")
    print(response)

soap_request()
soap_zeep()