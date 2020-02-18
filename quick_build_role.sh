#!/bin/bash
if [[ $# < 1 ]]; then
  cat <<HELP
Built ROLE on the development server

Usage: $0 <ROLE> [ansible-playbook options]

Examples:
  $0 eddbase
  $0 edd_master_controller -vv
HELP
  exit
fi

ROLE=$1
shift 

echo "Building role \"$ROLE\" ..."

export ANSIBLE_ROLES_PATH="$(pwd)/roles"
export ANSIBLE_RETRY_FILES_ENABLED="False"
ansible-playbook "$@" -i site.yml -e base_path=`pwd` --tags=build /dev/stdin <<END
---
- hosts: dev_server
  gather_facts: no
  tasks:
  - name: Print path variable
    debug:
      var: base_path
    tags: build

  roles:
    - $ROLE
END
