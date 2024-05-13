from subprocess import run, STDOUT, PIPE

cmd = "pkexec cat /var/log/secure*"
output = run(cmd, stdout=PIPE, stderr=STDOUT, text=True, shell=True)
list = output.stdout.split("\n")
print(list)