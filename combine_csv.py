# Import needed modules
import csv

# Set paths
fout_path = "/home/babykitty/tmp/K_all.csv" #Full path of the output file
f_dir = "/home/babykitty/tmp/" #Path to the directory that contains the csv files

# Set ouput csv file
fout = open(fout_path,"a")

# Write first line seperately so that we have headers
for line in open(f_dir+"K_subset_ 1 .csv"):
	line = line.rstrip()+",1\n"
	fout.write(line)
	print line
	print type(line)

# Now the rest of the files
for i in range(2,331):
	try: # Not all instances exist from 2 to 330 so a try/except block is used to skip over missing numbers
		f = open(f_dir+"K_subset_ "+str(i)+" .csv")
		f.next() #Skip the header
		for line in f:
			line = line.rstrip()+","+str(i)+"\n"
			fout.write(line)
			print line
			print type(line)
		f.close() #Just to sure everything is tidy
	except:
		pass

# Close output file
fout.close()
