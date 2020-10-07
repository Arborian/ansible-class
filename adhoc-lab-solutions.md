## Lab: Variables and patterns

- Add a custom variable for the `Role_app` group and view it using the `debug`
  command (`ansible Role_app -m debug -a var=VARNAME`)

Update the inventory.yaml file to include the following contents:

```yaml
...
Role_app:
    vars:
        name: app-server
        my_new_variable_name: my-new-variable-value
...
```

- Target all the servers using `ansible all` and view the value of your new variable (`ansible all -m debug -a var=VARNAME`)

```bash
$ ansible all -m debug -a var=my-new-variable-value
ansible | SUCCESS => {
    "my_new_variable_name": "VARIABLE IS NOT DEFINED!"
}
...
web-1 | SUCCESS => {
    "my_new_variable_name": "VARIABLE IS NOT DEFINED!"
}
app-0 | SUCCESS => {
    "my_new_variable_name": "my-new-variable-value"
}
hhannani | SUCCESS => {
    "my_new_variable_name": "VARIABLE IS NOT DEFINED!"
}
db-1 | SUCCESS => {
    "my_new_variable_name": "VARIABLE IS NOT DEFINED!"
}
app-1 | SUCCESS => {
    "my_new_variable_name": "my-new-variable-value"
}
kishore | SUCCESS => {
    "my_new_variable_name": "VARIABLE IS NOT DEFINED!"
}
...
```

## Lab: more variables

- Create a `host_vars` directory with a file web-0.yaml in it.
  - Set some variables in the web-0.yaml file and verify that they appear
    with `ansible web-0 -m debug...`
- Create a `group_vars` directory with a subdirectory `all`
  - Create a few files inside `group_vars/all` and verify that the variables
    are applied
    to all hosts using `ansible all -m debug ...`

**For the file changes above, see the file
src/data/ansible-examples/host_group_vars.zip**

To test:

```bash
$ ansible web-0 -m debug -a var=var0
web-0 | SUCCESS => {
    "var0": [
        1,
        2,
        3
    ]
}
$ ansible web-0 -m debug -a var=allvar1
web-0 | SUCCESS => {
    "allvar1": "bar"
}
```

## Lab: Ad-hoc Commands

Using Ansible one-off commands:

- Create a user for yourself on "your" server
- Verify that you can ssh to your new account
- Check out the class repository to your user's account (https://github.com/Arborian/ansible-class.git)
- Install and start nginx in your host
- Verify that it is working by visiting your server with a web browser

### Solution

(Assuming your username is gertrude and your server is the
salesforce.training.arborian.com server)

Create user:

```bash
$ ansible --become salesforce -m user -a 'name=gertrude shell=/usr/bin/bash'
salesforce | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": true,
    "comment": "",
    "create_home": true,
    "group": 1004,
    "home": "/home/gertrude",
    "name": "gertrude",
    "shell": "/usr/bin/bash",
    "state": "present",
    "system": false,
    "uid": 1004
}
```

Authorize public key:

```bash
$ ansible --become salesforce -m authorized_key -a 'user=gertrude key={{lookup("file", "../class-keypair-public")}}'
salesforce | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },

...
    "user": "gertrude",
    "validate_certs": true
}
```

Verify ssh access:

```bash
$ ssh -i ../class-keypair.pem gertrude@salesforce.training.arborian.com
Warning: untrusted X11 forwarding setup failed: xauth key data not generated
[gertrude@ip-172-30-1-193 ~]$ exit
logout
Connection to salesforce.training.arborian.com closed.

```

Checkout git repo:

```bash
$ ansible salesforce -m git --become --become-user gertrude -a 'name=https://github.com/Arborian/ansible-class.git dest=~/ansible-class'
[WARNING]: Module remote_tmp /home/gertrude/.ansible/tmp did not exist and was
created with a mode
of 0700, this may cause issues when running as another user. To avoid this,
create the remote_tmp
dir with the correct permissions manually
salesforce | CHANGED => {
    "after": "566fee5ee9173c36595947e7fca667dc4a7025d9",
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "before": null,
    "changed": true
}

```

Install nginx (requires instsall of epel-release first):

```bash
$ ansible salesforce --become -m yum -a 'name=epel-release'salesforce | CHANGED
=> {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": true,
    "changes": {
        "installed": [
            "epel-release"
        ]
    },
    "msg": "",
    "rc": 0,
    "results": [
        "Loaded plugins: fastestmirror\nLoading mirror speeds from cached
hostfile\n * base: d36uatko69830t.cloudfront.net\n * extras:
...
\n\nComplete!\n"
    ]
}
```

```bash
$ ansible salesforce --become -m yum -a 'name=nginx'
salesforce | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": true,
    "changes": {
        "installed": [
            "nginx"
        ]
    },
    "msg": "warning:
/var/cache/yum/x86_64/7/epel/packages/nginx-1.16.1-1.el7.x86_64.rpm: Header V3
...
\n  nginx-mod-http-perl.x86_64 1:1.16.1-1.el7
\n  nginx-mod-http-xslt-filter.x86_64 1:1.16.1-1.el7
\n  nginx-mod-mail.x86_64 1:1.16.1-1.el7          \n  nginx-mod-stream.x86_64
1:1.16.1-1.el7                                        \n\nComplete!\n"
    ]
}
```

Start nginx service

```bash
$ ansible salesforce --become -m service -a 'name=nginx state=started'
salesforce | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": true,
    "name": "nginx",
    "state": "started",
    "status": {
...
        "UnitFileState": "disabled",
        "WatchdogTimestampMonotonic": "0",
        "WatchdogUSec": "0"
    }
}
```

Verify connectivity at http://salesforce.training.arborian.com 

Alternatively, try using cURL:

```bash
$ curl -i http://salesforce.training.arborian.com
HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Tue, 22 Sep 2020 15:03:30 GMT
Content-Type: text/html
Content-Length: 4833
Last-Modified: Fri, 16 May 2014 15:12:48 GMT
Connection: keep-alive
ETag: "53762af0-12e1"
Accept-Ranges: bytes
...
```

