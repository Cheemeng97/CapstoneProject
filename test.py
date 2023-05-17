import paramiko


# SSH command to retrieve firewall details
command = "uci show firewall"

# Create SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to OpenWRT router
    ssh.connect('192.168.3.1', username='root', password='Qsfhk!xdr1')

    # Execute the SSH command
    stdin, stdout, stderr = ssh.exec_command(command)

    # Read and print the output
    output = stdout.read().decode()
    print(output)

finally:
    # Close the SSH connection
    ssh.close()