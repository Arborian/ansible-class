import os
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        name=dict(type="str", required=True),
        new=dict(type="bool", required=False, default=False),
    )
    result = dict(changed=False, original_message="", message="")
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    if module.check_mode:
        return module.exit_json(**result)
    result["original_message"] = module.params["name"]
    result["message"] = "goodbye"
    result["num_files"] = len(os.listdir(os.environ["HOME"]))
    if module.params["new"]:
        result["changed"] = True
    if module.params["name"] == "fail me":
        module.fail_json(msg="You requested this to fail", **result)
    module.exit_json(**result)


if __name__ == "__main__":
    run_module()
