# Additional Information for Ansible Fundamentals

- Delegation and serialization
- Database Modules
- Network Automation
- Testing Ansible Roles

---

## Delegation and serialization

Sometimes we may want to run one (or more) tasks on a host that is *not* the targeted host.

For instance, a common need is to do the following three steps when deploying an app server:

- remove a host from the load balancer
- update the code on the host
- add the host to the load balancer

While you *can* run the 'add/remove from load balancer' code on the app server, it's often better to run those API calls from another "control" server.

---

`delegate_demo.yaml`

```yaml
- hosts: me
  become: true
  tasks:
    - name: Remove host from load balancer
      debug:
        msg: "This would probably be a custom module or the ec2_elb module"
      delegate_to: localhost
    - name: Deploy some code on all the nodes
      debug:
        msg: "Hey, I'm deploying code!"
    - name: Re-add host to load balancer
      debug:
        msg: "This would probably be a custom module or the ec2_elb module"
      delegate_to: localhost
```

---

In the special case of delegating to `localhost`, we can use the `local_action` task:

`delegate_demo2.yaml`

```yaml
- hosts: web
  become: true
  tasks:
    - name: Remove host from load balancer
      local_action:
        module: debug
        msg: "This would probably be a custom module or the ec2_elb module"
    - name: Deploy some code
      debug:
        msg: "Hey, I'm deploying code!"
    - name: Re-add host to load balancer
      local_action:
        module: debug
        msg: "This would probably be a custom module or the ec2_elb module"
```

---

## Serializing tasks

By default, Ansible will run tasks in parallel across all hosts targeted.

If you'd prefer some level of serialization, Ansible provides the `serial` key in plays. The value is the number of hosts to execute in parallel.

`serialize.yaml`

```yaml
- hosts: all
  serial: 4
  tasks:
    - name: Do something to each host, one at a time
      debug: "I am on host {{ansible_host}}"
```

---

```bash
rick@ansible:~/ansible-class$ ansible-playbook serialize.yaml

PLAY [all] ***********************************************************************************************************************

TASK [Do something to each host, four at a time] *********************************************************************************
ok: [rick-instance] => {
    "msg": "Hello world!"
}
ok: [Dmitri.Zaremba-instance] => {
    "msg": "Hello world!"
}
ok: [Anthony.Rounis-instance] => {
    "msg": "Hello world!"
}
ok: [Adam.Klein-instance] => {
    "msg": "Hello world!"
}

PLAY [all] ***********************************************************************************************************************

TASK [Do something to each host, four at a time] *********************************************************************************
ok: [Michael.Mickanen-instance] => {
    "msg": "Hello world!"
    ...
```

---

We can also give Ansible a list of values for `serial` to enable gradual rolling deployments:

`serialize2.yaml`

```yaml
- hosts: all
  gather_facts: off
  serial:
    - 1
    - 20%
    - 100%
  tasks:
    - name: Do something to each host, a few at a time
      debug: "I am on host {{ansible_host}}"
```

---

```bash
rick@ansible:~/ansible-class$ ansible-playbook serialize2.yaml

PLAY [all] ***********************************************************************************************************************

TASK [Do something to each host, a few at a time] ********************************************************************************
ok: [rick-instance] => {
    "msg": "Hello world!"
}

PLAY [all] ***********************************************************************************************************************

TASK [Do something to each host, a few at a time] ********************************************************************************
ok: [Dmitri.Zaremba-instance] => {
    "msg": "Hello world!"
}
ok: [Anthony.Rounis-instance] => {
    "msg": "Hello world!"
}

PLAY [all] ***********************************************************************************************************************
...
```

---

## Database Modules

Ansible includes support for configuring several popular databases:

- SQLServer (`mssql_db`)
- MySQL (`mysql_db`)
- Postgresql (`postgresql_eb`)

It also includes support for a few NoSQL databases:

- MongoDB (`mongodb_parameter`, `mongodb_user`)
- ElasticSearch (`elasticsearch_plugin`)
- Redis (`redis`)
- Riak (`riak`)

http://docs.ansible.com/ansible/latest/list_of_database_modules.html

---

## Network Automation

Ansible itself has a [nice tutorial on network automation][tutorial-network-automation]

Some things to consider:

- Many tasks will run on the Ansible controller node or be delegated, since network equipment does not always have Python available
- There may be protocols other than SSH used to invoke network modules. These are set with the `ansible_connection` variable:
    - `network_cli`: network CLI tools over the SSH protocol
    - `netconf`: XML tools over SSH
    - `httpapi`: network API using http/https
    - `local` is dependent on the particular module (not recommended any more)
- `become` can work different for networking equipment (`become_method: enable`)

[tutorial-network-automation]: https://docs.ansible.com/ansible/latest/network/index.html

---

## Testing Roles using Molecule

> [Molecule][molecule] is designed to aid in the development and testing of Ansible roles.

### Available Providers

- Docker (default)
- Vagrant
- OpenStack
- ... and many more

--

## Getting Started with Molecule

Molecule has a [getting started guide][molecule-gs] that we can go through together.

[molecule-gs]: https://molecule.readthedocs.io/en/stable/getting-started.html

[molecule]: https://molecule.readthedocs.io/en/stable/
