# -*- coding: utf-8 -*-
import os

os.chdir('/home/temp/OTUsTable')
file = open('SearchGroups.txt')
namelist = []
for line in file.readlines():
	namelist.append(line.split('\n')[0] + '.txt')
file.close()

filetext = []
filetext.append('ERRfile'+'\t'+'OTUsSeqHit'+'\t'+'OTUsSeqTotal'+'\t'+'OTUsSeqPercent'+'\n')
for fn in namelist:
	fnfirst = fn.split('.')[0]
	otufn = fn
	os.chdir('/home/temp/TaxFile')
	if os.path.exists(fn) == True:
		print('=====  which file ongoing ? ',fn,'  =====')
		filetext.append(fnfirst)

		# hit count
		otucount = 0	
		file = open(fn)
		os.chdir('/home/temp/OTUsTable')
		for line in file.readlines():
			# 'Deltaproteobacteria' can be replaced with other microbial groups
			if 'Deltaproteobacteria' in line:
				print('=========  Here hited ========')
				hitotu = line.split('\t')[0]			
				otufile = open(otufn)
				for ln in otufile.readlines():
					if (hitotu in ln) and ('OTU ' not in ln):
						count = ln.split('\n')[0].split('\t')[1]
						otucount = otucount + int(count)
						break
				otufile.close()
		file.close()

		# hit percent
		totalotu = 0
		otufile = open(otufn)
		for ln in otufile.readlines():
			if 'OTU_' in ln:
				count = ln.split('\n')[0].split('\t')[1]
				totalotu += int(count)
		otufile.close()

		filetext.append('\t'+str(otucount)+'\t'+str(totalotu)+'\t'+str(float(otucount/totalotu))+'\n')

os.chdir('/home/temp')
with open('SummaryPercent.txt','w') as file:
	for line in filetext:
		file.write(line)
	file.close()

