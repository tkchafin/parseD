#!/usr/bin/python

import re
import sys
import os
import getopt

def main():
	params = parseArgs()

	data = dict()

		#Print dict to phylip file
		# with open(params.out, 'w') as fh:
		# 	try:
		# 		header = getPhylipHeader(data) + "\n"
		# 		fh.write(header)
		#
		# 		for sample in data:
		# 			line = str(sample) + "\t" + "".join(data[sample]) + "\n"
		# 			fh.write(line)
		# 	except IOError:
		# 		print("Could not write to file ",params.out)
		# 		sys.exit(1)
		# 	finally:
		# 		fh.close()


#Read VCF variant calls
#Generator function, yields each locus
def read_vcf(v):

	try:
		vfh = vcf.Reader(filename=v)
	except IOError as err:
		print("I/O error({0}): {1}".format(err.errno, err.strerror))
	except:
		print("Unexpected error:", sys.exec_info()[0])

	chrom = ""
	recs = []
	added = 0
	for rec in vfh:
		if not rec.FILTER:
			yield(rec)


#Object to parse command-line arguments
class parseArgs():
	def __init__(self):
		#Define options
		try:
			options, remainder = getopt.getopt(sys.argv[1:], 'i:zho:a:s', \
			["input=","help","out=","alpha=","popz","sigp"])
		except getopt.GetoptError as err:
			print(err)
			self.display_help("\nExiting because getopt returned non-zero exit status.")
		#Default values for params
		#Input params
		self.input=None
		self.alpha=0.05
		self.popz=False
		self.sigp=False
		self.out="d_summary.tsv"

		#First pass to see if help menu was called
		for o, a in options:
			if o in ("-h", "-help", "--help"):
				self.display_help("Exiting because help menu was called.")

		#Second pass to set all args.
		for opt, arg_raw in options:
			arg = arg_raw.replace(" ","")
			arg = arg.strip()
			opt = opt.replace("-","")
			#print(opt,arg)
			if opt in ('i', 'input'):
				self.input = str(arg)
			elif opt in ('h', 'help'):
				pass
			elif opt in ('o','out'):
				self.out = str(arg)
			elif opt in ('a','alpha'):
				self.alpha = float(arg)
			elif opt in ('z','popz'):
				self.popz = True
			elif opt in ('s','sigp'):
				self.sigp = True
			else:
				assert False, "Unhandled option %r"%opt

		#Check manditory options are set
		if not self.input:
			self.display_help("\nError: Missing required input files <-i,--input>")


	def display_help(self, message=None):
		if message is not None:
			print (message)
		print ("\nparseD.py\n")
		print ("Contact:Tyler K. Chafin, University of Arkansas,tkchafin@uark.edu")
		print ("\nUsage: ", sys.argv[0], "-i </path/to/output>\n")
		print ("Description: Parse lots of D-tests")

		print("""
	Arguments:
		-i,--input	: Output files from CompD (Passed as /path/to/*.txt)
		-z,--popz	: Boolean. Toggle if you want summaries to include Pop Z-test
		-a,--alpha	: Alpha threshold for determining significance
		-s,--sigp	: Boolean. Toggle on if you want to only output signficicant tests
		-o,--out	: Name for output file <default = ./d_summary.tsv>
		-h,--help	: Displays help menu

""")
		sys.exit()

#Call main function
if __name__ == '__main__':
    main()
