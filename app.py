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

from aws import ec2

@click.group()
def cli():
    """SAPAWSCLI: Control AWS based SAP systems"""
    pass


@cli.command('list_instances')
@click.option('--all-instances', is_flag=True, help='Displays all instances and not just SAP')
def list_instances(all_instances):
    """List EC2 instances."""
    instances_list = ec2.get_instances(all_instances)
    for instance in instances_list:
        print(instance)

@cli.command('start_instance')
def start_instance():
    pass

if __name__ == '__main__':
    cli()

