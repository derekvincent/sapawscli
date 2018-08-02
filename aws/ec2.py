# -*- coding: utf-8 -*-

"""EC2 Instance Manager
Handle the EC2 function of the SAPAWSCLI program
"""
import boto3

class Ec2Manager:
    """Manage the EC2 instance communications."""

    def __init__(self, profile_name):
        self.session = boto3.Session(profile_name=profile_name)
        self.ec2 = self.session.resource('ec2')


    def get_instances(self, all_instances, sap_sid):

        server_list = list(())
        # TODO Get all instances, need to sort out the filter and SAP only...

        instances = self.ec2.instances.all()
        for instance in instances:

            is_sap = False
            instance_name = ""
            sap_sid = ""
            sap_sysnr = ""
            is_db_server = False
            is_ascs_server = False
            is_enq_server = False
            is_app_server = False
            is_hanadb = False

            for tag in instance.tags:
                if tag['Key'].upper() == 'SAP_SID':
                    sap_sid = tag['Value']
                    is_sap = True
                elif tag['Key'].upper() == 'SAP_SYSNR':
                    sap_sysnr = tag['Value']
                elif tag['Key'].upper() == 'SAP_TYPE':
                    system_types = tag['Value'].split(',')
                    for type in system_types:
                        if type.upper() == 'DB':
                            is_db_server = True
                        elif type.upper() == 'ASCS':
                            is_ascs_server = True
                        elif type.upper() == 'ENQ':
                            is_enq_server = True
                        elif type.upper() == 'APP':
                            is_app_server = True
                        elif type.upper() == 'HANADB':
                            is_hanadb = True
                elif tag['Key'].upper() == 'NAME':
                    instance_name = tag['Value']
                else:
                    is_sap = False

            # The block below will only run if instance is determined to be
            # an SAP system (via the SAP_SID tag being set) or if the all_instances
            # option was passed in from the CLI
            if is_sap or all_instances:
                server = {
                    'InstanceId': instance.id,
                    'InstanceType':  instance.instance_type,
                    'InstanceName': instance_name,
                    'AvailabilityZone': instance.placement['AvailabilityZone'],
                    'PrivateDnsName': instance.private_dns_name,
                    'PrivateIpAddress': instance.public_ip_address,
                    'StateCode': instance.state['Code'],
                    'StateName': instance.state['Name'],
                    'SID': sap_sid,
                    'SysNr': sap_sysnr,
                    'DatabaseServer': is_db_server,
                    'ASCSServer': is_ascs_server,
                    'EnqueueServer': is_enq_server,
                    'ApplicationServer': is_app_server,
                    "StandaloneHanaServer": is_hanadb
                }

                server_list.append(server)

        return server_list
