# SAP AWS CLI
Command Line Interface to control SAP system running on AWS


## Basic Setup 

- The **awscli** should be install and the basic configuration shuold be doe with API key and secret id. Current we are just pulling the default profile but will allow for specifying the required profile in the future. 
- Python 3.7 needs to be install along with pipenv. When the code is pulled down pipenv needs to be run. 
- Currently to run the use the following: `pipenv run sapawscli`
- The tags currently supported are:
  - SAP_SID: Set this to the system SID 
  - SAP_SYSNR: Set this to the system number
  - SAP_TYPE: List of system types below and can be comma seperated. ie. `DB,ASCS,APP`
    - DB: Database system 
    - ASCS: ASCS system 
    - ENQ: Enqueue system 
    - APP: Application servers
    - HANADB: Stand alone HANA Database (no ABAP servers) 
    
## Features

### AWS Features
#### List Instances - list_instances
The `list instance` command return a list of all instances with the _SAP_SID_ value set. The option `--all-instances` returns all the instances types. 

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
     
## TODO

- [X] Get a list of currently avaliable AMI's
- [ ] Find a specific AMI based on a predetermined TAG system
- [ ] Check the status of a running AWS instance
- [ ] Start a specific AMI
- [ ] Stop a specific AMI
- [ ] Get a list of avaliable SAP's system based a predetermined TAG system
- [ ] Check the running status of an SAP ABAP instance
- [ ] Start a full SAP ABAP system
- [ ] Shutdown a full SAP ABAP system
- [ ] Start specific components of a ABAP system [DB, ENQU, ACSC, APP Servers]
- [ ] Stop specific components of a ABAP system [DB, ENQU, ACSC, APP Servers]
