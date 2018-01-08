Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.box_check_update = false
  config.ssh.forward_agent = false

  # config.vm.provision "ansible" do |ansible|
  #   ansible.playbook = "playbooks/vagrant.yaml"
  #   ansible.groups = {
  #     "webdb" => ["web", "db"],
  #     "webdb:vars" => {"ntp_server" => "ntp.atlanta.example.com",
  #                      "proxy" => "proxy.atlanta.example.com"}
  #   }
  # end

  config.vm.define "controller" do |controller|
    controller.vm.box = "ansible-class"
    controller.vm.hostname = "controller"
    controller.vm.network "private_network", ip: "10.0.3.50"
  end

  config.vm.define "web" do |web|
    web.vm.hostname = "web"
    web.vm.network "forwarded_port", guest: 80, host: 8080
    web.vm.network "private_network", ip: "10.0.3.51"
  end

  config.vm.define "db" do |db|
    db.vm.hostname = "db"
    db.vm.network "private_network", ip: "10.0.3.52"
  end


end
