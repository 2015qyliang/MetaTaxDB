# -*- coding: utf-8 -*-
# Copyright： qyliang
# time: 06-13-2018

'''
输出提示信息：
1. 是否在vsearch文件夹下建立相应project文件夹
2. 使用16S高通量序列格式是(a) fastaq还是(b) fasta
3. 如果使用的序列格式为fastq，是否在project文件夹下建立相应的原始序列fqfile文件夹
4. 如果使用的序列格式为fasta，是否在project文件夹下建立相应的原始序列filtedfile文件夹
'''

import os
import sys
# 定义vsearch函数
def Vsearch(processType, idOTU = 0.97, idChimerotus = 0.97, idTax = 0.97):
	vsearch = './vsearchlinux/bin/vsearch'
	fnlist = os.listdir(fileAddr)
	for fn in fnlist:
		fnfirst = fn.split('.')[0]
		# 构建分部流程
		# 1-质量控制
		proc11 = vsearch + ' --fastq_filter ./' + projectname + '/fqfile/' + fn
		proc12 = ' --fastq_maxee_rate 0.01 --fastaout ./' + projectname + '/filtedfile/'
		process1 = proc11 + proc12 + fnfirst + '_filted.fasta'
		# 2-序列去冗余/搜寻单一序列
		proc21 = vsearch + ' --derep_fulllength ./' + projectname + '/filtedfile/' + fn
		proc22 = ' --sizeout --minuniquesize 2 --output ./' + projectname + '/uniquesfile/'
		process2 = proc21 + proc22 + fnfirst + '_uniques.fasta'
		# 3-聚类生成OTU
		proc31 = vsearch + ' --cluster_fast ./' + projectname + '/uniquesfile/' + fnfirst + '_uniques.fasta --id '
		proc32 = idOTU + ' --centroids ./' + projectname + '/otusfile/'
		process3 = proc31 + proc32 + fnfirst + '_otus.fasta' + ' --relabel OTU_'
		# 4-去除嵌合体
		# 细菌可用Usearch作者整理的RDP Gold数据库去除嵌合体
		# wget http://drive5.com/uchime/rdp_gold.fa
		proc41 = vsearch + ' --uchime_ref ./' + projectname + '/otusfile/' + fnfirst + '_otus.fasta'
		proc42 = ' --db ./rdp_gold.fa --nonchimeras ./' + projectname + '/nonchimerotusfile/'
		process4 = proc41 + proc42 + fnfirst + '_nonchimerotus.fasta'
		# 5-生成OTU表格,其中可以使用--threads 4
		proc51 = vsearch + ' --usearch_global ./' + projectname + '/filtedfile/' + fn + ' --db '
		proc52 = './' + projectname + '/nonchimerotusfile/' + fnfirst + '_nonchimerotus.fasta --id '
		proc53 = idChimerotus + ' --otutabout ./'+ projectname + '/otutabfile/'
		process5 = proc51 + proc52 + proc53 + fnfirst + '_otutab.txt'
		# 6-物种注释
		proc61 = vsearch + ' --usearch_global ./' + projectname + '/nonchimerotusfile/'  + fnfirst + '_nonchimerotus.fasta'
		proc62 = ' --db ./vsearchsilva.udb --id ' + idTax + ' --blast6out ./' + projectname + '/taxfile/'
		process6 = proc61 + proc62 + fnfirst + '_tax.txt'
		if processType == '1-6':
			print('='*80)
			print('='*10,' Which is file on going? ',fn)
			print('='*10,' File order? ',fnlist.index(fn)+1)
			os.system(process1)
			os.system(process2)
			os.system(process3)
			os.system(process4)
			os.system(process5)
			os.system(process6)
		elif processType == '2-6':
			print('='*80)
			print('='*10,' Which is file on going? ',fn)
			print('='*10,' File order? ',fnlist.index(fn)+1)
			os.system(process2)
			os.system(process3)
			os.system(process4)
			os.system(process5)
			os.system(process6)
		elif processType == '6':
			print('='*80)
			print('='*10,' Which is file on going? ',fn)
			print('='*10,' File order? ',fnlist.index(fn)+1)
			os.system(process6)
		else:
			pass

