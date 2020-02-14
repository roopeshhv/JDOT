import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('10.4.96.74', username='vivek', password='nutanix/4u')

stdin, stdout, stderr = client.exec_command('cd /home/nutanix; wget http://10.4.8.60/acro_images/DISKs/cirros-0.3.4-x86_64-disk.img')

#for line in stdout:
#    print line.strip('\n')

client.close()
