#!/usr/bin/env bash

# Shell Opts
set -e -u -x

# Run the normal playbook process
pushd openstack-ansible > /dev/null

( ./scripts/run-playbooks.sh )

popd > /dev/null

# Extra options to pass to ansible command
ANSIBLE_PARAMETERS=${ANSIBLE_PARAMETERS:--e gather_facts=False}


# Run the fullstack service installation
pushd fullstack/playbooks > /dev/null
  openstack-ansible setup-fullstack.yml ${ANSIBLE_PARAMETERS}
popd > /dev/null
