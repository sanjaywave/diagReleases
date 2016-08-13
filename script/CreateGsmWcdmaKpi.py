from csv_processor import ParseCSV
import Time_Calculation_GSM_WCDMA
import csv
import gzip
import sys
import getopt
import os
import time
import glob
import math


def GSM_WCDMA_COUNTER_FILE_PATH(inputstring):
	"""
	It returns the path of GSM WCDMA COUNTER FILE PATH
	"""
	GSM_WCDMA_COUNTER_FILE_PATH = inputstring + 'GSM_WCDMA_COUNTER/*.csv.gz'
	GSM_WCDMA_COUNTER_FILE_PATH = glob.glob(GSM_WCDMA_COUNTER_FILE_PATH)
	GSM_WCDMA_COUNTER_FILE_PATH = ''.join(map(str,GSM_WCDMA_COUNTER_FILE_PATH))
	return GSM_WCDMA_COUNTER_FILE_PATH

def GSM_WCDMA_KPI_FILE_PATH(inputstring):
	"""
	It returns the path of GSM WCDMA KPI FILE PATH
	"""
	GSM_WCDMA_KPI_FILE_PATH = inputstring + 'GSM_WCDMA_KPI/*.csv.gz'
	GSM_WCDMA_KPI_FILE_PATH = glob.glob(GSM_WCDMA_KPI_FILE_PATH)
	GSM_WCDMA_KPI_FILE_PATH = ''.join(map(str,GSM_WCDMA_KPI_FILE_PATH))
	return GSM_WCDMA_KPI_FILE_PATH

def output_file_path(inputfile):
	"""
	It creates the output folder and returns its path and file name
	"""
	outputfile = inputfile + 'GSM_WCDMA_COUNT_CALC'
	if not os.path.exists(outputfile):
		os.makedirs(outputfile)
	inputfile = GSM_WCDMA_COUNTER_FILE_PATH(inputfile)
	nameOfFile = inputfile.split('/')
	outputfile = outputfile +'/'+ nameOfFile[-1]
	return outputfile


def WCDMA_CS_MO_Single_RAB_Mean_Call_Connect_Time(Object):
	"""
	It returns average value of the CS MO Single RAB WCDMA CS call connect time
	"""
	WCDMA_CS_MOCALL_SINGLE_RAB_CONNECT_AVG = Object.getAverageValueInColumn(Object.getColumnIndexByName('WCDMA_CS_MOCALL_SINGLE_RAB_CONNECT_TIME'))
	return WCDMA_CS_MOCALL_SINGLE_RAB_CONNECT_AVG

def WCDMA_CS_MO_Multi_RAB_Mean_Call_Connect_Time(Object):
	"""
	It return average value of the CS MO Multi RAB WCDMA CS call connect time
	"""
	WCDMA_CS_MOCALL_MULTIPLE_RAB_CONNECT_AVG = Object.getAverageValueInColumn(Object.getColumnIndexByName('WCDMA_CS_MOCALL_MULTIPLE_RAB_CONNECT_TIME'))
	return WCDMA_CS_MOCALL_MULTIPLE_RAB_CONNECT_AVG

def WCDMA_CS_MT_Access_Mean_Call_Connect_Time(Object):
	"""
	It return average value of the CS MT Access WCDMA CS call connect time
	"""
	WCDMA_CS_MTCALL_SINGLE_RAB_CONNECT_AVG = Object.getAverageValueInColumn(Object.getColumnIndexByName('WCDMA_CS_MTCALL_SINGLE_RAB_CONNECT_TIME'))
	return WCDMA_CS_MTCALL_SINGLE_RAB_CONNECT_AVG

def CS_Transmit_Power_Count(Object):
	return Object.getNumOfValuesInColumn(Object.getColumnIndexByName('WCDMA_Tx_Power_CS'))

def CS_Transmit_Power_Average(Object):
	"""
	it returns the average of the CS Transmit Power by formula alpha*current_elem + (1-alpha)*avg
	"""
	CS_Transmit_Power_List = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_Tx_Power_CS'))
	#CS_Transmit_Power_List = filter(None, CS_Transmit_Power_List)
	i = 0
	avg = 0.0
	prev_elem = 0.0
	for elem in CS_Transmit_Power_List:
		elem = 10*float(elem) + 188
		prev_elem = float(CS_Transmit_Power_List[i - 1])*10 + 188
		avg = elem*0.6 + avg*0.4
		i = i + 1
	return (avg+512)/10-70

