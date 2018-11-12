# SAP AWS CLI
Command Line Interface to control SAP system running on AWS


## Basic Setup 

- The **awscli** should be install and the basic configuration shuold be doe with API key and secret id. Current we are just pulling the default profile but will allow for specifying the required profile in the future. 
- Python 3.7 needs to be install along with pipenv. When the code is pulled down pipenv needs to be run. 
- Currently to run the use the following: `pipenv run app.py`
- The tags currently supported are:
  - SAP_SID: Set this to the system SID 
  - SAP_SYSNR: Set this to the system number
  - SAP_TYPE: List of system types below and can be comma seperated. ie. `DB,ASCS,APP`
    - DB: Database system 
    - ASCS: ASCS system 
    - ENQ: Enqueue system 
    - APP: Application servers
    - HANADB: Stand alone HANA Database (no ABAP servers) 
  - SAP_SYSTEM_TYPE: Type of application running, ABAP, JAVA, Web Dispatcher, HANA
  - SAP_ENV: Landscape or environment running in. Free text but should be used to group system into a environments such as sandboxes, development, QA, uat, production etc. 
    
## Features

### Common Features
#### List Instances - list_instances
The `list instance` command return a list of all instances with the _SAP_SID_ value set. The following option are available:

 - `--all-instances` returns all the instances types
 - `--sap-sid [SID]` filters results to instances with the provided SID in the SAP_SID tag
 - `--sap-env [ENV]` fiters results to instances with the provided ENV in the SAP_ENV tag
 

The current returned list is in a JSON format and provides the following values: 
- AWS Instance ID
- AWS Instance Type 
- AWS Instance Name (based on the standard name tag)
- AWS Availability Zone
- Private DNS Name 
- Private IP Address
- Run State Code  
- Run State Text 
- SAP SID
- SAP System Number 
- Database Server (Bool)
- ASCS Server (Bool)
- Enqueue Server (Bool)
- Application Server (Bool)
- Standalone Hana DB (Bool)

### AWS commands 
#### Instance Status - instance-status
The `instance-status` command currently provides a AWS json formatted instance state code made up of a Number and Text field. 

#### Start Instance - start-instance
The `start-instance` command takes the aws _instance id_ and issues a start to the instance. It waits for the instance to start before returning.

### Stop Instance - stop-instnace 
The `stop-instance` command takes the aws _instance id_ and issues a stop to the instance. It waits for the instance to stop before returning.

### SAP commands
#### Instance Status - instance-status
The `instance-status` command currently provides a SAP json formatted SAP instance state containing a list of:
- hostnames
- instance numbers
- http/s ports
- features (what services are running)
- run status     

#### Start Instance - start-instance
The `start-instance` command takes the aws _instance id_ and issues a start to the SAP instance. It waits for the instance to start before returning.

### Stop Instance - stop-instnace 
The `stop-instance` command takes the aws _instance id_ and issues a stop to the SAP instance. It waits for the instance to stop before returning.
      
## TODO

- [X] Get a list of currently avaliable AMI's
- [ ] Find a specific AMI based on a predetermined TAG system
  - [X] Default filter is the existence of the SAP_SID tag
  - [ ] Filter on SAP_SYSTEM_TYPE tag
  - [X] Filter on the SAP_ENV tag
- [X] Check the status of a running AWS instance
- [X] Start a specific AMI
- [X] Stop a specific AMI
- [ ] Get a list of available SAP's system based a predetermined TAG system
- [X] Check the running status of an SAP ABAP instance
- [ ] Start a full SAP ABAP system
- [ ] Shutdown a full SAP ABAP system
- [ ] Start specific components of a ABAP system [DB, ENQU, ACSC, APP Servers]
- [ ] Stop specific components of a ABAP system [DB, ENQU, ACSC, APP Servers]
- [ ] AMI Creation - shutdown, create ami, startup (optional)
- [ ] EBS Snapshot creation (full system with ignore) - shutdown, snapshot, startup (optional)
- [ ] AWS Instance Resize (up/down) - shutdown, snapshots (optional), resize EC2, startup