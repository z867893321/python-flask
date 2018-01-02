import docker
import time
class container():
	def create_container(self,filename):
		client = docker.from_env()
		cmd = 'python '+' '+filename
		c1 = client.containers.run('python:3',
                           command=cmd,
                           detach=True,
                           stdin_open=True,
                           volumes={'/web/data':{'bind':'/opt','mode':'rw'}},
                           working_dir='/opt',
                         )
		c1.wait()
		c_logs=open('/opt/logs','w')
		c_logs.close()
		c_logs=open('/opt/logs','a')
		line=str(c1.logs(follow=True),encoding='utf-8')
		c_logs.write(line)
		c_logs.close
		c1.remove()
	