def PS_Transmit_Power_Count(Object):
	return Object.getNumOfValuesInColumn(Object.getColumnIndexByName('WCDMA_Tx_Power_PS'))

def PS_Transmit_Power_Average(Object):
	"""
	it returns the average of the CS Transmit Power by formula alpha*current_elem + (1-alpha)*avg
	"""
	PS_Transmit_Power_List = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_Tx_Power_PS'))
	#PS_Transmit_Power_List = filter(None, PS_Transmit_Power_List)
	i = 0
	avg = 0.0
	prev_elem = 0.0
	for elem in PS_Transmit_Power_List:
		elem = 10*float(elem) + 188
		if i:
			prev_elem = float(PS_Transmit_Power_List[i - 1])*10 + 188
		avg = elem*0.6 + avg*0.4
		i = i + 1
	return (avg+512)/10-70

def CS_EcIo_Count(Object):
	CS_EcIo_List = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_ECIO_CS'))
	return len(CS_EcIo_List)

def antilog(x):
	return 10 ** x

def CS_EcIo_Average(Object):
	"""
	it returns the average of the CS Transmit Power by formula alpha*current_elem + (1-alpha)*avg
	"""
	CS_EcIo_List = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_ECIO_CS'))
	i = 0
	avg = 0
	prev_elem = 0
	for elem in CS_EcIo_List:
		elem = antilog(float(elem))
		if i:
			prev_elem = antilog(float(CS_EcIo_List[i - 1]))
		avg = elem*0.6 + avg*0.4
		i = i + 1
	try:
		return math.log10(avg)
	except Exception:
		print 'Warning:CS_EcIo_Average is empty'
		return ''



def PS_EcIo_Count(Object):
	PS_EcIo_List = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_ECIO_PS'))
	#PS_EcIo_List = filter(lambda a: a != '0.000000 ', PS_EcIo_List)
	return len(PS_EcIo_List)

def PS_EcIo_Average(Object):
	"""
	it returns the average of the CS Transmit Power by formula alpha*current_elem + (1-alpha)*avg
	"""
	PS_EcIo_List = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_ECIO_PS'))
	#PS_EcIo_List = filter(lambda a: a != '0.000000 ', PS_EcIo_List)
	i = 0
	avg = 0
	prev_elem = 0
	for elem in PS_EcIo_List:
		elem = antilog(float(elem))
		if i:
			prev_elem = antilog(float(PS_EcIo_List[i - 1]))
		avg = elem*0.6 + avg*0.4
		i = i + 1
	try:
		return math.log10(avg)
	except Exception:
		print 'Warning:PS_EcIo_Average counter is empty'
		return ''


def RACH_Success_WCDMA(Object):
	try:
		WCDMA_Rach_Success_Count = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_Rach_Success_Count')))
		return WCDMA_Rach_Success_Count
	except Exception:
		print 'Warning:RACH_Success_WCDMA counter is empty'
		return ''


def RACH_FAILURE_WCDMA(Object):
	try:
		WCDMA_Rach_Total_Count = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_Rach_Total_Count')))
		WCDMA_Rach_Success_Count = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_Rach_Success_Count')))
		if WCDMA_Rach_Total_Count:
			RACH_FAILURE_WCDMA = WCDMA_Rach_Total_Count - WCDMA_Rach_Success_Count
			return RACH_FAILURE_WCDMA
		else:
			return ''
	except Exception:
		print 'Warning:WCDMA_Rach_Total_Count counter is empty'
		return ''

def RACH_Failure_Rate_WCDMA(Object):
	try:
		WCDMA_Rach_Total_Count = float(Object.getLastValue(Object.getColumnIndexByName('WCDMA_Rach_Total_Count')))
		RACH_Failure_Rate_WCDMA = RACH_FAILURE_WCDMA(Object)*100/(WCDMA_Rach_Total_Count)
		return RACH_Failure_Rate_WCDMA
	except Exception:
		print "Warning:WCDMA_Rach_Total_Count counter is empty"
		return ''

