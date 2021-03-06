from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup

from address_services.base_address_service import BaseAddressService
import address_services.context as context

class SmartyAddressService(BaseAddressService):

    def __init__(self):
        pass

    @classmethod
    def get_api_keys(cls):
        smarty_info = context.get_context("SMARTY")

        auth_id = smarty_info["auth_id"]
        auth_token = smarty_info["auth_token"]

        return auth_id, auth_token

    @classmethod
    def get_credentials(cls):
        auth_id, auth_token = cls.get_api_keys()
        credentials = StaticCredentials(auth_id, auth_token)
        return credentials


    @classmethod
    def do_lookup(cls, address_dto):
        creds = cls.get_credentials()
        client = ClientBuilder(creds).with_licenses(["us-core-cloud"]).build_us_street_api_client()

        lookup = StreetLookup()

        lookup.street = address_dto.street
        lookup.city = address_dto.city
        lookup.state = address_dto.state
        lookup.zipcode = address_dto.zipcode

        client.send_lookup(lookup)

        try:
            client.send_lookup(lookup)
        except exceptions.SmartyException as err:
            print(err)
            cls.candidates = None
            return

        cls.candidates = lookup.result