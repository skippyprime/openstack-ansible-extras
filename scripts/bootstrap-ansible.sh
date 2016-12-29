#!/usr/bin/env bash

# Shell Opts
set -e -u -x

# Run the normal bootstrap ansible process
pushd openstack-ansible > /dev/null

( ./scripts/bootstrap-ansible.sh )

popd > /dev/null
