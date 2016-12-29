#!/usr/bin/env bash

# Shell Opts
set -e -u -x

# Extra options to pass to the AIO bootstrap process
export BOOTSTRAP_OPTS=${BOOTSTRAP_OPTS:-''}

# Run the normal bootstrap AIO process
pushd openstack-ansible > /dev/null

( ./scripts/bootstrap-aio.sh )

popd > /dev/null


# Run the fullstack AIO bootstrap playbook
pushd tests/aio > /dev/null
  if [ -z "${BOOTSTRAP_OPTS}" ]; then
    ansible-playbook bootstrap-aio-fullstack.yml \
                     -i ../../openstack-ansible/tests/test-inventory.ini
  else
    ansible-playbook bootstrap-aio-fullstack.yml \
                     -i ../../openstack-ansible/tests/test-inventory.ini \
                     -e "${BOOTSTRAP_OPTS}"
  fi
popd > /dev/null
