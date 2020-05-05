import os
import subprocess
import re
import string
import io
import sys, getopt

def main(argv):
	inputfile = ""
	profile = ""
	browser = "all"
	output = ""

	try:
		arguments, values = getopt.getopt(argv,"hf:p:b:o:",["help","file=","profile=","browser=","output="])
	except getopt.error as err:
		print("python project.py -f <inputfile> -p <profile> -b <ie|chrome|firefox|all> -o <output>")
		print(str(err))
		sys.exit()
   	
	for arg, val in arguments:
		if arg in ("-h", "--help"):
			print('python project.py -f <inputfile> -p <profile> -b <ie|chrome|firefox|all> -o <output>')
			sys.exit()
		elif arg in ("-f", "--ifile"):
			inputfile = val
		elif arg in ("-p", "--profile"):
			profile = val
		elif arg in ("-b", "--browser"):
			if val not in ["chrome","iexplore","firefox","all"]:
				print('Error: wrong input: the browser input must be iexplore, chrome, firefox or all')
				sys.exit()
			else:
				browser = val
		elif arg in ("-o", "--output"):

			output = val
   	
   	if(inputfile == "" or profile == "" or output == ""):
   		print('Error: wrong input')
   		print inputfile
   		print profile
   		print output
   		print("python project.py -f <inputfile> -p <profile> -b <iexplore|chrome|firefox|all> -o <output>")
   		sys.exit()

   	return inputfile, profile, browser, output

def findwebproc(filepath, profile, browser):
	# step 1 : file processess ID of web browser
	inpprof = "--profile="+profile
	proclist = []
	webproc = []

	if browser == "all":
		webproc = ["chrome","firefox","iexplore"]
	else:
		webproc.append(browser)
	
	process = subprocess.Popen(['python','vol.py','-f',filepath, inpprof, 'pslist'],
						stdout=subprocess.PIPE, 
						stderr=subprocess.PIPE)
	stdout,stderr = process.communicate()

	for line in stdout.splitlines():
		record = line.split()
		if record[1].split('.')[0] in webproc: 
			proclist.append(record[2])	

	return proclist

def memdump(filepath, profile, proclist):
	# step 2 : dump memory of each process ID
	inpprof = "--profile="+profile

	os.popen('rm -rf *.dmp')
	
	for proc in proclist:
		process = subprocess.Popen(['python','vol.py','-f',filepath, inpprof, 'memdump', '-p', proc, '--dump-dir=./'],
						stdout=subprocess.PIPE, 
						stderr=subprocess.PIPE)
		stdout,stderr = process.communicate()
		print proc

def urlscan(proclist):
	# step 3 : searching for url
	weblist = {}

	for proc in proclist:
		file = proc+".dmp"
		try:
			for url in re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F])){6,}',open(file,"rb").read()):
				weblist[url.strip('/')] = 1
		except:
			continue	

	return weblist

def carveimage(output):	
	cmd = "scalpel -c img.conf -o "+output + " *.dmp"
	os.popen(cmd)
	
def export(weblist,output):
	output = output+"/urls.txt"

	f = open(output,"w")
	for url in weblist:
			f.write(url+"\r\n")
	f.close()


if __name__ == "__main__":	
	
		
	file, profile, browser, output = main(sys.argv[1:])
	
	subprocess.Popen(['rm',  '-rf',output])	
	subprocess.Popen(['mkdir',output])	

	print("=== Starting run the script ...")
	proclist = findwebproc(file, profile, browser)
	print("=== Finding web browser process ID completed")
	print("=== Process ID found")
	print(proclist)

	print("=== Dumping memory in progress ...")
	memdump(file, profile, proclist)
	print("=== Dumping memory completed")
	
	print("=== Carving images in progress  ...")
	carveimage(output)
	print("=== Completed, All images have been recovered!")
	
	print("=== Extracting Web URL in progress  ...")
	weblist = urlscan(proclist)
	export(weblist, output)
	print("=== Completed, All URLs have been recovered!")
	
	os.popen('rm -rf *.dmp')


	