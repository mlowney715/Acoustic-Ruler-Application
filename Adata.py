import ConfigParser
import datetime
import os

class Adata:

	def __init__(self, configname):
		self.config = ConfigParser.RawConfigParser()
		if os.path.isfile(configname):
			self.load(configname)
		else:
			self.newconfig(configname)

	def newconfig(self, configname):
		self.config.add_section('phys_env')
		self.config.set('phys_env', 'speed_sound', '343')
		self.config.add_section('data_env')
		self.config.set('data_env', 'log_path', './')
		with open(configname, 'wb') as configfile:
			self.config.write(configfile)
		configfile.close()
		self.speed = self.config.getfloat('phys_env', 'speed_sound')
		self.path = self.config.get('data_env', 'log_path')

	def load(self, configname):
		self.config.read(configname)
		self.speed = self.config.getfloat('phys_env', 'speed_sound')
		self.path = self.config.get('data_env', 'log_path')

	def changespeed(self, newspeed):
		self.config.set('phys_env','speed_sound',newspeed)
		with open('ruler.cfg', 'wb') as configfile:
			self.config.write(configfile)
		configfile.close()
		self.speed = float(newspeed)

	def changepath(self, newpath):
		if newpath[0] == '~':
			newpath = os.environ['HOME'] + newpath[1:]
		if not os.path.isdir(newpath):
			try:
				os.makedirs(newpath, 0755)
			except OSError:
				print "Permission Denied: mkdir"
				return
		else:
			try:
				test = open(newpath+'/'+'foo', 'w+')
			except IOError:
				print "Warning: No write permission, but path changed."
			try:
				test.close()
			except UnboundLocalError:
				pass
			try:
				os.remove(newpath+'/'+'foo')
			except OSError:
				pass
		self.config.set('data_env','log_path',newpath)
		with open('ruler.cfg', 'wb') as configfile:
			self.config.write(configfile)
		configfile.close()
		self.path = newpath

	def createLogFile(self):
                log = open(self.path+"/"+"SingleChannelLog-"+str(datetime.date.today())+".txt", "a")
	
	def measure(self, delay):
		distance = self.speed*float(delay)
		log = open(self.path+"/"+"SingleChannelLog-"+str(datetime.date.today())+".txt", "a")
		log.write("\nTime: "+str(datetime.datetime.now().time())+"\n")
		log.write("Delay: " + str(delay)+" msec\n")
		log.write("Distance: " + str(distance)+" m\n\n")
