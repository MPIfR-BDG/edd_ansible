EDD backend Control with ansible
================================

[Ansible](https://www.ansible.com/) is an IT automatization tool written in
python that requires only a SSH login on the host to control its configuration.
We use it here to manage the EDD backend. The [Ansible documentation](https://docs.ansible.com/ansible/latest/user_guide/intro_getting_started.html) is a good entry point to get familiar with the tool.


##  General Design Idea
The ansible terminology is derived from theater - roles are assigned and
a play is performed.

Within ansible terminology a **host** assumes one or more **roles**. Setting up
all roles is the **play** applied to all ressources in the **inventory**.
Setting up a **role** consists of one or multiple **tasks**. For the EDD the
availbe services as e.g.
  - GatedSpectromeeter
  - VDIF Conversion
  - BeamFormer
  - ...
are roles assigned to individual hosts.


## Inventories
All hosts are collected in the
inventory file `site.yml` (_This may change in the future!_). You can ping
them via the command:
 `$ ansible -i all_nodes.yml -m ping all`
.


## Roles
Roles are defined in the directory `roles`, e.g `roles/gated_spectrometer`.
Here the tasks performed by a role are in `tasks/main.yml` that contains only
one task to start the according docker container. The build and start of EDD
docker container is abstracted out into a common role, so taht only some
variables have to be definied. The Dockerfile to build the corresponding image
is stored in teh templates.


## Play
Every configuration is a play. The `example_run.yml` assignes the role
gated_spectrometer to the first gpu node and executes test roles (a simpel ping) on the next.
The play is executed by:

`$ansible-playbook -i site.yml example_run.yml`


## ToDo:
- Recovery from desaster(s). The backend roles are currently shut down via the katcp
  command. We need a system to force shut down the backend via the ansible
  control
- Smarter dynamic inventories. Fine grained roles and host types in the future?
- However, can the dynamic inventory as it is cover all use cases as e.g.
  consider the network topology? Would't teh default here be a manual check of
  the oeprator, thus contradicting the dynamic setup? this would be potentially
  easier to just write a play for the specific observation run.


## Cheat sheet
  - Basic setup of the edd backend, including base container:
    $ansible-playbook -i site.yml basic_configuration.yml`

  - Build container for configuration:
    $ansible-playbook -i site.yml example_run.yml --tags build

  - Launch gated + pfb:
    $ansible-playbook -i site.yml example_run.yml

  - Stop gated + pfb:
    $ansible-playbook -i site.yml example_run.yml --tags stop

