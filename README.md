# ansible-mezzanine
Template for a full deployment pipeline (dev, staging, production ) of Mezzanine &amp; Django system using Ansible 

The Ansible playbook defined under "deploy" does the following:

- Provision nodes in Vagrant or AWS
    - Provisions nodes
    - Setups DNS (including hosts for local dev)
    - Provisions VPC and security groups
- Deploy and configure Mezzanine 
    - deploys all packages
    - configures nginx and gunicorn
    - Updates Mezzanine, local_settings.py and settings.py
    - Updates DB config to accept connections from web servers
- Deploy and configure Django
    - deploys all packages
    - Updates DB config to accept connections from web servers
    - configures nginx and gunicorn
- Deploy a Mezzanine project
    - deploys code from git repo locally or from remote, based on branch
- Deploy a Django API project
    - deploys code from git repo locally or from remote, based on branch
    
The primary focus of this project was to see how the same playbook(s) could be used for deploying to all environments 
in a deployment pipeline. One of the core principles in DevOps is that your mechanisms for deployment are automated and 
repeatable so that they can be tested continuous. To this end using the same mechanism, with minimal change to the 
mechanism, to deploy in development, in staging, in testing (CI) and ultimately into productions is essential to ensure
quality.

So here I have tried to use variables in Ansible to parameterize the playbooks based on environments. 
I have implemented 3 environments local-dev, staging and production. However others could be easily added such as 
testing or continuous integration container environments.

### Requirements

- ansible
- virtualenv
- vagrant
- git
- aws

### Parameters
For each environment definition is done in the '/deploy/pipeline/{{ environment }}', for example local using vagrant:

    ansible_ssh_user: vagrant
    remote_user: vagrant 
    #sudo_user: ubuntu
    local_sudo_user: root
    private_key_file: ~/.vagrant.d/insecure_private_key
      
    # Application Git repo variables
    # only enable git_repo or git_local_repo
    #
    git_repo_local: /project_repo
    git_branch: HEAD
    
    # provider info
    provider: vagrant
    
    vagrant_nodes:
      - name: db1
        groups:
          - dbservers
        ip: '192.168.3.20'
      - name: web1
        groups:
          - webservers
        ip: '192.168.3.10'
        http: 8080
        ssl: 8443
      - name: api1
        groups:
          - apiservers
        ip: '192.168.3.11'
        http: 7080
        ssl: 7443

This will result in three test nodes being provisioned in vagrant and then the Ansible playbooks for each group bing applied.
In the other examples for staging and production you will see definitions for AWS provisionings and be number of nodes to spinup.
In the secrets.yml in each pipeline you will need to put in your own secrets for each environment to provision and work:

        DB_password: dbpassword
        admin_password: some-password
        secret_key: verysecretkeypleasechange
        nevercache_key: anothersecretkeyyoushouldchange
        
        # Twitter Integration keys
        twitter_access_token_key: changetoyouraccounttoken
        twitter_access_token_secret: changetoyouraccountkey
        twitter_consumer_key: changetoyourconsumerkey
        twitter_consumer_secret: changetpyourconsumersecret
        
        # AWS keys
        
        ec2_access_key: "your key"
        ec2_secret_key: "your key"

In the production sercets.yml above the absolute minimum is to define you AWS access keys so that you can provision into AWS.


### Workflow
Following commands are executed from within the deploy directory and assume that you have Ansible installed and ideally
are working in a Virtualenv. All of the following commands have been made idempotent so the commands can be repeated without fear. 

#### Create an environment (Provision and Deploy)

    ansible-playbook -i stubinv site.yml --extra-vars='pipeline_env=local' --ask-sudo-pass
    
Now I do need to start off with an quirk here, the first time you spin up a vagrant environment the inventory is not 
going to exist so I placed a stub inventory into the project. This will only execute the provision portion.
On all subsequent executions the linked file 'local' will exists, which links to the generated inventory from the vagrant provision.
Hence the following command is used to execute the Provision and Deploy, even if you destroy your vagrant nodes:

    ansible-playbook -i local site.yml --extra-vars='pipeline_env=local' --ask-sudo-pass
    
The `--ask-sudo-pass`, will prompt for your local sudo password so that '/etc/hosts' can be updated with the node names.
    
For a staging environment:

    ansible-playbook -i library/ec2.py site.yml --extra-vars='pipeline_env=stage'
    
Here the dynamic inventory for AWS is used as stage is provisioned into there.

For a prod environment:

    ansible-playbook -i library/ec2.py site.yml --extra-vars='pipeline_env=prod'
    
Here the dynamic inventory for AWS is used as stage is provisioned into there.

> Would be good if Ansible could pickup which inventory from a YML or allow you to switch during executions. 
> Then defining two indicators of the same environment would not be necessary.  


#### Deploy updated code to an existing environment

Local vagrant development environment, deploy only the API:

    ansible-playbook -i local site.yml --extra-vars='pipeline_env=local' --tags api
    
Staging environment, deploy the Mezzanine application:

    ansible-playbook -i library/ec2.py site.yml --extra-vars='pipeline_env=stage' --tags app
    
    
    
# TODOs:

- integration with CI to spin-up Jenkins (slaves) for automated test runs.

    
