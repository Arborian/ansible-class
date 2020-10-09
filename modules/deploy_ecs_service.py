#!/usr/bin/python
import base64

import boto3
from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: my_sample_module

short_description: This is my sample module

version_added: "2.4"

description:
    - "This is my longer description explaining my sample module"

options:
    name:
        description:
            - This is the message to send to the sample module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

extends_documentation_fragment:
    - azure

author:
    - Your Name (@yourhandle)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_new_test_module:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_new_test_module:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_new_test_module:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
    returned: always
message:
    description: The output message that the sample module generates
    type: str
    returned: always
'''


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        profile=dict(type='str', required=False, default=None),
        service=dict(type='str', required=True),
        cluster=dict(type='str', default='default'),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    session = boto3.Session(profile_name=module.params['profile'])
    ecs = session.client('ecs')
    kwargs = {}
    try:
        resp = ecs.update_service(
            service=module.params['service'],
            cluster=module.params['cluster'],
            forceNewDeployment=True
        )
    except Exception as err:
        module.fail_json(msg=f'Error updating service: {err!r}')
    result.update(resp=resp, changed=True)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