def Time_between_handover_WCDMA(Object,Dict_of_time_in_technologies):
	"""
	return the Time between soft handovers in WCDMA
	"""
	try:
		Time_between_handover_WCDMA = Dict_of_time_in_technologies['WCDMA']/int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_SoftHandover_Success')))
		return Time_between_handover_WCDMA
	except Exception:
		print "Warning:WCDMA_SoftHandover_Success = 0"
		return ''

def Time_between_Inter_frequency_handover(Object,Dict_of_time_in_technologies):
	"""
	return the Time between Inter Frequency handovers in WCDMA
	"""
	try:
		Time_between_Inter_frequency_handover = Dict_of_time_in_technologies['WCDMA']/(int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Inter_Freq_Handover_Success_Count')))*60)
		return Time_between_Inter_frequency_handover
	except Exception:
		print "Warning:Wcdma_Inter_Freq_Handover_Success_Count = 0"
		return ''

def Time_between_Hard_Intra_frequency_handover(Object,Dict_of_time_in_technologies):
	"""
	return the Time between hard intra Frequency handovers in WCDMA
	"""
	try:
		Time_between_Hard_Intra_frequency_handover = Dict_of_time_in_technologies['WCDMA']/(int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Intra_Freq_Handover_Success_Count')))*60)
		return Time_between_Hard_Intra_frequency_handover
	except Exception:
		print "Warning:Wcdma_Intra_Freq_Handover_Success_Count = 0"
		return ''

def WCDMA_PS_Setup_success_rate(Object):
	try:
		WCDMA_PDPContextAttemptCount_Single = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_PDPContextAttemptCount_Single_RAB')))
		WCDMA_PDPContextActivateCount_Single = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_PDPContextActivateCount_Single_RAB')))
		WCDMA_PS_Setup_success_rate = WCDMA_PDPContextActivateCount_Single*100/WCDMA_PDPContextAttemptCount_Single
		return WCDMA_PS_Setup_success_rate
	except Exception:
		print "Warning:WCDMA_PDPContextAttemptCount_Single = 0"
		return ''

def WCDMA_PS_retainability_Rate_MultiRAB(Object):
	try:
		WCDMA_PDPContextActivateCount_Multi = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_PDPContextActivateCount_Multi_RAB')))
		WCDMA_PDPContextDeactivateCount_Multi = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_PDPContextDeactivateCount_Multi_RAB')))
		WCDMA_PS_retainability_Rate_MultiRAB = WCDMA_PDPContextDeactivateCount_Multi*100/WCDMA_PDPContextActivateCount_Multi
		return WCDMA_PS_retainability_Rate_MultiRAB
	except Exception:
		print "Warning:WCDMA_PDPContextActivateCount_Multi = 0"
		return ''

def WCDMA_PS_retainability_Rate_SingleRAB(Object):
	"""
	return the retainability rate singleRAB
	"""
	try:
		WCDMA_PDPContextDeactivateCount_Single = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_PDPContextDeactivateCount_Single_RAB')))
		WCDMA_PDPContextActivateCount_Single = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_PDPContextActivateCount_Single_RAB')))
		WCDMA_PS_retainability_Rate_SingleRAB = WCDMA_PDPContextDeactivateCount_Single*100/WCDMA_PDPContextActivateCount_Single
		return WCDMA_PS_retainability_Rate_SingleRAB
	except Exception:
		print "Warning:WCDMA_PDPContextActivateCount_Single = 0"
		return ''

def WCDMA_SoftHandover_Failures(Object):
	"""
	Return the soft handover failures
	"""
	try:
		WCDMA_SoftHandover_Attempt = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_SoftHandover_Attempt')))
		WCDMA_SoftHandover_Success = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_SoftHandover_Success')))
		if WCDMA_SoftHandover_Attempt:
			WCDMA_SoftHandover_Failures = WCDMA_SoftHandover_Attempt - WCDMA_SoftHandover_Success
			return WCDMA_SoftHandover_Failures
		else:
			return ''
	except Exception:
		print 'warning:WCDMA_SoftHandover_Attempt is zero'

def WCDMA_Soft_Handover_success_rate(Object):
	"""
	Return The Soft Handover success rate
	"""
	try:
		WCDMA_SoftHandover_Attempt = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_SoftHandover_Attempt')))
		WCDMA_SoftHandover_Success = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_SoftHandover_Success')))
		WCDMA_SoftHandover_success_rate = WCDMA_SoftHandover_Success*100/WCDMA_SoftHandover_Attempt
		return WCDMA_SoftHandover_success_rate
	except Exception:
		print "Warning:WCDMA_SoftHandover_Attempt = 0"
		return ''

def WCDMA_Inter_Frequency_Handover_Failures(Object):
	"""
	Return the Inter Frequency Handover Failures
	"""
	try:
		Wcdma_Inter_Freq_Handover_Attempt_Count = int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Inter_Freq_Handover_Attempt_Count')))
		Wcdma_Inter_Freq_Handover_Success_Count = int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Inter_Freq_Handover_Success_Count')))
		if Wcdma_Inter_Freq_Handover_Attempt_Count:
			Wcdma_Inter_Freq_Handover_Failures = Wcdma_Inter_Freq_Handover_Attempt_Count - Wcdma_Inter_Freq_Handover_Success_Count
			return Wcdma_Inter_Freq_Handover_Failures
		else:
			return ''
	except Exception:
		print 'Warning:Wcdma_Inter_Freq_Handover_Attempt_Count counter is empty'

def WCDMA_Inter_Frequency_Handover_success_rate(Object):
	"""
	Return the Inter Frequency Handover success rate
	"""

	try:
		Wcdma_Inter_Freq_Handover_Attempt_Count = int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Inter_Freq_Handover_Attempt_Count')))
		Wcdma_Inter_Freq_Handover_Success_Count = int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Inter_Freq_Handover_Success_Count')))
		Wcdma_Inter_Freq_Handover_Success_rate = Wcdma_Inter_Freq_Handover_Success_Count*100/Wcdma_Inter_Freq_Handover_Attempt_Count
		return Wcdma_Inter_Freq_Handover_Success_rate
	except Exception:
		print "Warning:Wcdma_Inter_Freq_Handover_Attempt_Count = 0"
		return ''

def WCDMA_Intra_Frequency_Handover_Failures(Object):
	"""
	return the Intra Frequency Handover Failures
	"""
	try:
		Wcdma_Intra_Freq_Handover_Attempt_Count = int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Intra_Freq_Handover_Attempt_Count')))
		Wcdma_Intra_Freq_Handover_Success_Count = int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Intra_Freq_Handover_Success_Count')))
		if Wcdma_Intra_Freq_Handover_Attempt_Count:
			Wcdma_Intra_Freq_Handover_Failures = Wcdma_Intra_Freq_Handover_Attempt_Count - Wcdma_Intra_Freq_Handover_Success_Count
			return Wcdma_Intra_Freq_Handover_Failures
		else:
			return ''
	except Exception:
		print 'Warning:Wcdma_Inter_Freq_Handover_Attempt_Count counter is empty'

def WCDMA_Intra_Frequency_Handover_success_rate(Object):
	"""
	return the Intra Frequency Handover success rate
	"""
	try:
		Wcdma_Intra_Freq_Handover_Attempt_Count = int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Intra_Freq_Handover_Attempt_Count')))
		Wcdma_Intra_Freq_Handover_Success_Count = int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Intra_Freq_Handover_Success_Count')))
		Wcdma_Intra_Freq_Handover_Success_rate = Wcdma_Intra_Freq_Handover_Success_Count*100/Wcdma_Intra_Freq_Handover_Attempt_Count
		return Wcdma_Intra_Freq_Handover_Success_rate
	except Exception:
		print "Warning:Wcdma_Intra_Freq_Handover_Attempt_Count = 0"
		return ''


def Local_time():
	"""
	return the the current time of the system
	"""
	localtime = time.asctime(time.localtime(time.time()))
	return localtime
	
def main(argv):
	'''This gets the argument from terminal in format python filename.py -i inputfolder'''
	inputstring = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o",["ifile=","ofile="])
	except getopt.GetoptError:
		print "invalid input type input format python filename.py -i inputfolder"
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-i","--ifile"):
			inputstring = arg
		else:
			print "invalid input type input format python filename.py -i inputfolder"
	#Getting path of the csv files
	GSMWCDMACOUNTERFILE = GSM_WCDMA_COUNTER_FILE_PATH(inputstring)
	GSMWCDMAKPIFILE = GSM_WCDMA_KPI_FILE_PATH(inputstring)
	#Creating object from the file path after uncompressing it from gzip format
	GSM_WCDMA_COUNTER_FILE = gzip.open(GSMWCDMACOUNTERFILE,'rb')
	GSM_WCDMA_KPI_FILE = gzip.open(GSMWCDMAKPIFILE,'rb')
	GSM_WCDMA_COUNTER_OBJECT = ParseCSV(GSM_WCDMA_COUNTER_FILE)
	GSM_WCDMA_KPI_OBJECT = ParseCSV(GSM_WCDMA_KPI_FILE)
	#This gives a list containing float integers representing the time spend in GSM and WCDMA in format (GSM_TIME,WCDMA_TIME)
	Dict_of_time_in_technologies = Time_Calculation_GSM_WCDMA.Calculate_Time_Technology(GSM_WCDMA_COUNTER_OBJECT)
	#Getting path of outputfile and then creating object and then writing to it
	outputfile = output_file_path(inputstring)
	output_File = gzip.open(outputfile,"wb")
	writer = csv.writer(output_File, delimiter=',')
	#writing to the csv outputfile
	writer.writerow(['Time_Stamp']+['WCDMA_PS_Setup_success_rate']+['WCDMA_PS_retainability_Rate_MultiRAB']+['WCDMA_PS_retainability_Rate_SingleRAB']+['WCDMA_CS_MO_Single_RAB_Mean_Call_Connect_Time']+['WCDMA_CS_MO_Multi_RAB_Mean_Call_Connect_Time']+['WCDMA_CS_MT_Access_Mean_Call_Connect_Time']+['WCDMA_SoftHandover_Failures']+['WCDMA_Soft_Handover_success_rate']+['WCDMA_Inter_Frequency_Handover_Failures']+['WCDMA_Inter_Frequency_Handover_success_rate']+['WCDMA_Intra_Frequency_Handover_Failures']+['WCDMA_Intra_Frequency_Handover_success_rate']+['WCDMA_RACH_Failures']+['WCDMA_RACH_Failure_Rate']+['Time_between_handover']+['Time_between_Inter_frequency_handover']+['Time_between_Hard_Intra_frequency_handover']+['CS_Transmit_Power_Count']+['CS_Transmit_Power_Average']+['PS_Transmit_Power_Count']+['PS_Transmit_Power_Average']+['CS_EcIo_Count']+['CS_EcIo_Average']+['PS_EcIo_Count']+['PS_EcIo_Average'])
	writer.writerow([Local_time()]+[WCDMA_PS_Setup_success_rate(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_PS_retainability_Rate_MultiRAB(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_PS_retainability_Rate_SingleRAB(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_CS_MO_Single_RAB_Mean_Call_Connect_Time(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_CS_MO_Multi_RAB_Mean_Call_Connect_Time(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_CS_MT_Access_Mean_Call_Connect_Time(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_SoftHandover_Failures(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_Soft_Handover_success_rate(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_Inter_Frequency_Handover_Failures(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_Inter_Frequency_Handover_success_rate(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_Intra_Frequency_Handover_Failures(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_Intra_Frequency_Handover_success_rate(GSM_WCDMA_COUNTER_OBJECT)]+[RACH_FAILURE_WCDMA(GSM_WCDMA_COUNTER_OBJECT)]+[RACH_Failure_Rate_WCDMA(GSM_WCDMA_COUNTER_OBJECT)]+[Time_between_handover_WCDMA(GSM_WCDMA_COUNTER_OBJECT,Dict_of_time_in_technologies)]+[Time_between_Inter_frequency_handover(GSM_WCDMA_COUNTER_OBJECT,Dict_of_time_in_technologies)]+[Time_between_Hard_Intra_frequency_handover(GSM_WCDMA_COUNTER_OBJECT,Dict_of_time_in_technologies)]+[CS_Transmit_Power_Count(GSM_WCDMA_KPI_OBJECT)]+[CS_Transmit_Power_Average(GSM_WCDMA_KPI_OBJECT)]+[PS_Transmit_Power_Count(GSM_WCDMA_KPI_OBJECT)]+[PS_Transmit_Power_Average(GSM_WCDMA_KPI_OBJECT)]+[CS_EcIo_Count(GSM_WCDMA_KPI_OBJECT)]+[CS_EcIo_Average(GSM_WCDMA_KPI_OBJECT)]+[PS_EcIo_Count(GSM_WCDMA_KPI_OBJECT)]+[PS_EcIo_Average(GSM_WCDMA_KPI_OBJECT)])
	output_File.close()


main(sys.argv[1:])
