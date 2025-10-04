Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  # config.vm.network "private_network", ip: "192.168.56.10"
  config.vm.network "public_network", ip: "192.168.1.75"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "8192"
  end
end
