# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Use a small Debian box
  config.vm.box = "chef/debian-7.6"

  # Prepare the Vm
  config.vm.define "yeoman-vm" do |machine|

        machine.vm.hostname = "yeoman-vm"

        # Provision the VM using the shell
        config.vm.provision "shell", inline: "apt-get update && apt-get -y install python"

        # Provision the VM using ansible
        config.vm.provision "ansible" do |ansible|
          ansible.playbook = "etc/yeoman.yaml"
          ansible.extra_vars = { ansible_ssh_user: 'vagrant' }
        end
  end
end
