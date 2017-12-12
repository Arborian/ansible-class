Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.box_check_update = false

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbooks/basic.yaml"
    ansible.groups = {
      "webdb" => ["web", "db"],
      "webdb:vars" => {"ntp_server" => "ntp.atlanta.example.com",
                       "proxy" => "proxy.atlanta.example.com"}
    }
  end

  config.vm.define "web" do |web|
    web.vm.hostname = "web"
    web.vm.network "forwarded_port", guest: 80, host: 8080
  end

  config.vm.define "db" do |db|
    db.vm.hostname = "db"
  end


end
