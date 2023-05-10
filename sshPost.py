import paramiko

macList = ["01:23:45:67:89:aa", "01:23:45:67:89:bb"]

commands = [
    'uci add firewall rule',
    'uci set firewall.@rule[-1].name="Filter-Parental-Controls"',
    'uci set firewall.@rule[-1].src="lan"',
    'uci set firewall.@rule[-1].dest="wan"',
    'uci set firewall.@rule[-1].target="REJECT"',
    # f'uci set firewall.@rule[-1].src_mac="{macAddress}"',
]

commitFirewall = 'uci commit firewall'
restartFirewall = '/etc/init.d/firewall restart'

# Establish SSH connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.168.1', username='root', password='cheemeng')

# send command and get output
# stdin, stdout, stderr = ssh.exec_command('ls -l')
# output = stdout.read().decode()

for macAddress in macList:
    
    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command)
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



# uci add firewall rule
# uci set firewall.@rule[-1].name="Filter-Parental-Controls"
# uci set firewall.@rule[-1].src="lan"
# uci set firewall.@rule[-1].src_mac="00:11:22:33:44:55"
# uci set firewall.@rule[-1].dest="wan"
# uci set firewall.@rule[-1].start_time="21:30:00"
# uci set firewall.@rule[-1].stop_time="07:00:00"
# uci set firewall.@rule[-1].weekdays="Mon Tue Wed Thu Fri"
# uci set firewall.@rule[-1].target="REJECT"
# uci commit firewall
# /etc/init.d/firewall restart