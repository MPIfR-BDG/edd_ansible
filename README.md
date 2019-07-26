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
To enable abstraction from physical hosts the inventory of all hosts is read
by the script `dyn_inventory.py` that removes currently not pingable hosts from
teh file. Within the play(book)s only generic host names as gpu_server[0]
should be used.



## Roles
Roles are difined in the directory `roles`, e.g `roles/gated_spectrometer`.
Here the tasks performed by a role are in `tasks/main.yml` that contains only
one task to start the according docker container.

## Play
Every configuration is a play. The `example_run.yml` assignes the role
gated_spectrometer to the first gpu node and executes test roles (a simpel ping) on the next.
The play is executed by:

`$ansible-playbook -i dyn_inventory.py example_run.yml`

## ToDo:
- Recovery from desaster(s). The backend roles are currently shut down via the katcp
  command. We need a system to force shut down the backend via the ansible
  control
- Smarter dynamic inventories. Fine grained roles and host types in the future?
- However, can the dynamic inventory as it is cover all use cases as e.g.
  consider the network topology? Would't teh default here be a manual check of
  the oeprator, thus contradicting the dynamic setup? this would be potentially
  easier to just write a play for the specific observation run.

## Ideas:
- There can be multiple dynamic inventoreis for different needs
