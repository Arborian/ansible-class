import os
from ansible.module_utils.basic import AnsibleModule

try:
    import SimpleHTTPServer # python2
    modname = 'SimpleHTTPServer'
except ImportError:
    import http.server
    modname = 'http.server'

TEMPLATE = '''
[program:{name}]
command=python -m {modname} {port}
directory={path}
'''

def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        path=dict(type='str', required=True),
        port=dict(type='int', required=True),
    )
    result = dict(
        changed=False,
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    if module.check_mode:
        return module.exit_json(**result)
    name = module.params['name']
    path = module.params['path']
    port = module.params['port']
    new_text = TEMPLATE.format(name=name, modname=modname, port=port, path=path)
    config_filename = '/etc/supervisor/conf.d/{}.conf'.format(name)
    if os.path.exists(config_filename):
        if open(config_filename).read() == new_text:
            module.exit_json(**result)
    with open(config_filename, 'w') as fp:
        fp.write(TEMPLATE.format(
            name=name,
            modname=modname,
            port=port,
            path=path))
        result['changed'] = True
    module.exit_json(**result)


if __name__ == '__main__':
    run_module()
