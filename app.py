#!/ysr/bin/python
# -*- coding: utf-8 -*-

"""SAPAWSCLI: Control AWS based SAP system form teh command line

SAP AWS CLI provides the ability to control AWS based SAP system
- Work with EC2 Instances
    - List EC2 instances
        - raw instances or via a tag structure
    - Start and Stop the instances
    - Check the current instance status
"""

import click
import boto3
import json

from aws.ec2 import Ec2Manager
from botocore.exceptions import ClientError

from sap.system import SAPSystemManager

"""Initializes global variables."""
session = None
ec2_manager = None
sap_manager = None

@click.group()
@click.option('--profile', default=None, help="Use a specific AWS profile")
def cli(profile):
    """SAPAWSCLI: Control AWS based SAP systems"""
    global session, ec2_manager, sap_manager

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(**session_cfg)
    ec2_manager = Ec2Manager(session)
    sap_manager = SAPSystemManager(ec2_manager)


@cli.command('list-instances')
@click.option('--all-instances', is_flag=True, help='Displays all instances and not just SAP')
@click.option('--sap-sid', default=None, help='Returns the systems associated with the SAP System ID')
@click.option('--sap-env', default=None, help='Returns the systems in the specified environment')
def list_instances(all_instances, sap_sid, sap_env):
    """List EC2 instances."""

    try:
        instances_list = ec2_manager.get_instances(all_instances, sap_sid, sap_env)
        click.echo(json.dumps(
            instances_list,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
            )
        )

    except ClientError as error:
        click.echo(error, err=True)

@cli.group('aws')
def aws():
    """AWS Based Commands"""

@aws.command('instance-status')
@click.argument('instance_id')
def instance_status(instance_id):
    """Returns the status of the specified instance."""
    print(ec2_manager.get_instances_status(instance_id))


@aws.command('start-instance')
@click.argument('instance_id')
def start_instance(instance_id):
    """Start the AWS Instance."""
    print(ec2_manager.start_instance(instance_id,True))


@aws.command('stop-instance')
@click.argument('instance_id')
def stop_instance(instance_id):
    """Stop the AWS Instance"""
    print(ec2_manager.stop_instance(instance_id, True))


@cli.group('sap')
def sap():
    """SAP based commands"""

@sap.command('instance-status')
@click.argument('instance_id')
def instance_status(instance_id):
    """Get the running status of an SAP system."""
    print(sap_manager.get_sap_system_status(instance_id))


@sap.command('stop-instance')
@click.argument('instance_id')
def stop_instance(instance_id):
    """Stop a running SAP system."""
    print(sap_manager.stop_system(instance_id))


@sap.command('start-instance')
@click.argument('instance_id')
def start_instance(instance_id):
    """Stop a running SAP system."""
    print(sap_manager.start_system(instance_id))


if __name__ == '__main__':
    cli()
