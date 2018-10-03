# -*- coding: utf-8 -*-

"""EC2 Instance Manager
Handle the EC2 function of the SAPAWSCLI program
"""
import boto3
import time

from botocore.exceptions import ClientError


class Ec2Manager:
    """Manage the EC2 instance communications."""

    # TODO Lots of error handling.
    # Need to flush out custom exceptions and integrate with BOTO and SAP

    def __init__(self, session):

        self.session = session
        self.ec2 = self.session.resource('ec2')

    def get_instances(self, all_instances, sap_sid, sap_env):

        server_list = list(())

        try:

            instance_filters = []
            if sap_sid is not None:
                instance_filters.append({'Name': 'tag:SAP_SID', 'Values': [sap_sid]})

            if sap_env is not None:
                instance_filters.append({'Name': 'tag:SAP_ENV', 'Values': [sap_env]})

            if all_instances:
                instances = self.ec2.instances.all()
            else:
                instance_filters.append({'Name': 'tag-key', 'Values': ['SAP_SID']})
                instances = self.ec2.instances.filter(Filters=instance_filters)

            for instance in instances:

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

                # The block below will only run if instance is determined to be
                # an SAP system (via the SAP_SID tag being set) or if the all_instances
                # option was passed in from the CLI
                server = {
                    'InstanceId': instance.id,
                    'InstanceType': instance.instance_type,
                    'InstanceName': instance_name,
                    'AvailabilityZone': instance.placement['AvailabilityZone'],
                    'PrivateDnsName': instance.private_dns_name,
                    'PrivateIpAddress': instance.private_ip_address,
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

            return_list = {}
            return_list['Instances'] = server_list
            return return_list

        except ClientError as error:
            raise

    def get_instances_status(self, instance_id):
        """Returns the status of a specific instance."""
        return self.ec2.Instance(instance_id).state

    def start_instance(self, instance_id, start_wait):
        """Start the AWS Instance"""
        instance = self.ec2.Instance(instance_id)
        instance.start()
        if start_wait:
            instance.wait_until_running()

        return instance.state

    def stop_instance(self, instance_id, stop_wait):
        """Stop the AWS Instance"""

        # TODO: Clean up exception handling
        instance = {}

        try:

            instance = self.ec2.Instance(instance_id)

            # Only stop the instance if it is in the running state
            if instance.state['Code'] == 16:

                try:
                    instance.stop(DryRun=True)

                except ClientError as error:
                    if 'DryRunOperation' not in str(error):
                        raise

                try:
                    instance.stop()

                    # If the stop_wait option is used the command is synchronous
                    if stop_wait:
                        instance.wait_until_stopped()

                except ClientError as error:
                    print(error)

        except ClientError as error:
            return 'Error: ' + str(error)

        return instance.state

    def get_instance_details(self, instance_id):
        """Return the required basic Instance information for SAP functions."""

        try:
            instance = self.ec2.Instance(instance_id)

            sap_sid = None
            sap_sysnr = None
            details = {}

            for tag in instance.tags:
                if tag['Key'].upper() == 'SAP_SID':
                    sap_sid = tag['Value']
                elif tag['Key'].upper() == 'SAP_SYSNR':
                    sap_sysnr = tag['Value']

            if sap_sid:
                details = {
                            'Hostname': instance.private_dns_name,
                            'IpAddress': instance.private_ip_address,
                            'StateCode': instance.state['Code'],
                            'StateName': instance.state['Name'],
                            'SID': sap_sid,
                            'SysNr': sap_sysnr
                        }

            return details

        except ClientError as error:
            print(error)