# 询问是否已建有相应的项目文件夹，若有pass，若无则在当前路径下建立相应的项目文件夹
haveproject = raw_input('是否已建立项目文件（y/n）：')
if haveproject == 'y':
	projectname = raw_input('请输入项目名称（英文）：')
	pass
elif haveproject == 'n':
	projectname = raw_input('请命名项目名称（英文）：')
	os.chdir('/run/media/microbe/9cfa605f-2865-421d-9d6a-bca11659d5a8/vsearch/')
	os.mkdir(projectname)
	creatRelativeFile = raw_input('是否创建项目文件中的相应的文件夹（比如fqfile、filtedfile等）（y/n）：')
	if creatRelativeFile == 'y':
		os.chdir(projectname)
		os.mkdir('fqfile')
		os.mkdir('filtedfile')
		os.mkdir('uniquesfile')
		os.mkdir('otusfile')
		os.mkdir('nonchimerotusfile')
		os.mkdir('otutabfile')
		os.mkdir('taxfile')
	elif creatRelativeFile == 'n':
		pass
	else:
		pass
else:
	pass

# 询问是否已将原始序列上传至服务器
uploadRowSeq = raw_input('是否已将原始序列上传至fqfile或者filtedfile（y/n）:')
if uploadRowSeq == 'n':
	whichtype = raw_input('待上传的原始序列格式为哪种类型（fq或者fasta）：')
	if whichtype == 'fq':
		print('请将原始序列文件上传至相应项目的fqfile文件夹中')
	elif whichtype == 'fasta':
		print('请将原始序列文件上传至相应项目的filtedfile文件夹中')
	else:
		pass
	sys.exit(0)
elif uploadRowSeq == 'y':
	pass
else:
	pass

rawSeqType = raw_input('请确认上传的原始数据格式（fastq/fasta）:')
runVsearch = raw_input('是否首次进行vsearch 16S高通量序列分析流程（y/n）:')
assignmentTaxon = raw_input('重新分配注释信息？（y/n）:')
dbAddr = '/run/media/microbe/9cfa605f-2865-421d-9d6a-bca11659d5a8/vsearch/'
os.chdir('/run/media/microbe/9cfa605f-2865-421d-9d6a-bca11659d5a8/vsearch/')

if (runVsearch == 'y') and (rawSeqType == 'fastq') :
	fileAddr = dbAddr + projectname + '/fqfile'
	IdOTU = raw_input('聚类OTU使用的阈值（推荐0.97）：')
	IdChimerotus = raw_input('清除嵌合体使用的阈值（种,0.97;属,0.93;科,0.86;目,0.82）：')
	IdTax = raw_input('物种注释使用的阈值（种,0.97;属,0.93;科,0.86;目,0.82）：')
	Vsearch('1-6', idOTU = IdOTU, idChimerotus = IdChimerotus, idTax = IdTax)
elif (runVsearch == 'y') and (rawSeqType == 'fasta') :
	fileAddr = dbAddr + projectname + '/filtedfile'
	IdOTU = raw_input('聚类OTU使用的阈值（推荐0.97）：')
	IdChimerotus = raw_input('清除嵌合体使用的阈值（种,0.97;属,0.93;科,0.86;目,0.82）：')
	IdTax = raw_input('物种注释使用的阈值（种,0.97;属,0.93;科,0.86;目,0.82）：')
	Vsearch('2-6', idOTU = IdOTU, idChimerotus = IdChimerotus, idTax = IdTax)
elif (runVsearch == 'n') and (assignmentTaxon == 'y'):
	fileAddr = dbAddr + projectname + 'filtedfile'
	IdTax = raw_input('物种注释使用的阈值（种,0.97;属,0.93;科,0.86;目,0.82）：')
	Vsearch('6', idTax = IdTax)
else:
	pass
