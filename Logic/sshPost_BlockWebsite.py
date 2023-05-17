import paramiko

def sshPost_BlockWebsite(website):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.3.1', username='root', password='Qsfhk!xdr1')

        commands = [
        'uci add firewall rule',
        'uci set firewall.@rule[-1].src="lan"',
        'uci set firewall.@rule[-1].dest="wan"',
        'uci set firewall.@rule[-1].target="REJECT"',
        ]

        commitFirewall = 'uci commit firewall'
        restartFirewall = '/etc/init.d/firewall restart'
        # website = "https://chat.openai.com/"

        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if output:
                print(output)
            if error:
                print(error)

        stdin, stdout, stderr = ssh.exec_command(f'uci set firewall.@rule[-1].name="Block-"{website}""')
        output = stdout.read().decode()
        error = stderr.read().decode()
        if output:
            print(output)
        if error:
            print(error)

        stdin, stdout, stderr = ssh.exec_command(f'uci set firewall.@rule[-1].dest_ip="{website}"')
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
        return "Blocked"
    except:
        return "Pending"

