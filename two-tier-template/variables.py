import uuid
import subprocess

temp_ssh_key = subprocess.Popen(['cat', '/root/.ssh/id_rsa-gcloud.pub'], stdout = subprocess.PIPE)
# get the output as a string
ssh_output = str(temp_ssh_key.communicate()[0].rstrip(), 'utf-8')
#temp_service_account = subprocess.Popen(['gcloud', 'config', 'list', 'account', '--format', "\"value(core.account)\""], stdout = subprocess.PIPE) 
temp_service_account = subprocess.Popen(['gcloud', 'config', 'list', 'account'], stdout = subprocess.PIPE)
service_output = temp_service_account.communicate()


service_output2 = str(service_output[0]).split("=")[1].strip().rstrip("'")[:-2]
#Variables
zone = "us-central1-a"
region = "us-central1"
sshkey = ssh_output
serviceaccount = service_output2


fname = 'generated.py'
data = 'zone = "us-central1-a"\nregion = "us-central1"'+'\nsshkey = "'+ssh_output+'"\nserviceaccount = "'+service_output2+'"\n'

with open(fname, 'w') as f:
    f.write('{}'.format(data))

