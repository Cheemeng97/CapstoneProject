import paramiko

def sshPost_MacAddress(moduleCode, macAddress):
    commands = [
        'uci add firewall rule',
        'uci set firewall.@rule[-1].src="lan"',
        'uci set firewall.@rule[-1].dest="wan"',
        'uci set firewall.@rule[-1].target="ACCEPT"',
        'uci set firewall.@rule[-1].name="Filter-Parental-Controls"',
    ]

    commitFirewall = 'uci commit firewall'
    restartFirewall = '/etc/init.d/firewall restart'

    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.3.1', username='root', password='Qsfhk!xdr1')

    # for macAddress in macList:
        
    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command)

        nameCommand = f'uci set firewall.@rule[-1].name="{moduleCode}-{macAddress}"'
        stdin, stdout, stderr = ssh.exec_command(nameCommand)

        macAddressCommand = f'uci set firewall.@rule[-1].src_mac="{macAddress}"'
        stdin, stdout, stderr = ssh.exec_command(macAddressCommand)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if output:
            print(output)
        if error:
            print(error)

    stdin, stdout, stderr = ssh.exec_command(commitFirewall)
    output = stdout.read().decode()
    error = stderr.read().decode()
    if output:
        print(output)
    if error:
        print(error)

    stdin, stdout, stderr = ssh.exec_command(restartFirewall)
    output = stdout.read().decode()
    error = stderr.read().decode()
    if output:
        print(output)
    if error:
        print(error)

    # close SSH connection
    ssh.close()
