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
ansible-playbook "$@" -i site.yml --tags=build /dev/stdin <<END
---
- hosts: dev_server
  roles:
    - $ROLE
END
