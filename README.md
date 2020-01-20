EDD backend Control with ansible
================================

[Ansible](https://www.ansible.com/) is an IT automatization tool written in
python that requires only a SSH login on the host to control its configuration.
We use it here to manage the EDD backend. The [Ansible documentation](https://docs.ansible.com/ansible/latest/user_guide/intro_getting_started.html) is a good entry point to get familiar with the tool.


##  General Design Idea
The ansible terminology is derived from theater - roles are assigned and
a play is performed.

Within ansible terminology a **host** assumes one or more **roles**. Setting up
all roles is the **play** applied to all resources in the **inventory**.
Setting up a **role** consists of one or multiple **tasks**. For the EDD the
available services are e.g.
  - GatedSpectromeeter
  - VDIF Conversion
  - CiritcallySampledPFB
  - ...
are roles assigned to individual hosts.


## Inventories
All hosts + global variables for the site are collected in the
inventory file `site.yml` . You can ping
them via the command:
 `$ ansible -i site.yml -m ping all`
.


## Roles
Roles are defined in the directory `roles`, e.g `roles/gated_spectrometer`.
Here the tasks performed by a role are in `tasks/main.yml` that contains only
one task to start the according docker container. The build and start of EDD
docker container is abstracted out into a common role, so that only some
variables have to be defined. The Dockerfile to build the corresponding image
is stored in the templates.


## Play
Every configuration is a play. The `example_run.yml` assignees the role
gated_spectrometer to the first gpu node and executes test roles (a simple ping) on the next.
The play is executed by:

`$ansible-playbook -i site.yml example_run.yml`


## ToDo:
  - launch in scpi mode?
  - manage tags + launch different tags


## Cheat sheet
  - Basic setup of the edd backend. This configures:
    - a central docker registry and access of all nodes to it
    - a redis server
    - a master controller
    As the redis server is not available yet we have to override fact caching
    plugin here
    $ANSIBLE_CACHE_PLUGIN=memory ansible-playbook -i site.yml basic_configuration.yml

    build the edd base container and master controller
    $ansible-playbook -i site.yml basic_configuration.yml` --tags=build

  - Build containers for run (Rebuild all containers!):
    $ansible-playbook -i site.yml example_run.yml --tags build

  - Launch run:
    $ansible-playbook -i site.yml example_run.yml

  - Stop run:
    $ansible-playbook -i site.yml example_run.yml --tags stop

  - Quick built of specific role for developing purposes:
    $quick_build_role.sh edd_master_controller

