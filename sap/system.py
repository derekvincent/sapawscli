# -*- coding: utf-8 -*-

"""SAP System Instance Manager
Handle the SAP function of the SAPAWSCLI program
"""

from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from requests import exceptions

from zeep.transports import Transport


class SAPSystemManager:
    """SAP System instance manager."""
    def __init__(self, ec2_manager):
        self.ec2 = ec2_manager



    def get_sap_system_status(self, instance_id):
        """Gets the running status of the SAP system"""

        instance_details = self.ec2.get_instance_details(instance_id)

        if instance_details['StateCode'] is 16:
            # Will need to handle an tls switch and using port 5<NR>13 no tls or 5<NR>14 for tls connections.
            protocol = 'http'
            port = '5' + instance_details['SysNr'] + '13'
            sapctrl_url = protocol + '://' + instance_details['IpAddress'] + ':' + port + '/?wsdl'
            sapctrl_client = Client(sapctrl_url)

            try:
                sapctrl_status = sapctrl_client.service.GetSystemInstanceList()
            # TODO: Issue in the in-between state of when the instance is running and the SAP system is not running yet.

            except exceptions.ConnectionError as connection_error:
                return {'Status': 'Connection Error'}

            return sapctrl_status
        else:
            return {'Status': 'Instance is not in a running state'}


    def stop_sap_system(self, instance_id):
        """Stop and SAP Instance"""