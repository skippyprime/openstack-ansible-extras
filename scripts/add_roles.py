#!/usr/bin/env python2.7
import sys
import os
import argparse
import collections

import yaml


OA_SUBMODULE = 'openstack-ansible'


def ensure_roles_format(roles):
    for role in roles:
        if not isinstance(role, collections.Mapping):
            raise ValueError(
                'Improper role format, expected a list of mappings')
        if 'name' not in role:
            raise ValueError(
                'Improper role format, expected role name')


def merge_roles(target, source, update):
    target_roles = None
    source_roles = None

    # load the target and source
    with open(target, mode='r') as instream:
        target_roles = yaml.safe_load(instream)
    with open(source, mode='r') as instream:
        source_roles = yaml.safe_load(instream)

    # sanity check
    ensure_roles_format(target_roles)
    ensure_roles_format(source_roles)

    # get the target role names
    target_role_names = [x['name'] for x in target_roles]

    # get source role names to add/update
    source_role_names = [x['name'] for x in source_roles
                         if update or x['name'] not in target_role_names]

    # remove target roles that will be aded/updated
    target_roles = [x for x in target_roles
                    if x['name'] not in source_role_names]

    for role in source_roles:
        if role['name'] in source_role_names:
            target_roles.append(role)

    with open(target, mode='w') as outstream:
        yaml.dump(target_roles, outstream, default_flow_style=False)


def build_parser():
    parser = argparse.ArgumentParser(
        description='Ensure additional roles '
                    'added for openstack-ansible bootstrap-ansible step')
    parser.add_argument('-f',
                        '--file',
                        dest='file',
                        required=False,
                        default=(OA_SUBMODULE +
                                 '/ansible-role-requirements.yml'),
                        help='openstack-ansible roles config file')
    parser.add_argument('-r',
                        '--roles',
                        dest='roles',
                        required=False,
                        default='extra-ansible-role-requirements.yml',
                        help='extra role dependencies')
    parser.add_argument('-u',
                        '--update',
                        dest='update',
                        required=False,
                        action='store_true',
                        default=False,
                        help='Update role information and versions')
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    has_invalid_args = False

    # sanity checks
    if not os.path.isfile(args.file):
        print('Target openstack-ansible roles file missing: {:s}'.format(
            args.file))
        has_invalid_args = True
    if not os.path.isfile(args.roles):
        print('Extra roles file missing: {:s}'.format(
            args.roles))
        has_invalid_args = True

    # stop on error
    if has_invalid_args:
        sys.exit(1)

    merge_roles(args.file, args.roles, args.update)

    print('Roles updated')


if __name__ == "__main__":
    main()
