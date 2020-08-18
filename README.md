EDD backend Control with ansible
================================

[Ansible](https://www.ansible.com/) is an IT automatization tool written in
python that requires only a SSH login on the host to control its configuration.
We use it here to manage the EDD backend. The [Ansible
documentation](https://docs.ansible.com/ansible/latest/user_guide/intro_getting_started.html)
is a good entry point to get familiar with the tool.


## Ansible basics
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


### Inventories
All hosts + global variables for the individual sites are collected in the
corresponding inventory directory, e.g. effelsberg. You can e.g. ping all hosts
via the command:
 `$ ansible -i effelsberg -m ping all`
.


### Roles
Roles are defined in the directory `roles`, e.g `roles/gated_spectrometer`.
Here the tasks performed by a role are in `tasks/main.yml` that contains only
one task to start the according docker container. The build and start of EDD
docker container is abstracted out into a common role, so that only some
variables have to be defined. The Dockerfile to build the corresponding image
is stored in the templates.


### Play
Every configuration is a play. The `example_run.yml` assignees the role
gated_spectrometer to the first gpu node and executes test roles (a simple
ping) on the next.  The play is executed by:

`$ansible-playbook -i effelsberg example_run.yml`


## Ansible for EDD provisioning
### EDD Core
The core EDD consists of
  * a master controller,
  * a redis DB,
  * a docker registry,
	* a dhcp server,
  * a ansibleinterface container running on every node of the system used to
		grant ansible access to the node to the amster controller.

The basic_configuration.yml playbook will ensure the core system is up and
running. It will also ensure certain configurations on the bare metal systems,
e.g.
	* Installing the correct certificates for the docker registry
	* Installing the correct version of the nvidia driver

Use
`
$ANSIBLE_CACHE_PLUGIN=memory ansible-playbook -i effelsberg basic_configuration.yml
`
to execute the playbook, respectively **also** use
`
$ANSIBLE_CACHE_PLUGIN=memory ansible-playbook -i effelsberg basic_configuration.yml --tags=build
`
to build the containers. This is a force build to always pull latest changes
from the repositoreis. The basic configuration playbook will *create* the
registry certificate and ssh key-pairs for the docker registry, respectively
ansible_interface. **Old keys will be overwritten, so manually granted access
to components outside of the ansible system by copying e.g. the certificate
will be withdrawn.**


### EDD provisioning
To provison EDD based pipelines, a play needs to be loaded
`
$ansible-playbook -i effelsberg provision_descriptions/example_playbook.yml
`
Potentially, the required containers need **also** to be build before loading the play:
`
$ansible-playbook -i effelsberg provision_descriptions/example_playbook.yml --tags=build
`
To stop the containers launched use:
`
$ansible-playbook -i effelsberg example_run.yml --tags stop
``

The master controller may also provision the edd. The master controller
container thus pulls the edd_ansible repository and installs the site config
and roles.


## EDD Ansible structure
The repository is organied in the recommended playbook structure.

  - roles/ contains individual roles for EDD components, e.g.
    - roles/edd_master_controller
    - roles/gated_spectrometer
    - ...
  - roles/common contains common tasks to launch, stop, build the pipeline
    containers
  - roles/edd_base contains the tasks to build the eddbase container (usefull,
    but nor required) as base for pipeline containers. The role also launches
    the ansible interface on all nodes.


## Development hints
- Execute quick_build_role.sh  roles/myrole to quickly build  a single role
  without executing a playbook with --build tags which may build several
  roles.


## ToDo:
  - manage tags + launch different tags
