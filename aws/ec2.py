# -*- coding: utf-8 -*-

"""EC2 Instance Manager
Handle the EC2 function of the SAPAWSCLI program
"""
import boto3
import time

class Ec2Manager:
    """Manage the EC2 instance communications."""

    # TODO Lots of error handling.

    def __init__(self,session):

        self.session = session
        self.ec2 = self.session.resource('ec2')

    def get_instances(self, all_instances, sap_sid, sap_env):

        server_list = list(())

        # TODO Get all instances, need to sort out the filter and SAP only...

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
        """Start the AWS Instance"""
        instance = self.ec2.Instance(instance_id)
        instance.stop()
        if stop_wait:
            instance.wait_until_stopped()

        return instance.state
