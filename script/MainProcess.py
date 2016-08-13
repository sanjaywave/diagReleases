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
import logging

#logging.basicConfig(filename='Documents/MainProcess_py.log',level=logging.DEBUG)

#########################################################################Various Calculaiton################################
def dropCountCalculator(AttemptString,SuccessString,Object):
	try:
		Attempts = int(Object.getLastValue(Object.getColumnIndexByName(AttemptString)))
		Success = int(Object.getLastValue(Object.getColumnIndexByName(SuccessString)))
		if (Attempts!=0):
			DropsCount = Attempts - Success
			return DropsCount
		else:
			logging.warning(AttemptString + '= 0')
			return ''
	except Exception:
		logging.warning(AttemptString + ' is Empty or non integer value')
		return ''

def successRateCalculator(AttemptString,SuccessString,Object):
	try:
		Attempts = int(Object.getLastValue(Object.getColumnIndexByName(AttemptString)))
		Success = int(Object.getLastValue(Object.getColumnIndexByName(SuccessString)))
		SuccessRate = Success*100.0/Attempts
		return SuccessRate
	except Exception:
		logging.warning(AttemptString + '= 0')
		return ''

def percantageCalculator(AttemptStringOne,AttemptStringTwo,SuccessStringOne,SuccessStringTwo,Object):
	try:
		SuccessCountFirst = int(Object.getLastValue(Object.getColumnIndexByName(SuccessStringOne)))
		SuccessCountSecond = int(Object.getLastValue(Object.getColumnIndexByName(SuccessStringTwo)))
		AttemptConutFirst = int(Object.getLastValue(Object.getColumnIndexByName(AttemptStringOne)))
		AttemptConutSecond = int(Object.getLastValue(Object.getColumnIndexByName(AttemptStringTwo)))
		SuccessRate = (SuccessCountFirst+SuccessCountSecond)*100.0/(AttemptConutFirst+AttemptConutSecond)
		return SuccessRate
	except Exception:
		logging.warning(AttemptStringOne+'+'+AttemptStringTwo+'= 0')
		return ''

def medianCalculator(inputList):
	inputList = map(float, inputList)
	inputList.sort()
	numOfElem = len(inputList)
	if (numOfElem==0):
		print 'Warning:pased array is empty while calculating Median'
		return ''
	else:
		if (numOfElem%2 == 0.00):
			Median = (inputList[numOfElem/2 - 1] + inputList[numOfElem/2])/2
		else:
			Median = (inputList[numOfElem/2])
		return Median

###############################################################Extracting the important data from KPI files######################
def SHORT_WCDMA_GSM_KPI_FILE(inputstring,testfileid):
	GSMWCDMAKPIFILE = GSM_WCDMA_KPI_FILE_PATH(inputstring,testfileid)
	#commandstring = 'gunzip '+GSMWCDMAKPIFILE
	#os.system(commandstring)
	#GSMWCDMAKPIFILE = GSMWCDMAKPIFILE[0:-3]
	#csvfile = open(GSMWCDMAKPIFILE,'rb')
	csvfile = gzip.open(GSMWCDMAKPIFILE,"rb")
	csv_file = csv.reader(csvfile, delimiter=',')
	FirstLine = next(csv_file)
	outputfile = inputstring+'temp.csv.gz'
	output_File = gzip.open(outputfile,"wb")
	writer = csv.writer(output_File, delimiter=',')
	Dictionary_Of_Index = {'WCDMA_CS_MOCALL_SINGLE_RAB_CONNECT_TIME ':0,'WCDMA_CS_MOCALL_MULTIPLE_RAB_CONNECT_TIME ':0,'WCDMA_CS_MTCALL_SINGLE_RAB_CONNECT_TIME ':0, 'WCDMA_CS_MTCALL_MULTI_RAB_CONNECT_TIME ':0,' WCDMA_Tx_Power_CS ':0,'WCDMA_Tx_Power_PS ':0,' WCDMA_Adjusted_Closed_Loop_Power ':0,' WCDMA_ECIO_CS':0,' WCDMA_ECIO_PS':0,'WCDMA_Last_Preamble_Tx_Power ':0,'WCDMA_Time_To_First_Byte ':0,' WCDMA_RRC_STATE ':0,'Date ':0,'WCDMA_RRC_Setup_Time_Duration ':0,'WCDMA_PS_CONNECTED_TIME ':0}
	List_Of_Dic_elem = Dictionary_Of_Index.keys()
	for elem in List_Of_Dic_elem:
		Dictionary_Of_Index[elem] = FirstLine.index(elem)
	writer.writerow(List_Of_Dic_elem)
	List_Of_Dic_elem_values = Dictionary_Of_Index.values()
	for elem in csv_file:
		#elem[List_Of_Dic_elem_values[0]],elem[List_Of_Dic_elem_values[1]],elem[List_Of_Dic_elem_values[2]],elem[List_Of_Dic_elem_values[3]],elem[List_Of_Dic_elem_values[4]],elem[List_Of_Dic_elem_values[5]],elem[List_Of_Dic_elem_values[6]],
		writer.writerow([str(elem[List_Of_Dic_elem_values[0]])]+[str(elem[List_Of_Dic_elem_values[1]])]+[str(elem[List_Of_Dic_elem_values[2]])]+[str(elem[List_Of_Dic_elem_values[3]])]+[str(elem[List_Of_Dic_elem_values[4]])]+[str(elem[List_Of_Dic_elem_values[5]])]+[str(elem[List_Of_Dic_elem_values[6]])]+[str(elem[List_Of_Dic_elem_values[7]])]+[str(elem[List_Of_Dic_elem_values[8]])]+[str(elem[List_Of_Dic_elem_values[9]])]+[str(elem[List_Of_Dic_elem_values[10]])]+[str(elem[List_Of_Dic_elem_values[11]])]+[str(elem[List_Of_Dic_elem_values[12]])]+[str(elem[List_Of_Dic_elem_values[13]])]+[str(elem[List_Of_Dic_elem_values[14]])])
	#commandstring = 'gzip'+' '+GSMWCDMAKPIFILE
	#os.system(commandstring)
	return outputfile

def SHORT_LTE_KPI_FILE(inputstring,testfileid):
	LTEKPIFILE = LTE_KPI_FILE_PATH(inputstring,testfileid)
	#commandstring = 'gunzip '+GSMWCDMAKPIFILE
	#os.system(commandstring)
	#GSMWCDMAKPIFILE = GSMWCDMAKPIFILE[0:-3]
	#csvfile = open(GSMWCDMAKPIFILE,'rb')
	csvfile = gzip.open(LTEKPIFILE,"rb")
	csv_file = csv.reader(csvfile, delimiter=',')
	FirstLine = next(csv_file)
	outputfile = inputstring+'temp2.csv.gz'
	output_File = gzip.open(outputfile,"wb")
	writer = csv.writer(output_File, delimiter=',')
	Dictionary_Of_Index = {'Date ':0, ' QAM_Status':0,' UL_Rank_Index ':0,'Resource_Block_Allocated ':0,' PDSCH_Frame_Usage ':0,'PUSCH_Throughput ':0,'PDSCH_Throughput ':0,'RRC State Information ':0,' RLC_DL_Througput ':0,'CSFB_MO_Single_RAB_ConnectTime ':0,'CSFB_MO_Multi_RAB_ConnectTime ':0,'CSFB_MT_Single_RAB_ConnectTime ':0,'CSFB_MT_Multi_RAB_ConnectTime ':0,'LTE_CSFB_Single_RAB_RedirectTime ':0,'LTE_CSFB_Multi_RAB_RedirectTime ':0,'LTE_Data_Interrupt_PS_Only_Single_RAB_Time ':0,'LTE_Data_Interrupt_PS_Only_Multi_RAB_Time ':0,'LTE_Data_Interrupt_With_CSFBMO_Multi_RAB_Time ':0,'LTE_Data_Interrupt_With_CSFBMT_Multi_RAB_Time ':0,'LTE_Time_To_First_Byte ':0,'LTE_RRC_Connection_Setup_Time ':0,'UL_WideBand_CQI_CW[0] ':0,'CSFB_MO_Single_RAB_Increment_ConnectTime ':0,'CSFB_MO_Multi_RAB_Increment_ConnectTime ':0,'CSFB_MT_Single_RAB_Increment_ConnectTime ':0,'CSFB_MT_Multi_RAB_Increment_ConnectTime ':0,'LTE_Data_Interruption_Time_PS_After_ESR_MO ':0,'LTE_Data_Interruption_Time_PS_After_ESR_MT ':0,'LTE_PS_Single_RAB_Connected_Time ':0,'LTE_PS_Connected_Multi_RAB_Connected_Time ':0,'LTE_PS_Only_Multi_RAB_Connected_Time ':0,'LTE_CSFB_PS_Connected_Time_in_WCDMA ':0,'anovaUMTS_LTE_CSFB_Reselect_Duration ':0,' MIMO_Usage':0}
	List_Of_Dic_elem = Dictionary_Of_Index.keys()
	for elem in List_Of_Dic_elem:
#		print "FirstLine.index(elem)", FirstLine.index(elem)
#		print "elem -----", elem
		Dictionary_Of_Index[elem] = FirstLine.index(elem)
	writer.writerow(List_Of_Dic_elem)
	List_Of_Dic_elem_values = Dictionary_Of_Index.values()
#	print "List_Of_Dic_elem_values----- ",List_Of_Dic_elem_values
#	for i in range(0,30):
#		print "List_Of_Dic_elem_values[",i,"]= ",List_Of_Dic_elem_values[i]
#	print "csv_File",csv_file
	for elem in csv_file:
		#elem[List_Of_Dic_elem_values[0]],elem[List_Of_Dic_elem_values[1]],elem[List_Of_Dic_elem_values[2]],elem[List_Of_Dic_elem_values[3]],elem[List_Of_Dic_elem_values[4]],elem[List_Of_Dic_elem_values[5]],elem[List_Of_Dic_elem_values[6]],
		writer.writerow([str(elem[List_Of_Dic_elem_values[0]])]+[str(elem[List_Of_Dic_elem_values[1]])]+[str(elem[List_Of_Dic_elem_values[2]])]+[str(elem[List_Of_Dic_elem_values[3]])]+[str(elem[List_Of_Dic_elem_values[4]])]+[str(elem[List_Of_Dic_elem_values[5]])]+[str(elem[List_Of_Dic_elem_values[6]])]+[str(elem[List_Of_Dic_elem_values[7]])]+[str(elem[List_Of_Dic_elem_values[8]])]+[str(elem[List_Of_Dic_elem_values[9]])]+[str(elem[List_Of_Dic_elem_values[10]])]+[str(elem[List_Of_Dic_elem_values[11]])]+[str(elem[List_Of_Dic_elem_values[12]])]+[str(elem[List_Of_Dic_elem_values[13]])]+[str(elem[List_Of_Dic_elem_values[14]])]+[str(elem[List_Of_Dic_elem_values[15]])]+[str(elem[List_Of_Dic_elem_values[16]])]+[str(elem[List_Of_Dic_elem_values[17]])]+[str(elem[List_Of_Dic_elem_values[18]])]+[str(elem[List_Of_Dic_elem_values[19]])]+[str(elem[List_Of_Dic_elem_values[20]])]+[str(elem[List_Of_Dic_elem_values[21]])]+[str(elem[List_Of_Dic_elem_values[22]])]+[str(elem[List_Of_Dic_elem_values[23]])]+[str(elem[List_Of_Dic_elem_values[24]])]+[str(elem[List_Of_Dic_elem_values[25]])]+[str(elem[List_Of_Dic_elem_values[26]])]+[str(elem[List_Of_Dic_elem_values[27]])]+[str(elem[List_Of_Dic_elem_values[28]])]+[str(elem[List_Of_Dic_elem_values[29]])]+[str(elem[List_Of_Dic_elem_values[30]])]+[str(elem[List_Of_Dic_elem_values[31]])]+[str(elem[List_Of_Dic_elem_values[32]])]+[str(elem[List_Of_Dic_elem_values[33]])])
	#commandstring = 'gzip'+' '+GSMWCDMAKPIFILE
	#os.system(commandstring)
	return outputfile

#############################################################File Path Manupulation by input string###############################

def LTE_KPI_FILE_PATH(inputstring,testfileid):
	LTE_KPI_FILE_PATH = inputstring + 'LTE_KPI/'+testfileid+'.csv.gz'
	LTE_KPI_FILE_PATH = glob.glob(LTE_KPI_FILE_PATH)
	LTE_KPI_FILE_PATH = ''.join(map(str,LTE_KPI_FILE_PATH))
	return LTE_KPI_FILE_PATH

def LTE_COUNTER_FILE_PATH(inputstring,testfileid):
	LTE_COUNTER_FILE_PATH = inputstring + 'LTE_COUNTER/'+testfileid+'.csv.gz'
	LTE_COUNTER_FILE_PATH = glob.glob(LTE_COUNTER_FILE_PATH)
	LTE_COUNTER_FILE_PATH = ''.join(map(str,LTE_COUNTER_FILE_PATH))
	return LTE_COUNTER_FILE_PATH

def GSM_WCDMA_COUNTER_FILE_PATH(inputstring,testfileid):
	"""
	It returns the path of GSM WCDMA COUNTER FILE PATH
	"""
	GSM_WCDMA_COUNTER_FILE_PATH = inputstring + 'GSM_WCDMA_COUNTER/'+ testfileid +'.csv.gz'
	GSM_WCDMA_COUNTER_FILE_PATH = inputstring + 'GSM_WCDMA_COUNTER/'+testfileid+'.csv.gz'
	GSM_WCDMA_COUNTER_FILE_PATH = glob.glob(GSM_WCDMA_COUNTER_FILE_PATH)
	GSM_WCDMA_COUNTER_FILE_PATH = ''.join(map(str,GSM_WCDMA_COUNTER_FILE_PATH))
	return GSM_WCDMA_COUNTER_FILE_PATH

def GSM_WCDMA_KPI_FILE_PATH(inputstring,testfileid):
	"""
	It returns the path of GSM WCDMA KPI FILE PATH
	"""
	GSM_WCDMA_KPI_FILE_PATH = inputstring + 'GSM_WCDMA_KPI/'+ testfileid +'.csv.gz'
	GSM_WCDMA_KPI_FILE_PATH = inputstring + 'GSM_WCDMA_KPI/'+testfileid+'.csv.gz'
	GSM_WCDMA_KPI_FILE_PATH = glob.glob(GSM_WCDMA_KPI_FILE_PATH)
	GSM_WCDMA_KPI_FILE_PATH = ''.join(map(str,GSM_WCDMA_KPI_FILE_PATH))
	return GSM_WCDMA_KPI_FILE_PATH

def L3_Messages_FILE_PATH(inputstring,testfileid):
	"""
	It returns the path of GSM WCDMA KPI FILE PATH
	"""
	L3_Messages_FILE_PATH = inputstring + 'L3Messages/'+testfileid+'.csv.gz'
	L3_Messages_FILE_PATH = glob.glob(L3_Messages_FILE_PATH)
	L3_Messages_FILE_PATH = ''.join(map(str,L3_Messages_FILE_PATH))
	return L3_Messages_FILE_PATH

def output_file_path(inputfile,testfileid):
	"""
	It creates the output folder and returns its path and file name
	"""
#	outputfile = inputfile + 'GSM_WCDMA_COUNT_CALC/'+testfileid+'.csv.gz'
#	outputfile = inputfile + 'GSM_WCDMA_COUNT_CALC/'
	outputdir = inputfile + 'GSM_WCDMA_COUNT_CALC/'
	outputfile = outputdir + testfileid+'.csv.gz'

	if not os.path.exists(outputdir):
		os.makedirs(outputdir)
#	inputfile = GSM_WCDMA_COUNTER_FILE_PATH(inputfile,testfileid)
#	nameOfFile = inputfile.split('/')
#	outputfile = outputfile +'/'+ nameOfFile[-1]
	return outputfile


#########################################################Object = GSM_WCDMA_KPI_OBJECT#################################################
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

def WCDMA_CS_Transmit_Power_Count(Object):
	return Object.getNumOfValuesInColumn(Object.getColumnIndexByName('WCDMA_Tx_Power_CS'))

def WCDMA_CS_Transmit_Power_Average(Object):
	"""
	it returns the average of the CS Transmit Power by formula alpha*current_elem + (1-alpha)*avg
	"""
	CS_Transmit_Power_List = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_Tx_Power_CS'))
	#CS_Transmit_Power_List = filter(None, CS_Transmit_Power_List)
	avg = 0.0
	for elem in CS_Transmit_Power_List:
		elem = 10*float(elem) + 188
		avg = avg + elem
	if len(CS_Transmit_Power_List):
		avg = avg/len(CS_Transmit_Power_List)
		return (avg+512)/10-70
	else:
		return ''

def WCDMA_PS_Transmit_Power_Count(Object):
	return Object.getNumOfValuesInColumn(Object.getColumnIndexByName('WCDMA_Tx_Power_PS'))

def WCDMA_PS_Transmit_Power_Average(Object):
	"""
	it returns the average of the CS Transmit Power by formula alpha*current_elem + (1-alpha)*avg
	"""
	PS_Transmit_Power_List = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_Tx_Power_PS'))
	#PS_Transmit_Power_List = filter(None, PS_Transmit_Power_List)
	avg = 0.0
	for elem in PS_Transmit_Power_List:
		elem = 10*float(elem) + 188
		avg = avg + elem
	if len(PS_Transmit_Power_List):
		avg = avg/len(PS_Transmit_Power_List)
		return (avg+512)/10-70
	else:
		return ''

def WCDMA_CS_EcIo_Count(Object):
	CS_EcIo_List = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_ECIO_CS'))
	return len(CS_EcIo_List)

def antilog(x):
	return 10 ** x

def WCDMA_CS_EcIo_Average(Object):
	"""
	it returns the average of the CS Transmit Power by formula alpha*current_elem + (1-alpha)*avg
	"""
	CS_EcIo_List = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_ECIO_CS'))
	avg = 0.0
	for elem in CS_EcIo_List:
		elem = antilog(float(elem))
		avg = elem + avg
	try:
		avg = avg/len(CS_EcIo_List)
		return math.log10(avg)
	except Exception:
		logging.warning('CS_EcIo_Average is empty')
		return ''



def WCDMA_PS_EcIo_Count(Object):
	PS_EcIo_List = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_ECIO_PS'))
	#PS_EcIo_List = filter(lambda a: a != '0.000000 ', PS_EcIo_List)
	return len(PS_EcIo_List)

def WCDMA_PS_EcIo_Average(Object):
	"""
	it returns the average of the CS Transmit Power by formula alpha*current_elem + (1-alpha)*avg
	"""
	PS_EcIo_List = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_ECIO_PS'))
	#PS_EcIo_List = filter(lambda a: a != '0.000000 ', PS_EcIo_List)
	avg = 0.0
	for elem in PS_EcIo_List:
		elem = antilog(float(elem))
		avg = elem + avg
	try:
		avg = avg/len(PS_EcIo_List)
		return math.log10(avg)
	except Exception:
		logging.warning('PS_EcIo_Average counter is empty')
		return ''

def Median_LTE_Time_To_First_Byte(Object):
	"""
	it returnn the median of the Median_LTE_Time_To_First_Byte
	"""
	try:
		return Object.getMedianValueInColumn(Object.getColumnIndexByName('WCDMA_Time_To_First_Byte'))
	except Exception:
		logging.warning('Error returned while calculating Median in Median_LTE_Time_To_First_Byte')
		return ''

def WCDMA_Median_RRC_Setup_Time(Object):
	try:

		return Object.getMedianValueInColumn(Object.getColumnIndexByName('WCDMA_RRC_Setup_Time_Duration'))
	except Exception:
		logging.warning('Error returned while calculating Median in WCDMA_Median_RRC_Setup_Time')
		return ''
def WCDMA_CS_MTCALL_CONNECT_TIME(Object):
	a = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_CS_MTCALL_MULTI_RAB_CONNECT_TIME'))
	b = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_CS_MTCALL_SINGLE_RAB_CONNECT_TIME'))
	colList = a+b
	return colList	
	
def Total_Time_List_WCDMA_CS_Connect_Time(Object):
	a = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_CS_MOCALL_SINGLE_RAB_CONNECT_TIME'))
	b = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('WCDMA_CS_MOCALL_MULTIPLE_RAB_CONNECT_TIME'))
	wcdma_cs = WCDMA_CS_MTCALL_CONNECT_TIME(Object)
	colList = a+b+ wcdma_cs
	return colList	


def Total_WCDMA_CS_Mean_Call_Connect_Time(Object):		
	try:
		colList =  Total_Time_List_WCDMA_CS_Connect_Time(Object)
		colList = filter(None, colList)
		colList = filter(lambda a: a != ' ', colList)
		colList = map(float, colList)
		avg = sum(colList)/len(colList)
		return avg
	except Exception:
		logging.warning('some error in Total_WCDMA_CS_Mean_Call_Connect_Time')
		return ''

def Last_Preamble_Tx_Power_Avg(Object):
	try:
		avg = Object.getAverageValueInColumn(Object.getColumnIndexByName('WCDMA_Last_Preamble_Tx_Power'))
		return avg
	except Exception:
		logging.warning('some error in Last_Preamble_Tx_Power_Avg')
		return ''


def WCDMA_Adjusted_Closed_Loop_Power_Avg(Object):
	try:
		avg = Object.getAverageValueInColumn(Object.getColumnIndexByName('WCDMA_Adjusted_Closed_Loop_Power'))
		return avg
	except Exception:
		logging.warning('some error in WCDMA_Adjusted_Closed_Loop_Power_Avg')
		return ''


###################################Object = GSM_WCDMA_COUNTER_FILE############################################################
def RACH_Success_WCDMA(Object):
	try:
		WCDMA_Rach_Success_Count = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_Rach_Success_Count')))
		return WCDMA_Rach_Success_Count
	except Exception:
		logging.warning('Warning:RACH_Success_WCDMA counter is empty')
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
		logging.warning('WCDMA_Rach_Total_Count counter is empty')
		return ''

def RACH_Failure_Rate_WCDMA(Object):
	try:
		WCDMA_Rach_Total_Count = float(Object.getLastValue(Object.getColumnIndexByName('WCDMA_Rach_Total_Count')))
		RACH_Failure_Rate_WCDMA = RACH_FAILURE_WCDMA(Object)*100/(WCDMA_Rach_Total_Count)
		return RACH_Failure_Rate_WCDMA
	except Exception:
		logging.warning('WCDMA_Rach_Total_Count counter is empty')
		return ''

'''   #commented becoz implemented by using RRC connected state

def WCDMA_Time_between_soft_handover(Object,Dict_of_time_in_technologies_L3Messages):
	"""
	return the Time between soft handovers in WCDMA
	"""
	try:
		Time_between_handover_WCDMA = Dict_of_time_in_technologies_L3Messages['WCDMA']/int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_SoftHandover_Success')))
		return Time_between_handover_WCDMA
	except Exception:
		logging.warning('WCDMA_SoftHandover_Success = 0')
		return ''

def WCDMA_Time_between_Inter_frequency_handover(Object,Dict_of_time_in_technologies_L3Messages):
	"""
	return the Time between Inter Frequency handovers in WCDMA
	"""
	try:
		Time_between_Inter_frequency_handover = Dict_of_time_in_technologies_L3Messages['WCDMA']/(int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Inter_Freq_Handover_Success_Count')))*60)
		return Time_between_Inter_frequency_handover
	except Exception:
		logging.warning("Wcdma_Inter_Freq_Handover_Success_Count = 0")
		return ''

def WCDMA_Time_between_Hard_Intra_frequency_handover(Object,Dict_of_time_in_technologies_L3Messages):
	"""
	return the Time between hard intra Frequency handovers in WCDMA
	"""
	try:
		Time_between_Hard_Intra_frequency_handover = Dict_of_time_in_technologies_L3Messages['WCDMA']/(int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Intra_Freq_Handover_Success_Count')))*60)
		return Time_between_Hard_Intra_frequency_handover
	except Exception:
		logging.warning('Wcdma_Intra_Freq_Handover_Success_Count = 0')
		return ''
'''
# this Times are only for CELL_DCH state so 3 is passed 3:CELL_DCH

def WCDMA_Time_Between_Hard_Intra_Frequency_Handover_Second(Object,Calculate_Time_RRC_State_From_WCDMA_KPI_FILE):
	try:
		return Calculate_Time_RRC_State_From_WCDMA_KPI_FILE['3']/int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Intra_Freq_Handover_Success_Count')))
	except Exception:
		logging.warning('error in WCDMA_Time_Between_Hard_Intra_Frequency_Handover_Second')
		return ''


def WCDMA_Time_Between_Inter_Frequency_Handover_Second(Object,Calculate_Time_RRC_State_From_WCDMA_KPI_FILE):
	try:
		return Calculate_Time_RRC_State_From_WCDMA_KPI_FILE['3']/int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Inter_Freq_Handover_Success_Count')))
	except Exception:
		logging.warning('error in WCDMA_Time_Between_Hard_Inter_Frequency_Handover_Second')
		return ''

def WCDMA_Time_Between_Soft_Handover_Second(Object,Calculate_Time_RRC_State_From_WCDMA_KPI_FILE):
	try:
		return Calculate_Time_RRC_State_From_WCDMA_KPI_FILE['3']/int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_SoftHandover_Success')))
	except Exception:
		logging.warning('error in WCDMA_Time_Between_Soft_Handover_Second')
		return ''



def WCDMA_PS_Setup_success_rate_SingleRAB(Object):  #WCDMA_PS_Accessibility_Single_RAB
	return successRateCalculator('anovaWCDMA_PS_SingleRAB_AttemptCount','anovaWCDMA_PS_SingleRAB_SuccessCount',Object)

def WCDMA_PS_Setup_success_rate_MultiRAB(Object):    #WCDMA_PS_Accessibility_Multi_RAB
	return successRateCalculator('anovaWCDMA_PS_MultiRAB_AttemptCount','anovaWCDMA_PS_MultiRAB_SuccessCount',Object)

def PS_After_ESR_MO_Accessibility_in_WCDMA(Object): 
	return successRateCalculator('LTE_PS_After_ESR_MO_in_WCDMA_Attempt_Count','LTE_PS_After_ESR_MO_in_WCDMA_Attempt_Count',Object)
def PS_After_ESR_MT_Accessibility_in_WCDMA(Object): 
	return successRateCalculator('LTE_PS_After_ESR_MT_in_WCDMA_Attempt_Count','LTE_PS_After_ESR_MT_in_WCDMA_Attempt_Count',Object)

def PS_With_CSFB_MO_Accessibility_in_WCDMA(Object): 
	return successRateCalculator('PS_with_CSFB_MO_Attempt_in_WCDMA_Count','PS_With_CSFBMO_SuccessCount',Object)
def PS_With_CSFB_MT_Accessibility_in_WCDMA(Object): 
	return successRateCalculator('PS_with_CSFB_MT_Attempt_in_WCDMA_Count','PS_With_CSFBMT_SuccessCount',Object)

def WCDMA_PS_Accessibility_Total(ObjectWCDMA,ObjectLTE):
	try:
		attempt_single = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_PS_SingleRAB_AttemptCount')))
		ps_success_single = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_PS_SingleRAB_SuccessCount')))
		attempt_multi = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_PS_MultiRAB_AttemptCount')))
		ps_success_multi = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_PS_MultiRAB_SuccessCount')))
		success = LTE_CSFB_Success_total(ObjectLTE)
			
		a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('PS_with_CSFB_MO_Attempt_in_WCDMA_Count')))
		b = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('PS_with_CSFB_MT_Attempt_in_WCDMA_Count')))
		c = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('LTE_PS_After_ESR_MO_in_WCDMA_Attempt_Count')))
		d = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('LTE_PS_After_ESR_MT_in_WCDMA_Attempt_Count')))
		attempt = a+b+c+d +attempt_single+attempt_multi
		return (ps_success_single+ps_success_multi+success)*100.0/attempt
	except Exception:
		logging.warning('Error While calculatiing WCDMA_PS_Accessibility_Total denominator zero')
		return ''

'''
// To be implented in more optimized way

def WCDMA_PS_Drop_Count(object):
	try:
		ps_release_count_single = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_PS_SingleRAB_SuccessfulReleaseCount')))
		ps_success_count_single = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_PS_SingleRAB_SuccessCount')))
		WCDMA_PS_Drop_Count = ps_success_count_single - ps_release_count_single
		return WCDMA_PS_Drop_Count
	except Exception:
		logging.warning("Warning:anovaWCDMA_PS_SingleRAB_AttemptCount = 0")
		return ''
'''
def WCDMA_PS_Only_Retainability_MultiRAB(Object):
	return successRateCalculator('anovaWCDMA_PS_MultiRAB_SuccessCount','anovaWCDMA_PS_MultiRAB_SuccessfulReleaseCount',Object)

def WCDMA_PS_Only_Retainability_SingleRAB(Object):
	"""
	return the retainability rate singleRAB
	"""
	return successRateCalculator('anovaWCDMA_PS_SingleRAB_SuccessCount','anovaWCDMA_PS_SingleRAB_SuccessfulReleaseCount',Object)

def WCDMA_Only_PS_Retainability_Total(Object):
	"""
	return  WCDMA_Only_PS_Retainability_Total
	"""
	return percantageCalculator('anovaWCDMA_PS_MultiRAB_SuccessCount','anovaWCDMA_PS_SingleRAB_SuccessCount','anovaWCDMA_PS_MultiRAB_SuccessfulReleaseCount','anovaWCDMA_PS_SingleRAB_SuccessfulReleaseCount',Object)

def WCDMA_SoftHandover_Failures(Object):
	"""
	Return the soft handover failures
	"""
	return dropCountCalculator('WCDMA_SoftHandover_Attempt','WCDMA_SoftHandover_Success',Object)
def WCDMA_Soft_Handover_success_rate(Object):
	"""
	Return The Soft Handover success rate
	"""
	return successRateCalculator('WCDMA_SoftHandover_Attempt','WCDMA_SoftHandover_Success',Object)

def WCDMA_Inter_Frequency_Handover_Failures(Object):
	"""
	Return the Inter Frequency Handover Failures
	"""
	return dropCountCalculator('Wcdma_Inter_Freq_Handover_Attempt_Count','Wcdma_Inter_Freq_Handover_Success_Count',Object)

def WCDMA_Inter_Frequency_Handover_success_rate(Object):
	"""
	Return the Inter Frequency Handover success rate
	"""
	return successRateCalculator('Wcdma_Inter_Freq_Handover_Attempt_Count','Wcdma_Inter_Freq_Handover_Success_Count',Object)

def WCDMA_Intra_Frequency_Handover_Failures(Object):
	"""
	return the Intra Frequency Handover Failures
	"""
	return dropCountCalculator('Wcdma_Intra_Freq_Handover_Attempt_Count','Wcdma_Intra_Freq_Handover_Success_Count',Object)

def WCDMA_Intra_Frequency_Handover_success_rate(Object):
	"""
	return the Intra Frequency Handover success rate
	"""
	return successRateCalculator('Wcdma_Intra_Freq_Handover_Attempt_Count','Wcdma_Intra_Freq_Handover_Success_Count',Object)

def WCDMA_CS_Accessibility_Single_RAB_MO(Object):
	return successRateCalculator('anovaWCDMA_CSMO_SingleRAB_AttemptCount','anovaWCDMA_CSMO_SingleRAB_SuccessCount',Object)

def WCDMA_CS_Accessibility_Single_RAB_MT(Object):
	return successRateCalculator('anovaWCDMA_CSMT_SingleRAB_AttemptCount','anovaWCDMA_CSMT_SingleRAB_SuccessCount',Object)

def WCDMA_CS_Accessibility_Multi_RAB_MO(Object):
	return successRateCalculator('anovaWCDMA_CSMO_MultiRAB_AttemptCount','anovaWCDMA_CSMO_MultiRAB_SuccessCount',Object)

def WCDMA_CS_Accessibility_Multi_RAB_MT(Object):
	return successRateCalculator('anovaWCDMA_CSMT_MultiRAB_AttemptCount','anovaWCDMA_CSMT_MultiRAB_SuccessCount',Object)

def Total_WCDMA_CS_AlertCount(Object):
		a = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_SuccessCount')))
		b = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_CSMT_SingleRAB_SuccessCount')))
		c = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_CSMO_MultiRAB_SuccessCount')))
		d = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_CSMT_MultiRAB_SuccessCount')))
		total = a + b+c+d	
		return total

def Total_WCDMA_CM(Object):
		e = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_AttemptCount')))
		f = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_CSMT_SingleRAB_AttemptCount')))
		j = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_CSMO_MultiRAB_AttemptCount')))
		k = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_CSMT_MultiRAB_AttemptCount')))
		total = e+f+j+k
		return total
		
def WCDMA_CS_Accessibility_Total(Object):
	try:
		CS_Alert_total= Total_WCDMA_CS_AlertCount(Object)
		CM_ServReq_Setup= Total_WCDMA_CM(Object)
		
		return CS_Alert_total*100.0/CM_ServReq_Setup
	except Exception:
		logging.warning('denominator zero in WCDMA_CS_Accessibility_Total program')
		return ''

def WCDMA_CS_Retainability_Single_RAB_MO(Object):
	return successRateCalculator('anovaWCDMA_CSMO_SingleRAB_SuccessCount','anovaWCDMA_CSMO_SingleRAB_SuccessfulReleaseCount',Object)

def WCDMA_CS_Retainability_Multi_RAB_MO(Object):
	return successRateCalculator('anovaWCDMA_CSMO_MultiRAB_SuccessCount','WCDMA_CS_MO_DisconnectCount_Multi_RAB',Object)

def WCDMA_CS_Retainability_Single_RAB_MT(Object):
	return successRateCalculator('anovaWCDMA_CSMT_SingleRAB_SuccessCount','WCDMA_CS_MT_DisconnectCount_Single_RAB',Object)

def WCDMA_CS_Retainability_Multi_RAB_MT(Object):
	return successRateCalculator('anovaWCDMA_CSMT_MultiRAB_SuccessCount','WCDMA_CS_MT_DisconnectCount_Multi_RAB',Object)

def Overall_WCDMA_CS_Disconnect(Object):
		e = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_SuccessfulReleaseCount')))
		f = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_CS_MO_DisconnectCount_Multi_RAB')))
		j = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_CS_MT_DisconnectCount_Single_RAB')))
		k = int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_CS_MT_DisconnectCount_Multi_RAB')))
		total = e+f+j+k
		return total
def WCDMA_CS_Retainability_Total(Object):
	try:
		CS_Alert_total= Total_WCDMA_CS_AlertCount(Object)
		CS_Disconnect_total= Overall_WCDMA_CS_Disconnect(Object)
		return CS_Disconnect_total*100.0/CS_Alert_total
	except Exception:
		logging.warning('denominator zero in WCDMA_CS_Retainability_Total program')
		return ''

def WCDMA_Network_Attach_Success_Rate(Object):
	return successRateCalculator('WCDMA_Attach_RequestCount','WCDMA_Attach_CompleteCount',Object)

def WCDMA_LAU_Success_Rate(Object):
	return successRateCalculator('WCDMA_Location_Area_Update_RequestCount','WCDMA_Location_Area_Update_AcceptCount',Object)

def WCDMA_Minutes_Per_RRC_Drop(Object,Calculate_Time_RRC_State_From_WCDMA_KPI_FILE):
	try:
		drop_Count = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_RRC_DropCount')))
		return Calculate_Time_RRC_State_From_WCDMA_KPI_FILE['3']/(drop_Count*60)
	except Exception:
		logging.warning('Error in WCDMA_Minutes_Per_RRC_Drop')
		return ''

def WCDMA_Only_Minutes_Per_PS_Drop(Object,Calculate_Time_RRC_State_From_WCDMA_KPI_FILE):
	try:
		a = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_PS_Single_RAB_Drop')))
		b = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_PS_Multi_RAB_Drop')))
		return Calculate_Time_RRC_State_From_WCDMA_KPI_FILE['3']/((a+b)*60)   #output in minutes
	except Exception:
		logging.warning('Error in WCDMA_Only_Minutes_Per_PS_Drop')
		return ''
def drop_total_WCDMA_LTE(ObjectWCDMA,ObjectLTE):
		a = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_PS_Single_RAB_Drop')))
		b = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_PS_Multi_RAB_Drop')))
		c = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('LTE_PS_Drop_with_CSFB_MO_in_WCDMA')))
		d = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('LTE_PS_Drop_with_CSFB_MT_in_WCDMA')))
		e = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('LTE_PS_After_ESR_MO_in_WCDMA_Drop_Count')))
		f = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('LTE_PS_After_ESR_MT_in_WCDMA_Drop_Count')))
		ret = a + b + c + d + e + f
		return ret


def Total_WCDMA_Minutes_Per_Drop(ObjectWCDMA,ObjectLTE, Calculate_Time_RRC_State_From_WCDMA_KPI_FILE):
	try: 
		drop = drop_total_WCDMA_LTE(ObjectWCDMA,ObjectLTE)
		return Calculate_Time_RRC_State_From_WCDMA_KPI_FILE['3']/(drop*60)
	except Exception:
		logging.warning('Denominator Error in Total_WCDMA_Minutes_Per_Drop')
def Overall_Minutes_Per_Drop(ObjectWCDMA,ObjectLTE, Calculate_Time_RRC_State_From_WCDMA_KPI_FILE,Calculate_Time_RRC_State):
	try: 
		drop = drop_total_WCDMA_LTE(ObjectWCDMA,ObjectLTE)
		a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('LTE_RRC_Drop_Count')))
		return (Calculate_Time_RRC_State_From_WCDMA_KPI_FILE['3']+Calculate_Time_RRC_State)/((drop + a)*60)
	except Exception:
		logging.warning('Denominator Error in Overall_Minutes_Per_Drop')

def Normalized_PS_Retainability_Rate(ObjectWCDMA_C, ObjectWCDMA_K, ObjectLTE_C, ObjectLTE_K, Calculate_Time_RRC_State):
	try:
		drop1 = drop_total_WCDMA_LTE(ObjectWCDMA_C,ObjectLTE_C)

		drop2 = LTE_RRC_Drop_Count(ObjectLTE_C)
		time_sum = LTE_CSFB_and_WCDMA_PS_Connected_Time(ObjectWCDMA_K,ObjectLTE_K)
		result = (drop1 + drop2)/((time_sum + Calculate_Time_RRC_State)/60.0)   # here time is in min

		return (1-result)
	except Exception:
		logging.warning('Denominator Error in Overall_Minutes_Per_Drop')



def UMTS_To_LTE_Redirection_Success_Rate(Object):
	return successRateCalculator('UMTS_LTE_Redirect_PS_AttemptCount','UMTS_LTE_Redirect_PS_SuccessCount',Object)

def WCDMA_Time_Between_Hard_Intra_Frequency_HO(Object,Calculate_Time_RRC_State_From_WCDMA_KPI_FILE):
	try:
		return Calculate_Time_RRC_State_From_WCDMA_KPI_FILE['RRC_Connected']/int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Intra_Freq_Handover_Success_Count')))
	except Exception:
		logging.warning('error in WCDMA_Time_Between_Hard_Intra_Frequency_HO')
		return ''


def WCDMA_Time_Between_Hard_Inter_Frequency_HO(Object,Calculate_Time_RRC_State_From_WCDMA_KPI_FILE):
	try:
		return Calculate_Time_RRC_State_From_WCDMA_KPI_FILE['RRC_Connected']/int(Object.getLastValue(Object.getColumnIndexByName('Wcdma_Inter_Freq_Handover_Success_Count')))
	except Exception:
		logging.warning('error in WCDMA_Time_Between_Hard_Inter_Frequency_HO')
		return ''

def WCDMA_Time_Between_Soft_HO(Object,Calculate_Time_RRC_State_From_WCDMA_KPI_FILE):
	try:
		return Calculate_Time_RRC_State_From_WCDMA_KPI_FILE['RRC_Connected']/int(Object.getLastValue(Object.getColumnIndexByName('WCDMA_SoftHandover_Success')))
	except Exception:
		logging.warning('error in WCDMA_Time_Between_Soft_HO')
		return ''

def WCDMA_RRC_Connection_Success_Rate(Object):
	return successRateCalculator('WCDMA_RRC_Conn_Request_Count','WCDMA_RRC_Conn_Setup_Complete_Count',Object)

def Total_CSFB_PS_in_WCDMA_Attempt(Object):     #by zahid
	try:
		a = int(Object.getLastValue(Object.getColumnIndexByName('PS_with_CSFB_MO_Attempt_in_WCDMA_Count')))
		b = int(Object.getLastValue(Object.getColumnIndexByName('PS_with_CSFB_MT_Attempt_in_WCDMA_Count')))
		c = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_After_ESR_MO_in_WCDMA_Attempt_Count')))
		d = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_After_ESR_MT_in_WCDMA_Attempt_Count')))
		return (a+b+c+d)
	except Exception:
		logging.warning('error in Total_CSFB_PS_in_WCDMA_Attempt')
		return ''
def Total_CSFB_PS_in_WCDMA_Connection_Count(Object):  
	try:
		a =  PS_With_CSFB_Success(Object)
		c = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_After_ESR_MO_in_WCDMA_Success_Count')))
		d = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_After_ESR_MT_in_WCDMA_Success_Count')))
#		print" Total_CSFB_PS_in_WCDMA  a=%d b=%d c=%d"%(a,b,c,d)	
		return (a+c+d)
	except Exception:
		logging.warning('error in Total_CSFB_PS_in_WCDMA_Connection_Count')
		return ''
def Total_WCDMA_Only_PS_Attempt(Object):     
	try:
		attempt_count_single = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_PS_SingleRAB_AttemptCount')))
		attempt_count_multi = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_PS_MultiRAB_AttemptCount')))
		return (attempt_count_single + attempt_count_multi)
	except Exception:
		logging.warning('error in Total_WCDMA_Only_PS_Attempt')
		return ''
def Total_PS_WCDMA_Only_Count(Object):     
	try:
		single = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_PS_SingleRAB_SuccessCount')))
		multi = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_PS_MultiRAB_SuccessCount')))
#		print "Total_PS_WCDMA_Only_Count single = %d multi = %d"%(single, multi)
		return (single + multi)
	except Exception:
		logging.warning('error in Total_PS_WCDMA_Only_Count')
		return ''
def Total_PS_WCDMA_Only_Release_Count(ObjectOne):     
	try:
		single = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_PS_SingleRAB_SuccessfulReleaseCount')))
		multi = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_PS_MultiRAB_SuccessfulReleaseCount')))
		return (single + multi)
	except Exception:
		logging.warning('error in Total_PS_WCDMA_Only_Release_Count')
		return ''
def Total_WCDMA_PS_Attempts(ObjectWCDMA, ObjectLTE):     
	try:
		CSFB_attempt = Total_CSFB_PS_in_WCDMA_Attempt(ObjectLTE)
		WCDMA_attempt = Total_WCDMA_Only_PS_Attempt(ObjectWCDMA)
		return (CSFB_attempt+WCDMA_attempt)
	except Exception:
		logging.warning('error in Total_WCDMA_PS_Attempts')
		return ''

def Total_WCDMA_PS_Connection_Count(ObjectWCDMA, ObjectLTE):
	try:
		a = Total_PS_WCDMA_Only_Count(ObjectWCDMA)
		b = Total_CSFB_PS_in_WCDMA_Connection_Count(ObjectLTE)
		return (a+b)
	except Exception:
		logging.warning('error in Total_WCDMA_PS_Connection_Count')
		return ''
def Total_PS_Drop_WCDMA_Only_Count(Object):
	try:
		drop_single = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_PS_Single_RAB_Drop')))
		drop_multi = int(Object.getLastValue(Object.getColumnIndexByName('anovaWCDMA_PS_Multi_RAB_Drop')))
		return (drop_single + drop_multi)
	except Exception:
		logging.warning('error in Total_PS_Drop_WCDMA_Only_Count')
		return ''
	

#################################################################LTE_KPI_OBJECT######################################################
def Mean_CSFB_MO_MultiRAB_Call_Connect_Time(Object):
	"""
	Calculate Mean_CSFB_MO_MultiRAB_Call_Connect_Time
	"""
	try:
		Mean_CSFB_MO_MultiRAB_Call_Connect_Time = Object.getAverageValueInColumn(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_ConnectTime'))
		return Mean_CSFB_MO_MultiRAB_Call_Connect_Time
	except Exception:
		logging.warning("CSFB_MO_Multi_RAB_ConnectTime is empty")

def Mean_CSFB_MO_Call_Connect_Time_SingleRAB(Object):
	"""
	calculate Mean_CSFB_MO_Call_Connect_Time_SingleRAB
	"""
	try:
		Mean_CSFB_MO_SingleRAB_Call_Connect_Time = Object.getAverageValueInColumn(Object.getColumnIndexByName('CSFB_MO_Single_RAB_ConnectTime'))
		return Mean_CSFB_MO_SingleRAB_Call_Connect_Time
	except Exception:
		logging.warning('CSFB_MO_Single_RAB_ConnectTime is empty')	

def Mean_CSFB_MT_Call_Connect_Time_MultiRAB(Object):
	"""
	calculate Mean_CSFB_MT_Call_Connect_Time_MultiRAB
	"""
	try:
		Mean_CSFB_MT_MultiRAB_Call_Connect_Time = Object.getAverageValueInColumn(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_ConnectTime'))
		return Mean_CSFB_MT_MultiRAB_Call_Connect_Time
	except Exception:
		logging.warning('CSFB_MT_Multi_RAB_ConnectTime is empty')

def Mean_CSFB_MT_Call_Connect_Time_SingleRAB(Object):
	"""
	calculate Mean_CSFB_MT_Call_Connect_Time_SingleRAB
	"""
	try:
		Mean_CSFB_MT_SingleRAB_Call_Connect_Time = Object.getAverageValueInColumn(Object.getColumnIndexByName('CSFB_MT_Single_RAB_ConnectTime'))
		return Mean_CSFB_MT_SingleRAB_Call_Connect_Time
	except Exception:
		logging.warning('CSFB_MT_Single_RAB_ConnectTime is empty')


def LTE_Mean_Resource_Block_Allocation(Object):
	"""
	Calculate LTE_Mean_Resource_Block_Allocation
	"""
	try:
		LTE_Mean_Resource_Block_Allocation = Object.getAverageValueInColumn(Object.getColumnIndexByName('Resource_Block_Allocated'))
		return LTE_Mean_Resource_Block_Allocation
	except Exception:
		logging.warning("Resource_Block_Allocated is empty")
		return ''

def LTE_Mean_Rank_Indicator(Object):
	"""
	Calculate LTE_Mean_Rank_Indicator
	"""
	try:
		LTE_Mean_Rank_Indicator = Object.getAverageValueInColumn(Object.getColumnIndexByName('UL_Rank_Index'))
		return LTE_Mean_Rank_Indicator
	except Exception:
		logging.warning("UL_Rank_Index is empty")
		return ''

def Median_CSFB_Redirect_Time_SingleRAB(Object):
	"""
	return the Median CSFB Reselect Time SingleRAB
	"""
	try:
		Median_CSFB_Redirect_Time_SingleRAB = Object.getMedianValueInColumn(Object.getColumnIndexByName('LTE_CSFB_Single_RAB_RedirectTime'))
		return Median_CSFB_Redirect_Time_SingleRAB
	except Exception:
		logging.warning("returned by calculate Median program")
		return ''

def Median_CSFB_Redirect_Time_MultiRAB(Object):
	"""
	return the Median CSFB Reselect Time MultiRAB
	"""
	try:
		Median_CSFB_Redirect_Time_MultiRAB = Object.getMedianValueInColumn(Object.getColumnIndexByName('LTE_CSFB_Multi_RAB_RedirectTime'))
		return Median_CSFB_Redirect_Time_MultiRAB
	except Exception:
		logging.warning("returned by calculate Median program")
		return ''

def Overall_Median_UMTS_To_LTE_Redirect_Time(Object):
	listone = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('LTE_CSFB_Single_RAB_RedirectTime'))
	listtwo = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('LTE_CSFB_Multi_RAB_RedirectTime'))
	inputList = listtwo + listone
	return medianCalculator(inputList)

def LTE_Median_Data_Interrupt_Time_PS_Only_SingleRAB(Object):
	"""
	return the Median Data Interrupt Time PS Only SingleRAB
	"""
	try:
		Median_Data_Interrupt_Time_PS_Only_SingleRAB = Object.getMedianValueInColumn(Object.getColumnIndexByName('LTE_Data_Interrupt_PS_Only_Single_RAB_Time'))
		return Median_Data_Interrupt_Time_PS_Only_SingleRAB
	except Exception:
		logging.warning("returned by calculate Median program")
		return ''

def LTE_Median_Data_Interrupt_Time_PS_Only_MultiRAB(Object):
	"""
	return the Median Data Interrupt Time PS Only MultiRAB
	"""
	try:
		Median_Data_Interrupt_Time_PS_Only_MultiRAB = Object.getMedianValueInColumn(Object.getColumnIndexByName('LTE_Data_Interrupt_PS_Only_Multi_RAB_Time'))
		return Median_Data_Interrupt_Time_PS_Only_MultiRAB
	except Exception:
		logging.warning("returned by calculate Median program")
		return ''

def LTE_Median_Data_Interrupt_Time_CSFB_MO(Object):
	"""
	return the Median of kpi LTE_Data_Interrupt_With_CSFBMO_Multi_RAB_Time
	"""
	try:
		Median_Data_Interrupt_Time_CSFB_MO = Object.getMedianValueInColumn(Object.getColumnIndexByName('LTE_Data_Interrupt_With_CSFBMO_Multi_RAB_Time '))
		return Median_Data_Interrupt_Time_CSFB_MO
	except Exception:
		logging.warning("returned by calculate Median program")
		return ''

def LTE_Median_Data_Interrupt_Time_CSFB_MT(Object):
	"""
	return the Median of kpi LTE_Data_Interrupt_With_CSFBMT_Multi_RAB_Time
	"""
	try:
		Median_Data_Interrupt_Time_CSFB_MT = Object.getMedianValueInColumn(Object.getColumnIndexByName('LTE_Data_Interrupt_With_CSFBMT_Multi_RAB_Time'))
		return Median_Data_Interrupt_Time_CSFB_MT
	except Exception:
		logging.warning("returned by calculate Median program")
		return ''

def LTE_Mean_RB_Count(Object):
	"""
	Calculate mean of Resource_Block_Allocated
	"""
	try:
		LTE_Mean_RB_Count = Object.getAverageValueInColumn(Object.getColumnIndexByName('Resource_Block_Allocated'))
		return LTE_Mean_RB_Count
	except Exception:
		logging.warning("returned by mean calculation program")
		return ''

def Mean_CSFB_UMTS_To_LTE_Redirection_Time_SingleRAB(Object):
	"""
	Calculate Mean CSFB UMTS To LTE Reselection Time SingleRAB
	"""
	try:
		Mean_CSFB_UMTS_To_LTE_Redirection_Time_SingleRAB = Object.getAverageValueInColumn(Object.getColumnIndexByName('LTE_CSFB_Single_RAB_RedirectTime'))
		return Mean_CSFB_UMTS_To_LTE_Redirection_Time_SingleRAB
	except Exception:
		print "Error:returned by mean calculation program"
		return ''

def Mean_CSFB_UMTS_To_LTE_Redirection_Time_MultiRAB(Object):
	"""
	Calculate Mean CSFB UMTS To LTE Reselection Time MultiRAB
	"""
	try:
		Mean_CSFB_UMTS_To_LTE_Redirection_Time_MultiRAB = Object.getAverageValueInColumn(Object.getColumnIndexByName('LTE_CSFB_Multi_RAB_RedirectTime'))
		return Mean_CSFB_UMTS_To_LTE_Redirection_Time_MultiRAB
	except Exception:
		print "Error:returned by mean calculation program"
		return ''

def LTE_DL_PDSCH_ThroughputCount(Object):
	"""
	calculate DL_PDSCH_ThroughputCount
	"""
	try:
		return Object.getNumOfValuesInColumn(Object.getColumnIndexByName('PDSCH_Throughput'))
	except Exception:
		print 'Error:Returned by getNumOfValuesInColumn in DL_PDSCH_ThroughputCount'
		return ''

def LTE_DL_PDSCH_ThroughputAverage(Object):
	"""
	calculate DL_PDSCH_ThroughputAverage
	"""
	try:
		return Object.getAverageValueInColumn(Object.getColumnIndexByName('PDSCH_Throughput'))
	except Exception:
		print 'Error:Returned by getAverageValueInColumn in DL_PDSCH_ThroughputAverage'
		return ''

def LTE_UL_PUSCH_ThroughputCount(Object):
	"""
	calculate LTE_UL_PUSCH_ThroughputCount
	"""
	try:
		return Object.getNumOfValuesInColumn(Object.getColumnIndexByName('PUSCH_Throughput'))
	except Exception:
		print 'Error:Returned by getNumOfValuesInColumn in UL_PUSCH_ThroughputCount'
		return ''

def LTE_UL_PUSCH_ThroughputAverage(Object):
	"""
	calculate UL_PUSCH_ThroughputAverage
	"""
	try:
		return Object.getAverageValueInColumn(Object.getColumnIndexByName('PUSCH_Throughput'))
	except Exception:
		print 'Error:Returned by getAverageValueInColumn in UL_PUSCH_ThroughputAverage'
		return ''

def LTE_PDSCH_Mean_Frame_Usage(Object):
	"""
	calculate LTE PDSCH mean frame usage
	"""
	try:
		return Object.getAverageValueInColumn(Object.getColumnIndexByName('PDSCH_Frame_Usage'))
	except Exception:
		print 'Error:Returned by getAverageValueInColumn in LTE_PDSCH_Mean_Frame_Usage'
		return ''

def Overall_Median_CSFB_Interruption_Time(Object):
	"""
	calculate Overall_Median_CSFB_Interruption_Time
	"""
	try:
		inputList = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('LTE_Data_Interrupt_With_CSFBMO_Multi_RAB_Time'))
		inputList = inputList+(Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('LTE_Data_Interrupt_With_CSFBMT_Multi_RAB_Time')))
		inputList = filter(lambda a: a != ' ', inputList)
		inputList = filter(None, inputList)
		inputList = map(float, inputList)
		inputList.sort()
		numOfElem = len(inputList)
		if (numOfElem==0):
			print 'Warning:pased array is empty'
			return ''
		else:
			if (numOfElem%2 == 0.00):
				Median = (inputList[numOfElem/2 - 1] + inputList[numOfElem/2])/2
			else:
				Median = (inputList[numOfElem/2])
			return Median
	except Exception:
		print 'Error:in Overall_Median_CSFB_Interruption_Time program'
		return ''

def LTE_Spectral_Efficiency_DL(Object):
	"""
	calculate LTE_Spectral_Efficiency_DL
	"""
	try:
		Avg_PDSCH_Frame_Usage = Object.getAverageValueInColumn(Object.getColumnIndexByName('PDSCH_Frame_Usage'))
		LTE_Mean_RB_Count = Object.getAverageValueInColumn(Object.getColumnIndexByName('Resource_Block_Allocated'))
		Avg_RLC_DL_Througput = Object.getAverageValueInColumn(Object.getColumnIndexByName('RLC_DL_Througput'))
		LTE_Spectral_Efficiency_DL = Avg_RLC_DL_Througput/(LTE_Mean_RB_Count*Avg_PDSCH_Frame_Usage*180)
		return LTE_Spectral_Efficiency_DL
	except Exception:
		print 'Warning:Zero in denominator while calating LTE_Spectral_Efficiency_DL'
		return ''

def Median_WCDMA_Time_To_First_Byte(Object):
	"""
	calculatiing Median_WCDMA_Time_To_First_Byte
	"""
	try:
		return Object.getMedianValueInColumn(Object.getColumnIndexByName('LTE_Time_To_First_Byte'))
	except Exception:
		logging.warning('Median problem return a error while calculating Median_WCDMA_Time_To_First_Byte')
		return ''

def LTE_Median_RRC_Setup_Time(Object):
	try:
		return Object.getMedianValueInColumn(Object.getColumnIndexByName('LTE_RRC_Connection_Setup_Time'))
	except Exception:
		logging.warning('Median problem return a error while calculating LTE_Median_RRC_Setup_Time')
		return ''

def LTE_Mean_CQI(Object):
	try:
		return Object.getAverageValueInColumn(Object.getColumnIndexByName('UL_WideBand_CQI_CW[0]'))
	except Exception:
		logging.warning('Median problem return a error while calculating LTE_Mean_CQI')
		return ''
def LTE_Overall_Median_Data_Interrupt_Time(Object):
	try:

		listone = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('LTE_Data_Interrupt_With_CSFBMT_Multi_RAB_Time'))
		listtwo = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('LTE_Data_Interrupt_With_CSFBMO_Multi_RAB_Time'))
		listthree = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('LTE_Data_Interrupt_PS_Only_Single_RAB_Time'))
		listfour = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('LTE_Data_Interrupt_PS_Only_Multi_RAB_Time'))
		listfive = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('LTE_Data_Interruption_Time_PS_After_ESR_MO'))
		listsix = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('LTE_Data_Interruption_Time_PS_After_ESR_MT'))
		inputList = listone+listtwo+listthree+listfour+listfive+listsix
		inputList = filter(None, inputList)
		inputList = filter(lambda a: a != ' ', inputList)
#		print inputList
		inputList = map(int, inputList)        #SZ updated
		inputList.sort()
		numOfElem = len(inputList)
		if (numOfElem==0):
			print 'Warning:pased array is empty while calculating Median'
			return ''
		else:
			if (numOfElem%2 == 0.00):
				Median = (inputList[numOfElem/2 - 1] + inputList[numOfElem/2])/2
			else:
				Median = (inputList[numOfElem/2])
		return Median
	except Exception:
		logging.warning('Error in LTE_Overall_Median_Data_Interrupt_Time')
		return ''
def LTE_Median_Data_Interrupt_Time_PS_After_ESR_MO(Object):
	try:
		return Object.getMedianValueInColumn(Object.getColumnIndexByName('LTE_Data_Interruption_Time_PS_After_ESR_MO'))
	except Exception:
		logging.warning('Median problem return a error while calculating LTE_Median_Data_Interrupt_Time_PS_After_ESR_MO')
		return ''
def LTE_Median_Data_Interrupt_Time_PS_After_ESR_MT(Object):
	try:
		return Object.getMedianValueInColumn(Object.getColumnIndexByName('LTE_Data_Interruption_Time_PS_After_ESR_MT'))
	except Exception:
		logging.warning('Median problem return a error while calculating LTE_Median_Data_Interrupt_Time_PS_After_ESR_MT')
		return ''

def Overall_CSFB_LTE_To_UMTS_Redirection_Success_Rate(Object):
	return percantageCalculator('LTE_IRAT_Redirect_With_CSFB_Single_RAB_AttemptCount','LTE_IRAT_Redirect_With_CSFB_Multi_RAB_AttemptCount','LTE_IRAT_Redirect_With_CSFB_Single_RAB_SuccessCount','LTE_IRAT_Redirect_With_CSFB_Multi_RAB_SuccessCount',Object)

def Overall_CSFB_UMTS_To_LTE_Reselection_Success_Rate(Object):
	return percantageCalculator('UMTS_LTE_Redirect_With_CSFB_Multi_RAB_AttemptCount','UMTS_LTE_Redirect_With_CSFB_Single_RAB_AttemptCount','UMTS_LTE_Redirect_With_CSFB_Single_RAB_SuccessCount','UMTS_LTE_Redirect_With_CSFB_Multi_RAB_SuccessCount',Object)

def Overall_LTE_Mean_Incremental_CS_Call_Connect_Time(Object):
	try:
		a = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('CSFB_MO_Single_RAB_Increment_ConnectTime'))
		b = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_Increment_ConnectTime'))
		c = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('CSFB_MT_Single_RAB_Increment_ConnectTime'))
		d = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_Increment_ConnectTime'))
		colList = a+b+c+d
                avg = Calculate_mean(colList)
		return avg
	except Exception:
		logging.warning('some error in Overall_LTE_Mean_Incremental_CS_Call_Connect_Time')
		return ''
def LTE_Mean_Incremental_CS_MO_Single_RAB_Call_Connect_Time(Object):
	try:
		return Object.getAverageValueInColumn(Object.getColumnIndexByName('CSFB_MO_Single_RAB_Increment_ConnectTime'))
	except Exception:
		logging.warning('some error in LTE_Mean_Incremental_CS_MO_Single_RAB_Call_Connect_Time')
		return ''


def LTE_Mean_Incremental_CS_MO_Multi_RAB_Call_Connect_Time(Object):
	try:
		return Object.getAverageValueInColumn(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_Increment_ConnectTime'))
	except Exception:
		logging.warning('some error in LTE_Mean_Incremental_CS_MO_Multi_RAB_Call_Connect_Time')
		return ''

def LTE_Mean_Incremental_CS_MT_Single_RAB_Call_Connect_Time(Object):
	try:
		return Object.getAverageValueInColumn(Object.getColumnIndexByName('CSFB_MT_Single_RAB_Increment_ConnectTime'))
	except Exception:
		logging.warning('some error in LTE_Mean_Incremental_CS_MT_Single_RAB_Call_Connect_Time')
		return ''


def LTE_Mean_Incremental_CS_MT_Multi_RAB_Call_Connect_Time(Object):
	try:
		return Object.getAverageValueInColumn(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_Increment_ConnectTime'))
	except Exception:
		logging.warning('some error in LTE_Mean_Incremental_CS_MT_Multi_RAB_Call_Connect_Time')
		return ''
def CSFB_MT_ConnectTime(Object):
		a = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('CSFB_MT_Single_RAB_ConnectTime'))
		b = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_ConnectTime'))
		return (a + b)

def Total_Time_List_CSFB_Connect_Time(Object):
	a = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('CSFB_MO_Single_RAB_ConnectTime'))
	b = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_ConnectTime'))
	csfb_mt = CSFB_MT_ConnectTime(Object)

	colList = a + b + csfb_mt
	return colList

def Total_LTE_CSFB_Call_Connect_Time(Object):
	try:
		colList = Total_Time_List_CSFB_Connect_Time(Object)
		avg = Calculate_mean(colList)
		avg = avg/1000		#in sec
		return avg
	except Exception:
		logging.warning('some error in Total_LTE_CSFB_Call_Connect_Time')
		return ''
def Overall_CS_Mean_Call_Connect_Time(ObjectWCDMA,ObjectLTE):
	try:
		one = Total_Time_List_WCDMA_CS_Connect_Time(ObjectWCDMA)
		two = Total_Time_List_CSFB_Connect_Time(ObjectLTE)
		colList = one+two
        	avg = Calculate_mean(colList)
		avg = avg/1000		#in sec
		return avg
	except Exception:
		logging.warning('some error in Overall_CS_Mean_Call_Connect_Time')
		return ''

def LTE_Mean_CSFB_MO_Single_RAB_Call_Connect_Time(Object):
	try:
		return Object.getAverageValueInColumn(Object.getColumnIndexByName('CSFB_MO_Single_RAB_ConnectTime'))
	except Exception:
		logging.warning('some error in LTE_Mean_CSFB_MO_Single_RAB_Call_Connect_Time')
		return ''

def LTE_Mean_CSFB_MO_Multi_RAB_Call_Connect_Time(Object):
	try:
		return Object.getAverageValueInColumn(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_ConnectTime'))
	except Exception:
		logging.warning('some error in LTE_Mean_CSFB_MO_Multi_RAB_Call_Connect_Time')
		return ''

def LTE_Mean_CSFB_MT_Single_RAB_Call_Connect_Time(Object):
	try:
		return Object.getAverageValueInColumn(Object.getColumnIndexByName('CSFB_MT_Single_RAB_ConnectTime'))
	except Exception:
		logging.warning('some error in LTE_Mean_CSFB_MT_Single_RAB_Call_Connect_Time')
		return ''

def LTE_Mean_CSFB_MT_Multi_RAB_Call_Connect_Time(Object):
	try:
		return Object.getAverageValueInColumn(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_ConnectTime'))
	except Exception:
		logging.warning('some error in LTE_Mean_CSFB_MT_Multi_RAB_Call_Connect_Time')
		return ''

def Overall_Mean_CSFB_UMTS_To_LTE_Redirection_Time(Object):
	try:
		listone = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('LTE_CSFB_Single_RAB_RedirectTime'))
		listtwo = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('LTE_CSFB_Multi_RAB_RedirectTime'))
		colList = listtwo + listone
                avg = Calculate_mean(colList)
                return avg
	except Exception:
		logging.warning('Error in Overall_Mean_CSFB_UMTS_To_LTE_Redirection_Time')
		return ''

def Median_CSFB_MO_Interruption_Time(Object):
	return Object.getMedianValueInColumn(Object.getColumnIndexByName('LTE_Data_Interrupt_With_CSFBMO_Multi_RAB_Time'))

def Median_CSFB_MT_Interruption_Time(Object):
	return Object.getMedianValueInColumn(Object.getColumnIndexByName('LTE_Data_Interrupt_With_CSFBMT_Multi_RAB_Time'))

def LTE_PRACH_Tx_Power_Sample_Count(Object):
	try:
		return Object.getNumOfValuesInColumn(Object.getColumnIndexByName('PRACH_TX_POWER'))
	except Exception:
		print 'Error:Returned by  LTE_PRACH_Tx_Power_Sample_Count'
		return ''

def Total_PS_Connected_Time_in_LTE(ObjectLTE):
	try:
		one = ObjectLTE.getAllColumnValuesByIndex(ObjectLTE.getColumnIndexByName('LTE_PS_Single_RAB_Connected_Time'))
		two = ObjectLTE.getAllColumnValuesByIndex(ObjectLTE.getColumnIndexByName('LTE_PS_Connected_Multi_RAB_Connected_Time'))
		three = ObjectLTE.getAllColumnValuesByIndex(ObjectLTE.getColumnIndexByName('LTE_PS_Only_Multi_RAB_Connected_Time'))
		colList = one + two + three
		sum_result = sum_List_element(colList)  #, typeTomap = int)
		sum_result = sum_result/(1000.0*60.0)		#in min
                return sum_result
	except Exception:
		logging.warning('Error in Total_PS_Connected_Time_in_LTE')
		return ''

def LTE_CSFB_and_WCDMA_PS_Connected_Time(ObjectWCDMA,ObjectLTE):
	'''
		This Function returns time in second
	'''
	try:
		one = ObjectWCDMA.getAllColumnValuesByIndex(ObjectWCDMA.getColumnIndexByName('WCDMA_PS_CONNECTED_TIME'))
		two = ObjectLTE.getAllColumnValuesByIndex(ObjectLTE.getColumnIndexByName('LTE_CSFB_PS_Connected_Time_in_WCDMA'))
		colList = two + one
		temp_sum = sum_List_element(colList) # , typeTomap = int)
		temp_sum = temp_sum/(1000.0)	#in sec
		
                return temp_sum
	except Exception:
		logging.warning('Error in LTE_CSFB_and_WCDMA_PS_Connected_Time')
		return ''
	
def Overall_PS_Connected_Time(ObjectWCDMA, ObjectLTE):
	temp_sum = LTE_CSFB_and_WCDMA_PS_Connected_Time(ObjectWCDMA,ObjectLTE)
	temp_sum = temp_sum/(60.0)	#in min

	Lte_PS_sum = Total_PS_Connected_Time_in_LTE(ObjectLTE)

	total_time = temp_sum + Lte_PS_sum
	return total_time
def Mean_CSFB_MO_SingleRAB_IncrementSetupTime(Object):
	try:
		a = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('CSFB_MO_Single_RAB_Increment_ConnectTime'))
                avg = Calculate_mean(a)
		avg = avg/1000
		return avg
	except Exception:
		logging.warning('some error in Mean_CSFB_MO_SingleRAB_IncrementSetupTime')


def Mean_CSFB_MT_IncrementalSetupTime(Object):
	try:
		a = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('CSFB_MT_Single_RAB_Increment_ConnectTime'))
		b = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_Increment_ConnectTime'))
		colList = a+b
                avg = Calculate_mean(colList)
		avg = avg/1000
		return avg
	except Exception:
		logging.warning('some error in Mean_CSFB_MT_IncrementalSetupTime')
def Mean_UMTS_LTE_CSFB_Reselect_Duration(Object):
	try:
		a = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('anovaUMTS_LTE_CSFB_Reselect_Duration'))
                avg = Calculate_mean(a)
		return avg
	except Exception:
		logging.warning('some error in Mean_UMTS_LTE_CSFB_Reselect_Duration')

def Median_UMTS_LTE_CSFB_Reselect_Duration(Object):
	try:
		a = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('anovaUMTS_LTE_CSFB_Reselect_Duration'))
                median = medianCalculator(a)
		return median
	except Exception:
		logging.warning('some error in Median_UMTS_LTE_CSFB_Reselect_Duration')
		
########################################################LTE_COUNTER_OBJECT##############################################################
def CSFB_LTE_To_UMTS_Redirection_Success_Rate_SingleRAB(Object):
	"""
	Calculate CSFB LTE To UMTS Redirection Success Rate SingleRAB
	"""
	return successRateCalculator('LTE_IRAT_Redirect_With_CSFB_Single_RAB_AttemptCount','LTE_IRAT_Redirect_With_CSFB_Single_RAB_SuccessCount',Object)

def CSFB_LTE_To_UMTS_Redirection_Success_Rate_MultiRAB(Object):
	"""
	Calculate CSFB LTE To UMTS Redirection Success Rate SingleRAB
	"""
	return successRateCalculator('LTE_IRAT_Redirect_With_CSFB_Multi_RAB_AttemptCount','LTE_IRAT_Redirect_With_CSFB_Multi_RAB_SuccessCount',Object)


###'''same implementation was done for CSFB_UMTS_To_LTE_Redirection_Success_Rate_MultiRAB'''
'''
def UMTS_To_LTE_Reselection_Success_Rate_SingleRAB(Object):
	"""
	calculate UMTS_To_LTE_Reselection_Success_Rate_SingleRAB
	"""
	return successRateCalculator('UMTS_LTE_Redirect_With_CSFB_Single_RAB_AttemptCount','UMTS_LTE_Redirect_With_CSFB_Single_RAB_SuccessCount',Object)

def UMTS_To_LTE_Reselection_Success_Rate_MultiRAB(Object):
	"""
	calculate UMTS_To_LTE_Reselection_Success_Rate_MultiRAB
	"""
	return successRateCalculator('UMTS_LTE_Redirect_With_CSFB_Multi_RAB_AttemptCount','UMTS_LTE_Redirect_With_CSFB_Multi_RAB_SuccessCount',Object)
'''
def CSFB_MO_SingleRAB_Setup_Success_Rate(Object):
	"""
	calculate CSFB_MO_SingleRAB_Setup_Success_Rate
	"""
	return successRateCalculator('CSFB_MO_Single_RAB_AttemptCount','CSFB_MO_Single_RAB_SuccessCount',Object)

def CSFB_MT_Setup_Success_Rate_SingleRAB(Object):
	"""
	calculate CSFB_MO_SingleRAB_Setup_Success_Rate
	"""
	return successRateCalculator('CSFB_MT_Single_RAB_AttemptCount','CSFB_MT_Single_RAB_SuccessCount',Object)

def LTE_To_UMTS_HO_Success_Rate_PS_Only_Single_RAB(Object):
	"""
	Calculate LTE_To_UMTS_HO_Success_Rate_PS_Only_Single_RAB
	"""
	return successRateCalculator('LTE_IRAT_Redirect_PS_Only_Single_RAB_AttemptCount','LTE_IRAT_Redirect_PS_Only_Single_RAB_SuccessCount',Object)

def LTE_To_UMTS_HO_Success_Rate_PS_Only_Multi_RAB(Object):
	"""
	Calculate LTE_To_UMTS_HO_Success_Rate_PS_Only_Single_RAB
	"""
	return successRateCalculator('LTE_IRAT_Redirect_PS_Only_Multi_RAB_AttemptCount','LTE_IRAT_Redirect_PS_Only_Multi_RAB_SuccessCount',Object)

def Overall_LTE_To_UMTS_HO_Success_Rate(Object):
	return percantageCalculator('LTE_IRAT_Redirect_PS_Only_Single_RAB_AttemptCount','LTE_IRAT_Redirect_PS_Only_Multi_RAB_AttemptCount','LTE_IRAT_Redirect_PS_Only_Single_RAB_SuccessCount','LTE_IRAT_Redirect_PS_Only_Multi_RAB_SuccessCount',Object)
'''
def LTE_MIMO_USAGE(Object):		//already calculated 
	"""
	calculate LTE_MIMO_USAGE
	"""
	try:
		MIMO_Sample_Count = int(Object.getLastValue(Object.getColumnIndexByName('MIMO_Sample_Count')))
		Non_MIMO_Sample_Count = int(Object.getLastValue(Object.getColumnIndexByName('Non_MIMO_Sample_Count')))
		LTE_MIMO_USAGE = MIMO_Sample_Count*100/(MIMO_Sample_Count + Non_MIMO_Sample_Count)
		return LTE_MIMO_USAGE
	except Exception:
		print "Warning:MIMO_Sample_Count = 0"
		return ''
'''
def LTE_MIMO_USAGE(Object): 
	"""
	calculate LTE_MIMO_USAGE
	"""
	try:
		listone = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('MIMO_Usage'))
		zero_Count = listone.count('0.00 ')
		Non_zero_Count = len(listone) - zero_Count 
		LTE_MIMO_USAGE = Non_zero_Count*100.0/(len(listone)) 
		return LTE_MIMO_USAGE
	except Exception:
		print "Warning:MIMO_Sample_Count = 0"
		return ''
def LTE_QAM_USAGE(Object):
	try:
		listone = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('QAM_Status'))
				
		QAM_Sample_Count = listone.count(' 64QAM ')
		Non_QAM_Sample_Count = listone.count(' Non64QAM ')
		LTE_QAM_USAGE = QAM_Sample_Count*100.0/(QAM_Sample_Count + Non_QAM_Sample_Count) 

		return LTE_QAM_USAGE
	except Exception:
		print "Warning:QAM_Sample_Count = 0"
		return ''

def CSFB_MO_PS_Setup_Success_Rate(Object):
	"""
	calculate CSFB_MO_PS_Setup_Success_Rate
	"""
	return successRateCalculator('PS_With_CSFBMO_AttemptCount','LTE_PS_With_CSFB_MO_Successful_Resume_in_WCDMA_Count',Object)

def CSFB_MT_PS_Setup_Success_Rate(Object):
	"""
	calculate CSFB_MT_PS_Setup_Success_Rate
	"""
	return successRateCalculator('PS_With_CSFBMT_AttemptCount','LTE_PS_With_CSFB_MT_Successful_Resume_in_WCDMA_Count',Object)

def LTE_RRC_Detach_Drops(Object):
	"""
	calculate LTE_RRC_Detach_Drops
	"""
	return dropCountCalculator('LTE_Detach_AttemptCount','LTE_Detach_SuccessCount',Object)


def LTE_RRC_Attach_Drops(Object):
	"""
	calculate LTE_RRC_Attach_Drops
	"""
	return dropCountCalculator('anovaLTE_Attach_Request','anovaLTE_Attach_Accept',Object)

def LTE_RRC_Retainability_Rate(Object):
	"""
	calculate LTE_RRC_Retainability_Rate
	"""
#	return successRateCalculator('RRC_Connection_Setup_Complete','RRC_Connection_Release_Count',Object)  
	return successRateCalculator('anovaLTE_RRC_Connection_Setup_CompleteCount','anovaLTE_RRC_Connection_ReleaseCount',Object)  


def LTE_RRC_Reestablishment_Success_Rate(Object):
	"""
	calculate LTE_RRC_Reestablishment_Success_Rate
	"""
	return successRateCalculator('LTE_ReEstablisment_AttemptCount','LTE_ReEstablishment_SuccessCount',Object)

def CSFB_MO_Single_RAB_Drop_Count(Object):
	return dropCountCalculator('CSFB_MO_Single_RAB_SuccessCount','CSFB_MO_Single_RAB_SuccessfulReleaseCount',Object)

def CSFB_MO_Multi_RAB_Drop_Count(Object):
	return dropCountCalculator('CSFB_MO_Multi_RAB_SuccessCount','CSFB_MO_Multi_RAB_SuccessfulReleaseCount',Object)

def CSFB_MT_Single_RAB_Drop_Count(Object):
	return dropCountCalculator('CSFB_MT_Single_RAB_SuccessCount','CSFB_MT_Single_RAB_SuccessfulReleaseCount',Object)

def CSFB_MT_Multi_RAB_Drop_Count(Object):
	return dropCountCalculator('CSFB_MT_Multi_RAB_SuccessCount','CSFB_MT_Multi_RAB_SuccessfulReleaseCount',Object)

def CSFB_Retainability_Rate_SingleRAB(Object):
	try:
		CSFB_MO_Single_RAB_DisconnectCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessfulReleaseCount')))
		CSFB_MT_Single_RAB_DisconnectCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessfulReleaseCount')))
		CSFB_MO_Single_RAB_SuccessCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessCount')))
		CSFB_MT_Single_RAB_SuccessCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessCount')))
		CSFB_Retainability_Rate_SingleRAB = (CSFB_MO_Single_RAB_DisconnectCount + CSFB_MT_Single_RAB_DisconnectCount)*100.0/(CSFB_MO_Single_RAB_SuccessCount + CSFB_MT_Single_RAB_SuccessCount)
		return CSFB_Retainability_Rate_SingleRAB
	except Exception:
		print 'Warning:one the CSFB_MO_Single_RAB_SuccessfulReleaseCount,CSFB_MT_Single_RAB_SuccessfulReleaseCount,CSFB_MO_Single_RAB_SuccessCount,CSFB_MT_Single_RAB_SuccessCount is non integer'
		return ''

def CSFB_Retainability_Rate_MultiRAB(Object):
	try:
		CSFB_MO_multi_RAB_DisconnectCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_SuccessfulReleaseCount')))
		CSFB_MT_multi_RAB_DisconnectCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_SuccessfulReleaseCount')))
		CSFB_MO_multi_RAB_SuccessCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_SuccessCount')))
		CSFB_MT_multi_RAB_SuccessCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_SuccessCount')))
		CSFB_Retainability_Rate_multiRAB = (CSFB_MO_multi_RAB_DisconnectCount + CSFB_MT_multi_RAB_DisconnectCount)*100.0/(CSFB_MO_multi_RAB_SuccessCount + CSFB_MT_multi_RAB_SuccessCount)
		return CSFB_Retainability_Rate_multiRAB
	except Exception:
		print 'Warning:one the CSFB_MO_multi_RAB_SuccessfulReleaseCount,CSFB_MT_multi_RAB_SuccessfulReleaseCount,CSFB_MO_multi_RAB_SuccessCount,CSFB_MT_multi_RAB_SuccessCount is non integer'
		return ''

def CSFB_Drop_Count_SingleRAB(Object):
	try:
		CSFB_MO_Single_RAB_DisconnectCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessfulReleaseCount')))
		CSFB_MT_Single_RAB_DisconnectCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessfulReleaseCount')))
		CSFB_MO_Single_RAB_SuccessCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessCount')))
		CSFB_MT_Single_RAB_SuccessCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessCount')))
		CSFB_Drop_Count_SingleRAB = (CSFB_MO_Single_RAB_SuccessCount+CSFB_MT_Single_RAB_SuccessCount)-(CSFB_MO_Single_RAB_DisconnectCount+CSFB_MT_Single_RAB_DisconnectCount)
		return CSFB_Drop_Count_SingleRAB
	except Exception:
		print 'Warning:one the CSFB_MO_Single_RAB_SuccessfulReleaseCount,CSFB_MT_Single_RAB_SuccessfulReleaseCount,CSFB_MO_Single_RAB_SuccessCount,CSFB_MT_Single_RAB_SuccessCount is non integer'
		return ''

def CSFB_Drop_Count_MultiRAB(Object):
	try:
		CSFB_MO_multi_RAB_DisconnectCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_SuccessfulReleaseCount')))
		CSFB_MT_multi_RAB_DisconnectCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_SuccessfulReleaseCount')))
		CSFB_MO_multi_RAB_SuccessCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_SuccessCount')))
		CSFB_MT_multi_RAB_SuccessCount = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_SuccessCount')))
		CSFB_Drop_Count_MultiRAB = (CSFB_MO_multi_RAB_SuccessCount+CSFB_MT_multi_RAB_SuccessCount)-(CSFB_MO_multi_RAB_DisconnectCount+CSFB_MT_multi_RAB_DisconnectCount)
		return CSFB_Drop_Count_MultiRAB
	except Exception:
		print 'Warning:one the CSFB_MO_multi_RAB_SuccessfulReleaseCount,CSFB_MT_multi_RAB_SuccessfulReleaseCount,CSFB_MO_multi_RAB_SuccessCount,CSFB_MT_multi_RAB_SuccessCount is non integer'
		return ''

def CSFB_UMTS_To_LTE_Redirection_Success_Rate_SingleRAB(Object):
	return successRateCalculator('UMTS_LTE_Redirect_With_CSFB_Single_RAB_AttemptCount','UMTS_LTE_Redirect_With_CSFB_Single_RAB_SuccessCount',Object)

def CSFB_UMTS_To_LTE_Redirection_Success_Rate_MultiRAB(Object):
	return successRateCalculator('UMTS_LTE_Redirect_With_CSFB_Multi_RAB_AttemptCount','UMTS_LTE_Redirect_With_CSFB_Multi_RAB_SuccessCount',Object)

def LTE_To_UMTS_Redirection_Failures(Object):
	try:
		LTE_UMTS_Redirect_SuccessCount = int(Object.getLastValue(Object.getColumnIndexByName('LTE_UMTS_Redirect_SuccessCount')))
		LTE_UMTS_Redirect_AttemptConut = int(Object.getLastValue(Object.getColumnIndexByName('LTE_UMTS_Redirect_AttemptConut')))
		LTE_To_UMTS_Redirection_Failures = LTE_UMTS_Redirect_AttemptConut - LTE_UMTS_Redirect_SuccessCount
		return LTE_To_UMTS_Redirection_Failures
	except Exception:
		print 'Warning:LTE_UMTS_Redirect_AttemptConut = 0'
		return ''

def LTE_IRAT_Success_Rate(Object):
	try:
		LTE_UMTS_Redirect_SuccessCount = int(Object.getLastValue(Object.getColumnIndexByName('LTE_UMTS_Redirect_SuccessCount')))
		LTE_UMTS_Redirect_AttemptConut = int(Object.getLastValue(Object.getColumnIndexByName('LTE_UMTS_Redirect_AttemptConut')))
		LTE_UMTS_Reselect_AttemptConut = int(Object.getLastValue(Object.getColumnIndexByName('LTE_UMTS_Reselect_AttemptConut')))
		LTE_UMTS_Reselect_SuccessCount = int(Object.getLastValue(Object.getColumnIndexByName('LTE_UMTS_Reselect_SuccessCount')))
		LTE_IRAT_Success_Rate = (LTE_UMTS_Redirect_SuccessCount + LTE_UMTS_Reselect_SuccessCount)*100/(LTE_UMTS_Redirect_AttemptConut + LTE_UMTS_Reselect_AttemptConut)
		return LTE_IRAT_Success_Rate
	except Exception:
		print 'Warning:LTE_UMTS_Redirect_AttemptConut + LTE_UMTS_Reselect_AttemptConut = 0'
		return ''

def LTE_PS_Accessibility_Single_RAB(Object):
	return successRateCalculator('LTE_PS_Single_RAB_AttemptCount','LTE_PS_Single_RAB_SuccessCount',Object)

def LTE_PS_Accessibility_Multi_RAB(Object):
	return successRateCalculator('LTE_PS_Multi_RAB_AttemptCount','LTE_PS_Multi_RAB_SuccessCount',Object)

def LTE_PS_Accessibility_Total(Object):
	return percantageCalculator('LTE_PS_Single_RAB_AttemptCount','LTE_PS_Multi_RAB_AttemptCount','LTE_PS_Single_RAB_SuccessCount','LTE_PS_Multi_RAB_SuccessCount',Object)

def LTE_Network_Attach_Success_Rate(Object):
	return successRateCalculator('anovaLTE_Attach_Request','anovaLTE_Attach_Accept',Object)

def LTE_RACH_Failure_Rate(Object):
	return successRateCalculator('RACH_Attempt_Num_Of_RACH_Attempt','RACH_Attempt_Num_Of_Failure',Object)

def LTE_CSFB_Accessibility_Single_RAB_MO(Object):
	"""
	calculate CSFB_MO_SingleRAB_Setup_Success_Rate
	"""
	return successRateCalculator('CSFB_MO_Single_RAB_AttemptCount','CSFB_MO_Single_RAB_SuccessCount',Object)

def LTE_CSFB_Accessibility_Single_RAB_MT(Object):
	"""
	calculate CSFB_MO_SingleRAB_Setup_Success_Rate
	"""
	return successRateCalculator('CSFB_MT_Single_RAB_AttemptCount','CSFB_MT_Single_RAB_SuccessCount',Object)

def LTE_CSFB_Accessibility_Multi_RAB_MO(Object):
	"""
	calculate CSFB_MO_SingleRAB_Setup_Success_Rate
	"""
	return successRateCalculator('CSFB_MO_Multi_RAB_AttemptCount','CSFB_MO_Multi_RAB_SuccessCount',Object)

def LTE_CSFB_Accessibility_Multi_RAB_MT(Object):
	"""
	calculate CSFB_MO_SingleRAB_Setup_Success_Rate
	"""
	return successRateCalculator('CSFB_MT_Multi_RAB_AttemptCount','CSFB_MT_Multi_RAB_SuccessCount',Object)
def Total_CSFB_Success(Object):  #no use
		a = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessCount')))
		b = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessCount')))
		c = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_SuccessCount')))
		d = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_SuccessCount')))
		total=a + b+c+d
		return total

def Total_CSFB_Attempt(Object):		#no use
		e = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Single_RAB_AttemptCount')))
		f = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Single_RAB_AttemptCount')))
		j = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_AttemptCount')))
		k = int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_AttemptCount')))

		total=e+f+j+k
		return total
def LTE_CSFB_Accessibility_Total(Object):
	try:
		success = Overall_CSFB_Success_Count(Object)
		attempt = Overall_CSFB_Attempt_Count(Object)
		return success*100.0/attempt
	except Exception:
		logging.warning('denominator zero in LTE_CSFB_Accessibility_Total program')
		return ''

def LTE_CSFB_Retainability_Single_RAB_MO(Object):
	return successRateCalculator('CSFB_MO_Single_RAB_SuccessCount','CSFB_MO_Single_RAB_SuccessfulReleaseCount',Object)

def LTE_CSFB_Retainability_Single_RAB_MT(Object):
	return successRateCalculator('CSFB_MT_Single_RAB_SuccessCount','CSFB_MT_Single_RAB_SuccessfulReleaseCount',Object)

def LTE_CSFB_Retainability_Multi_RAB_MO(Object):
	return successRateCalculator('CSFB_MO_Multi_RAB_SuccessCount','CSFB_MO_Multi_RAB_SuccessfulReleaseCount',Object)

def LTE_CSFB_Retainability_Multi_RAB_MT(Object):
	return successRateCalculator('CSFB_MT_Multi_RAB_SuccessCount','CSFB_MT_Multi_RAB_SuccessfulReleaseCount',Object)


def LTE_CSFB_Retainability_Total(Object):
	try:
		success = Overall_CSFB_Success_Count(Object)
		disconnect = Overall_CSFB_SuccessfulRelease_Count(Object)
		return disconnect*100.0/success
	except Exception:
		logging.warning('denominator zero in LTE_CSFB_Retainability_Total program')
		return ''

def LTE_Intra_Frequency_HO_Success_Rate(Object):
	try:
		Intra_LTE_HO_Failure = int(Object.getLastValue(Object.getColumnIndexByName('Intra_LTE_HO_Failure')))
		Intra_LTE_HO_Success = int(Object.getLastValue(Object.getColumnIndexByName('Intra_LTE_HO_Success')))
		LTE_Intra_Frequency_HO_Success_Rate = Intra_LTE_HO_Success*100.0/(Intra_LTE_HO_Success+ Intra_LTE_HO_Failure)
		return LTE_Intra_Frequency_HO_Success_Rate
	except Exception:
		logging.warning('Intra_LTE_HO_attempt = 0')
		return ''

def LTE_Inter_Frequency_HO_Success_Rate(Object):
	try:
		Inter_LTE_HO_Failure = int(Object.getLastValue(Object.getColumnIndexByName('Inter_LTE_HO_Failure')))
		Inter_LTE_HO_Success = int(Object.getLastValue(Object.getColumnIndexByName('Inter_LTE_HO_Success')))
		LTE_Inter_Frequency_HO_Success_Rate = Inter_LTE_HO_Success*100.0/(Inter_LTE_HO_Success+ Inter_LTE_HO_Failure)
		return LTE_Inter_Frequency_HO_Success_Rate
	except Exception:
		logging.warning('Inter_LTE_HO_attempt = 0')
		return ''

def LTE_Network_Attach_Success_Rate(Object):
	return successRateCalculator('anovaLTE_Attach_Request','anovaLTE_Attach_CompleteCount',Object)

def LTE_TAU_Success_Rate(Object):
	return successRateCalculator('anovaLTE_Track_Area_Update_RequestCount','anovaLTE_Track_Area_Update_AcceptCount',Object)

def LTE_Minutes_Per_Drop(Object, Calculate_Time_RRC_State):
	try:
		LTE_drop = int(Object.getLastValue(Object.getColumnIndexByName('LTE_RRC_Drop_Count')))
		return Calculate_Time_RRC_State /(LTE_drop*60)
	except Exception:
		logging.warning('Error in LTE_Minutes_Per_Drop')
		return ''

def LTE_Time_Between_Inter_Frequency_HO(Object,Calculate_Time_RRC_State):
	try:
		Inter_LTE_HO_Success = int(Object.getLastValue(Object.getColumnIndexByName('Inter_LTE_HO_Success')))
		return Calculate_Time_RRC_State/Inter_LTE_HO_Success
	except Exception:
		logging.warning('error while calculating LTE_Time_Between_Inter_Frequency_HO')
		return ''

def LTE_Time_Between_Intra_Frequency_HO(Object,Calculate_Time_RRC_State):
	try:
		Intra_LTE_HO_Success = int(Object.getLastValue(Object.getColumnIndexByName('Intra_LTE_HO_Success')))
		return Calculate_Time_RRC_State/Intra_LTE_HO_Success
	except Exception:
		logging.warning('error while calculating LTE_Time_Between_Intra_Frequency_HO')

def LTE_RRC_Connection_Success_Rate(Object):
	return percantageCalculator('anovaLTE_RRC_Connection_RequestCount','LTE_ReEstablisment_AttemptCount','LTE_ReEstablishment_SuccessCount','anovaLTE_RRC_Connection_Setup_CompleteCount',Object)

def PS_With_CSFB_Success(ObjectTwo):
	a = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('PS_With_CSFBMO_SuccessCount')))
	b = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('PS_With_CSFBMT_SuccessCount')))
	ret = a + b
	return ret
	
def LTE_CSFB_Success_total(ObjectTwo):
	try:
		a =  PS_With_CSFB_Success(ObjectTwo)
		c = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('LTE_PS_After_ESR_MO_in_WCDMA_Success_Count')))
		d = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('LTE_PS_After_ESR_MT_in_WCDMA_Success_Count')))
		return (a+c+d)
	except Exception:
		logging.warning('error in LTE_CSFB_Success_total')
		return ''

def LTE_CSFB_Attempt_total(ObjectTwo):
	try:
		a = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('PS_With_CSFBMO_AttemptCount')))
		b = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('PS_With_CSFBMT_AttemptCount')))
		c = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('LTE_PS_After_ESR_MO_Attempt_Count')))
		d = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('LTE_PS_After_ESR_MT_Attempt_Count')))
		return (a+b+c+d)
	except Exception:
		logging.warning('error in LTE_CSFB_Attempt_total')
		return ''

def Overall_CSFB_PS_Setup_Success_Rate(Object):
	try:
#		success = LTE_CSFB_Success_total(Object)
		a = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_With_CSFB_MO_Successful_Resume_in_WCDMA_Count'))) 
		b = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_With_CSFB_MT_Successful_Resume_in_WCDMA_Count')))
		c = LTE_PS_After_ESR_Success_resume(Object)
		print "a = %s , b =%s"%(a,b)
		success = a + b + c
		attempt = LTE_CSFB_Attempt_total(Object)
		return (success * 100.0)/attempt
	except Exception:
		logging.warning('error in Overall_CSFB_PS_Setup_Success_Rate')
		return ''

def LTE_PS_After_ESR_MO_Setup_Success_Rate(Object):
	return successRateCalculator('LTE_PS_After_ESR_MO_Attempt_Count','LTE_PS_After_ESR_MO_Successful_Resume_in_WCDMA_Count',Object)

def LTE_PS_After_ESR_MT_Setup_Success_Rate(Object):
	return successRateCalculator('LTE_PS_After_ESR_MT_Attempt_Count','LTE_PS_After_ESR_MT_Successful_Resume_in_WCDMA_Count',Object)


def Overall_CSFB_Attempt_Count(Object):
	return int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Single_RAB_AttemptCount')))+int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_AttemptCount')))+int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Single_RAB_AttemptCount')))+int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_AttemptCount')))

def Overall_CSFB_Success_Count(Object):
	return int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessCount')))+int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_AttemptCount')))+int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Single_RAB_AttemptCount')))+int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_AttemptCount')))

def Overall_CSFB_SuccessfulRelease_Count(Object):
	return int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessfulReleaseCount')))+int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_SuccessfulReleaseCount')))+int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessfulReleaseCount')))+int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_SuccessfulReleaseCount')))

def Overall_CSFB_Drop_Count(Object):
	return ((int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessCount'))) + int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_SuccessCount'))) + int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessCount'))) + int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_SuccessCount')))) - (int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessfulReleaseCount'))) + int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MO_Multi_RAB_SuccessfulReleaseCount'))) + int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessfulReleaseCount'))) + int(Object.getLastValue(Object.getColumnIndexByName('CSFB_MT_Multi_RAB_SuccessfulReleaseCount')))))

def Overall_CSFB_UMTS_To_LTE_Redirection_Attempt(Object):
	return int(Object.getLastValue(Object.getColumnIndexByName('UMTS_LTE_Redirect_With_CSFB_Single_RAB_AttemptCount'))) + int(Object.getLastValue(Object.getColumnIndexByName('UMTS_LTE_Redirect_With_CSFB_Multi_RAB_AttemptCount')))

def Overall_CSFB_UMTS_To_LTE_Redirection_Faiure(Object):
	return ((int(Object.getLastValue(Object.getColumnIndexByName('UMTS_LTE_Redirect_With_CSFB_Single_RAB_AttemptCount'))) + int(Object.getLastValue(Object.getColumnIndexByName('UMTS_LTE_Redirect_With_CSFB_Multi_RAB_AttemptCount')))) - (int(Object.getLastValue(Object.getColumnIndexByName('UMTS_LTE_Redirect_With_CSFB_Single_RAB_SuccessCount'))) + int(Object.getLastValue(Object.getColumnIndexByName('UMTS_LTE_Redirect_With_CSFB_Multi_RAB_SuccessCount')))))

def CSFB_UMTS_To_LTE_Reselection_Failure_Single_RAB(Object):
	return dropCountCalculator('UMTS_LTE_Redirect_With_CSFB_Single_RAB_AttemptCount','UMTS_LTE_Redirect_With_CSFB_Single_RAB_SuccessCount',Object)

def CSFB_UMTS_To_LTE_Reselection_Failure_Multi_RAB(Object):
	return dropCountCalculator('UMTS_LTE_Redirect_With_CSFB_Multi_RAB_AttemptCount','UMTS_LTE_Redirect_With_CSFB_Multi_RAB_SuccessCount',Object)

def LTE_IRAT_Success_Rate_Redirection_PS_Only_Single_RAB(Object):
	return successRateCalculator('LTE_IRAT_Redirect_PS_Only_Single_RAB_AttemptCount','LTE_IRAT_Redirect_PS_Only_Single_RAB_SuccessCount',Object)

def LTE_IRAT_Success_Rate_Redirection_PS_Only_Multi_RAB(Object):
	return successRateCalculator('LTE_IRAT_Redirect_PS_Only_Multi_RAB_AttemptCount','LTE_IRAT_Redirect_PS_Only_Multi_RAB_SuccessCount',Object)

def Total_CSFB_PS_Drop_in_WCDMA_Count(Object):
	try:
		a = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_After_ESR_MO_in_WCDMA_Drop_Count')))
		b = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_After_ESR_MT_in_WCDMA_Drop_Count')))
		c = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_Drop_with_CSFB_MO_in_WCDMA')))
		d = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_Drop_with_CSFB_MT_in_WCDMA')))
		return (a+b+c+d)
	except Exception:
		logging.warning('error in Total_CSFB_PS_Drop_in_WCDMA_Count')
		return ''
		
def Total_PS_Drop_LTE_Count(Object):
	try:
		a = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_Single_RAB_Drop')))
		b = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_Multi_RAB_During_CSFB_Drop')))
		c = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_Only_Multi_RAB_Drop')))
		return (a+b+c)
	except Exception:
		logging.warning('error in Total_PS_Drop_LTE_Count')
		return ''
def LTE_RRC_Drop_Count(Object):
	try:
		a = int(Object.getLastValue(Object.getColumnIndexByName('LTE_RRC_Drop_Count')))
		return (a)
	except Exception:
		logging.warning('error in LTE_RRC_Drop_Count')
		return ''
		
def PS_With_CSFB_MO_Retainability_Rate(Object):
	return successRateCalculator('PS_With_CSFBMO_SuccessCount','PS_with_CSFB_MO_Release_in_WCDMA_Count',Object)

def PS_With_CSFB_MT_Retainability_Rate(Object):
	return successRateCalculator('PS_With_CSFBMT_SuccessCount','PS_with_CSFB_MT_Release_in_WCDMA_Count',Object)

def LTE_PS_After_ESR_MO_Retainability_Rate_in_WCDMA(Object):
	return successRateCalculator('LTE_PS_After_ESR_MO_in_WCDMA_Success_Count','LTE_PS_After_ESR_MO_in_WCDMA_First_Release_Count',Object)

def LTE_PS_After_ESR_MT_Retainability_Rate_in_WCDMA(Object):
	return successRateCalculator('LTE_PS_After_ESR_MT_in_WCDMA_Success_Count','LTE_PS_After_ESR_MT_in_WCDMA_First_Release_Count',Object)

def Total_CSFB_PS_in_WCDMA_Release_Count(Object):
	try:
		a = int(Object.getLastValue(Object.getColumnIndexByName('PS_with_CSFB_MO_Release_in_WCDMA_Count')))
		b = int(Object.getLastValue(Object.getColumnIndexByName('PS_with_CSFB_MT_Release_in_WCDMA_Count')))
		c = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_After_ESR_MO_in_WCDMA_First_Release_Count')))
		d = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_After_ESR_MT_in_WCDMA_First_Release_Count')))
		return (a+b+c+d)
	except Exception:
		logging.warning('error in Total_CSFB_PS_in_WCDMA_Release_Count')
		return ''
def Total_CSFB_PS_Retainability_in_WCDMA(Object):
	try:
		release = Total_CSFB_PS_in_WCDMA_Release_Count(Object)
		success = Total_CSFB_PS_in_WCDMA_Connection_Count(Object)
		return	(release*100.0/success)
	except Exception:
		logging.warning('Error Denominator in Total_CSFB_PS_Retainability_in_WCDMA ')
		return ''
def Total_WCDMA_PS_Retainability_Rate(ObjectWCDMA, ObjectLTE):
	try:
		a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('PS_with_CSFB_MO_Release_in_WCDMA_Count')))
		b = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('PS_with_CSFB_MT_Release_in_WCDMA_Count')))
		c = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('LTE_PS_After_ESR_MO_in_WCDMA_Release_Count')))
		d = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('LTE_PS_After_ESR_MT_in_WCDMA_Release_Count')))
		release_WCDMA = Total_PS_WCDMA_Only_Release_Count(ObjectWCDMA)
		release_LTE =a+b+c+d
		success_LTE = Total_CSFB_PS_in_WCDMA_Connection_Count(ObjectLTE)
		success_WCDMA = Total_PS_WCDMA_Only_Count(ObjectWCDMA)
			
		return	(release_LTE+release_WCDMA)*100.0/(success_LTE+success_WCDMA)
	except Exception:
		logging.warning('Error Denominator in Total_WCDMA_PS_Retainability_Rate ')
		return ''
		
def Overall_PS_Retainability(ObjectWCDMA,ObjectLTE):
	try:
#		release_CSFB = Total_LTE_PS_ReleaseCount_in_WCDMA(ObjectLTE)
		release_WCDMA =Total_PS_WCDMA_Only_Release_Count(ObjectWCDMA)
		release_LTE = LTE_PS_Release_total(ObjectLTE)
		release_CSFB = Total_CSFB_PS_in_WCDMA_Release_Count(ObjectLTE)
		print release_CSFB
		print release_LTE
		print release_WCDMA
#		success = Total_LTE_PS_Successful_Resume_in_WCDMA_Count(Object)
	
		success_Resume = LTE_PS_After_ESR_Success_resume(ObjectLTE) + PS_With_CSFB_Success(ObjectLTE)
		success_WCDMA = Total_PS_WCDMA_Only_Count(ObjectWCDMA)
		success_LTE =  Total_LTE_PS_Connection_Count(ObjectLTE)

		release = release_LTE+release_WCDMA+release_CSFB
		success = success_LTE+success_WCDMA+success_Resume
		return	(release*100.0)/success
	except Exception:
		logging.warning('Error Denominator in Overall_PS_Retainability ')
		return ''

def PS_Retainability_with_CSFB_MO_in_WCDMA(Object):
	"""
	return the retainability rate PS_Retainability_with_CSFB_MO_in_WCDMA
	"""
	return successRateCalculator('LTE_PS_With_CSFB_MO_Successful_Resume_in_WCDMA_Count','anovaLTE_PS_With_CSFBMO_First_ReleaseCount_in_WCDMA',Object)
def PS_Retainability_with_CSFB_MT_in_WCDMA(Object):
	"""
	return the retainability rate PS_Retainability_with_CSFB_MT_in_WCDMA
	"""
	return successRateCalculator('LTE_PS_With_CSFB_MT_Successful_Resume_in_WCDMA_Count','anovaLTE_PS_With_CSFBMT_First_ReleaseCount_in_WCDMA',Object)
def PS_Retainability_After_ESR_MO_in_WCDMA(Object):
	"""
	return the retainability rate PS_Retainability_After_ESR_MO_in_WCDMA
	"""
	return successRateCalculator('LTE_PS_After_ESR_MO_Successful_Resume_in_WCDMA_Count','LTE_PS_After_ESR_MO_in_WCDMA_First_Release_Count',Object)
def PS_Retainability_After_ESR_MT_in_WCDMA(Object):
	"""
	return the retainability rate PS_Retainability_After_ESR_MT_in_WCDMA
	"""
	return successRateCalculator('LTE_PS_After_ESR_MT_Successful_Resume_in_WCDMA_Count','LTE_PS_After_ESR_MT_in_WCDMA_First_Release_Count',Object)

def PS_Retainability_LTE_to_UMTS_Redirection_CSFB(Object):
	return percantageCalculator('LTE_PS_With_CSFB_MO_Successful_Resume_in_WCDMA_Count','LTE_PS_With_CSFB_MT_Successful_Resume_in_WCDMA_Count','anovaLTE_PS_With_CSFBMT_First_ReleaseCount_in_WCDMA','anovaLTE_PS_With_CSFBMO_First_ReleaseCount_in_WCDMA',Object)
	

def Total_LTE_PS_ReleaseCount_in_WCDMA(Object):
	try:
		a = int(Object.getLastValue(Object.getColumnIndexByName('anovaLTE_PS_With_CSFBMO_First_ReleaseCount_in_WCDMA')))
		b = int(Object.getLastValue(Object.getColumnIndexByName('anovaLTE_PS_With_CSFBMT_First_ReleaseCount_in_WCDMA')))
		c = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_After_ESR_MO_in_WCDMA_First_Release_Count')))
		d = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_After_ESR_MT_in_WCDMA_First_Release_Count')))
		return (a+b+c+d)
	except Exception:
		logging.warning('error in Total_LTE_PS_ReleaseCount_in_WCDMA')
def LTE_PS_After_ESR_Success_resume(Object):
	c = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_After_ESR_MO_Successful_Resume_in_WCDMA_Count')))
	d = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_After_ESR_MT_Successful_Resume_in_WCDMA_Count')))
	return (c+d)
	
def Total_LTE_PS_Successful_Resume_in_WCDMA_Count(Object):
	try:
		a = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_With_CSFB_MO_Successful_Resume_in_WCDMA_Count')))
		b = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_With_CSFB_MT_Successful_Resume_in_WCDMA_Count')))
		c = LTE_PS_After_ESR_Success_resume(Object)
		return (a+b+c)
	except Exception:
		logging.warning('error in Total_LTE_PS_Successful_Resume_in_WCDMA_Count')

def Total_PS_Retainability_CSFB_in_WCDMA(Object):
	try:
		release = Total_LTE_PS_ReleaseCount_in_WCDMA(Object)
		success = Total_LTE_PS_Successful_Resume_in_WCDMA_Count(Object)
		rate = (release * 100.0)/success
		return rate
	except Exception:
		logging.warning('denominator error in Total_PS_Retainability_CSFB_in_WCDMA')

def Total_CS_MO_Multi_RAB_Retainability(ObjectWCDMA, ObjectLTE):
	try:
		a = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('novaWCDMA_CSMO_MultiRAB_SuccessfulReleaseCount')))
		b = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MO_Multi_RAB_SuccessfulReleaseCount')))
		c = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMO_MultiRAB_SuccessCount')))
		d = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MO_Multi_RAB_SuccessCount')))
		rate = (a + b)*100.0/(c + d)
		return rate
	except Exception:
		logging.warning('denominator error in Total_CS_MO_Multi_RAB_Retainability')

def Total_CS_MO_Single_RAB_Retainability(ObjectWCDMA, ObjectLTE):
	try:
		a = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_SuccessfulReleaseCount')))
		b = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessfulReleaseCount')))
		c = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_SuccessCount')))
		d = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessCount')))
		rate = (a + b)*100.0/(c + d)
		return rate
	except Exception:
		logging.warning('denominator error in Total_CS_MO_Single_RAB_Retainability')
def Total_PS_Accessibility_WCDMA_Only(Object):
	try:
		attempt = Total_WCDMA_Only_PS_Attempt(Object)     
		success = Total_PS_WCDMA_Only_Count(Object)
		rate = success * 100.0/attempt
		return rate
	except Exception:
		logging.warning('denominator error in Total_PS_Accessibility_WCDMA_Only')
def UMTS_LTE_CSFB_Reselect_Success_Rate(Object):
	return successRateCalculator('anovaUMTS_LTE_CSFB_Reselect_AttemptCount','anovaUMTS_LTE_CSFB_Reselect_SuccessCount',Object)
def UMTS_LTE_CSFB_Reselect_Failure_Rate(Object):
	return successRateCalculator('anovaUMTS_LTE_CSFB_Reselect_AttemptCount','anovaUMTS_LTE_CSFB_Reselect_DropCount',Object)

def PS_Accessibility_LTE_to_UMTS_Redirection_CSFB(ObjectLTE):
	try:
		MO_resume_success = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('LTE_PS_With_CSFB_MO_Successful_Resume_in_WCDMA_Count')))
		MT_resume_success = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('LTE_PS_With_CSFB_MT_Successful_Resume_in_WCDMA_Count')))
		MO_attempt = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('PS_With_CSFBMO_AttemptCount')))
		MT_attempt = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('PS_With_CSFBMT_AttemptCount')))
		PS_Retainability = (MO_resume_success + MT_resume_success)*100.0/(MO_attempt + MT_attempt)
		return	PS_Retainability
	except Exception:
		logging.warning('Error Denominator in PS_Accessibility_LTE_to_UMTS_Redirection_CSFB ')
		return ''
########################################################################LTE_Counter_Object + WCDMA_GSM_COUNTER_OBJECT###################
def Overall_PS_Attempts(ObjectWCDMA,ObjectLTE):
	try:
		CSFB_attempt = Total_CSFB_PS_in_WCDMA_Attempt(ObjectLTE)
		WCDMA_attempt = Total_WCDMA_Only_PS_Attempt(ObjectWCDMA)
		LTE_attempt = Total_LTE_PS_Attempt(ObjectLTE)
		return (CSFB_attempt+WCDMA_attempt+LTE_attempt)
	except Exception:
		logging.warning('one of the passed list is empty in Overall_PS_Attempts')
		return ''
def Overall_PS_Connection_Count(ObjectWCDMA,ObjectLTE):
	try:
		CSFB_success = Total_CSFB_PS_in_WCDMA_Connection_Count(ObjectLTE)
		WCDMA_success = Total_PS_WCDMA_Only_Count(ObjectWCDMA)
		LTE_success = Total_LTE_PS_Connection_Count(ObjectLTE)
		
		return (CSFB_success+WCDMA_success+LTE_success)
	except Exception:
		logging.warning('one of the passed list is empty in Overall_PS_Connection_Count')
		return ''

def Overall_PS_Setup_Success_Rate(ObjectOne,ObjectTwo):
	try:
		Temp_total_PS_Attempt = int(Overall_PS_Attempts(ObjectOne,ObjectTwo))
		Temp_total_PS_Success = int(Overall_PS_Connection_Count(ObjectOne,ObjectTwo))					
		return Temp_total_PS_Success*100.0/Temp_total_PS_Attempt
	except Exception:
		logging.warning('Overall_PS_Attempts is zero')
		return ''

def Total_CS_MO_Multi_RAB_Attempts(ObjectOne,ObjectTwo):
	try:
		CSFB_MO_Multi_RAB_AttemptCount = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MO_Multi_RAB_AttemptCount')))
		anovaWCDMA_CSMO_MultiRAB_AttemptCount = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_CSMO_MultiRAB_AttemptCount')))
		return (CSFB_MO_Multi_RAB_AttemptCount+anovaWCDMA_CSMO_MultiRAB_AttemptCount)
	except Exception:
		logging.warning('CSFB_MO_Multi_RAB_AttemptCount is empty in Total_CS_MO_Multi_RAB_Attempts')
		return ''

def Total_CS_MO_Single_RAB_Attempts(ObjectOne,ObjectTwo):
	try:
		CSFB_MO_Single_RAB_AttemptCount = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MO_Single_RAB_AttemptCount')))
		anovaWCDMA_CSMO_SingleRAB_AttemptCount = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_AttemptCount')))
		return (CSFB_MO_Single_RAB_AttemptCount+anovaWCDMA_CSMO_SingleRAB_AttemptCount)
	except Exception:
		logging.warning('CSFB_MO_Single_RAB_AttemptCount is empty in Total_CS_MO_Single_RAB_Attempts')
		return ''

def Total_CS_MT_Multi_RAB_Attempts(ObjectOne,ObjectTwo):
	try:
		CSFB_MT_Multi_RAB_AttemptCount = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MT_Multi_RAB_AttemptCount')))
		WCDMA_CMServReqCount_MT_Multi_RAB = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('WCDMA_CMServReqCount_MT_Multi_RAB')))
		return (CSFB_MT_Multi_RAB_AttemptCount+WCDMA_CMServReqCount_MT_Multi_RAB)
	except Exception:
		logging.warning('CSFB_MT_Multi_RAB_AttemptCount is empty in Total_CS_MT_Multi_RAB_Attempts')
		return ''

def Total_CS_MT_Single_RAB_Attempts(ObjectOne,ObjectTwo):
	try:
		CSFB_MT_Single_RAB_AttemptCount = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MT_Single_RAB_AttemptCount')))
		WCDMA_CMServReqCount_MT_Single_RAB = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('WCDMA_CMServReqCount_MT_Single_RAB')))
		return (CSFB_MT_Single_RAB_AttemptCount+WCDMA_CMServReqCount_MT_Single_RAB)
	except Exception:
		logging.warning('CSFB_MT_Single_RAB_AttemptCount is empty in Total_CS_MT_Single_RAB_Attempts')
		return ''

def Total_CS_MO_Single_RAB_Success_Rate(ObjectOne,ObjectTwo):
	try:
		Total_CS_MO_Single_RAB_Attempts = Total_CS_MO_Single_RAB_Attempts(ObjectOne,ObjectTwo)
		WCDMA_CS_AlertCount_MO_Single = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_SuccessCount')))
		CSFB_MO_Single_RAB_SuccessCount = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessCount')))
		return (WCDMA_CS_AlertCount_MO_Single + CSFB_MO_Single_RAB_SuccessCount)*100.0/Total_CS_MO_Single_RAB_Attempts
	except Exception:
		logging.warning('error while caculating Total_CS_MO_Single_RAB_Success_Rate')
		return ''

def Total_CS_MO_Multi_RAB_Success_Rate(ObjectOne,ObjectTwo):
	try:
		Total_CS_MO_Multi_RAB_Attempts = Total_CS_MO_Multi_RAB_Attempts(ObjectOne,ObjectTwo)
		WCDMA_CS_AlertCount_MO_Multi = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_CSMO_MultiRAB_SuccessCount')))
		CSFB_MO_Multi_RAB_SuccessCount = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MO_Multi_RAB_SuccessCount')))
		return (WCDMA_CS_AlertCount_MO_Multi + CSFB_MO_Multi_RAB_SuccessCount)*100.0/Total_CS_MO_Multi_RAB_Attempts
	except Exception:
		logging.warning('error while caculating Total_CS_MO_Multi_RAB_Success_Rate')
		return ''

def Total_CS_MT_Single_RAB_Success_Rate(ObjectOne,ObjectTwo):
	try:
		Total_CS_MT_Single_RAB_Attempts = Total_CS_MT_Single_RAB_Attempts(ObjectOne,ObjectTwo)
		WCDMA_CS_AlertCount_MT_Single = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_CSMT_SingleRAB_SuccessCount')))
		CSFB_MT_Single_RAB_SuccessCount = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessCount')))
		return (WCDMA_CS_AlertCount_MT_Single + CSFB_MT_Single_RAB_SuccessCount)*100.0/Total_CS_MT_Single_RAB_Attempts
	except Exception:
		logging.warning('error while caculating Total_CS_MT_Single_RAB_Success_Rate')
		return ''

def Total_CS_MT_Multi_RAB_Success_Rate(ObjectOne,ObjectTwo):
	try:
		Total_CS_MT_Multi_RAB_Attempts = Total_CS_MT_Multi_RAB_Attempts(ObjectOne,ObjectTwo)
		WCDMA_CS_AlertCount_MT_Multi = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_CSMT_MultiRAB_SuccessCount')))
		CSFB_MT_Multi_RAB_SuccessCount = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MT_Multi_RAB_SuccessCount')))
		return (WCDMA_CS_AlertCount_MT_Multi + CSFB_MT_Multi_RAB_SuccessCount)*100.0/Total_CS_MT_Multi_RAB_Attempts
	except Exception:
		logging.warning('error while caculating Total_CS_MT_Multi_RAB_Success_Rate')
		return ''

def Overall_CS_Setup_Success_Rate(ObjectOne,ObjectTwo):
	try:
		return (int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_SuccessCount'))) + int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessCount'))) + int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_CSMO_MultiRAB_SuccessCount'))) + int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MO_Multi_RAB_SuccessCount'))) + int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_CSMT_SingleRAB_SuccessCount'))) + int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessCount'))) + int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_CSMT_MultiRAB_SuccessCount'))) + int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MT_Multi_RAB_SuccessCount'))))*100 / (int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_AttemptCount'))) + int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MO_Single_RAB_AttemptCount'))) + int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_CSMO_MultiRAB_AttemptCount'))) + int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MO_Multi_RAB_AttemptCount'))) + int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_CSMT_SingleRAB_AttemptCount'))) + int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MT_Single_RAB_AttemptCount'))) + int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_CSMT_MultiRAB_AttemptCount'))) + int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('CSFB_MT_Multi_RAB_AttemptCount'))))
	except Exception:
		logging.warning('error while calculating Overall_CS_Setup_Success_Rate')
		return ''
def LTE_PS_Retainability_Single_RAB(Object):
	return successRateCalculator('LTE_PS_Single_RAB_SuccessCount','LTE_PS_Single_RAB_Successful_ReleaseCount',Object)
def LTE_PS_Retainability_Multi_RAB_During_CSFB(Object):
	return successRateCalculator('LTE_PS_Multi_RAB_SuccessCount','LTE_PS_Multi_RAB_Successful_ReleaseCount',Object)
def LTE_PS_Retainability_PS_Only_Multi_RAB(Object):
	return successRateCalculator('LTE_PS_Only_Multi_RAB_SuccessCount','LTE_PS_Only_Multi_RAB_Successful_ReleaseCount',Object)
def Total_LTE_PS_Connection_Count(Object):
	try:
		a = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_Single_RAB_SuccessCount')))
		b = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_Multi_RAB_SuccessCount')))
		c = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_Only_Multi_RAB_SuccessCount')))
#		print "Total_LTE_PS_Connection_Count a=%d b=%d c=%d"%(a,b,c)
		return (a+b+c)
	except Exception:
		logging.warning('error in LTE_PS_Success')
		return ''
def Total_LTE_PS_Attempt(ObjectTwo):
	try:
		a = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('LTE_PS_Single_RAB_AttemptCount')))
		b = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('LTE_PS_Multi_RAB_AttemptCount')))
		c = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('LTE_PS_Only_Multi_RAB_AttemptCount')))
		return (a+b+c)
	except Exception:
		logging.warning('error in Total_LTE_PS_Attempt')
		return ''
def LTE_PS_Release_total(Object):
	try:
		d = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_Single_RAB_Successful_ReleaseCount')))
		e = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_Multi_RAB_Successful_ReleaseCount')))
		f = int(Object.getLastValue(Object.getColumnIndexByName('LTE_PS_Only_Multi_RAB_Successful_ReleaseCount')))
		return (d+e+f)
	except Exception:
		logging.warning('error in LTE_PS_Release_total')
		return ''

def LTE_PS_Overall_Retainability(Object):
	try:
		success = Total_LTE_PS_Connection_Count(Object)
		release = LTE_PS_Release_total(Object)
		return release*100.0/success
	except Exception:
		logging.warning('denominator zero in LTE_PS_Overall_Retainability')
		return ''
def Overall_PS_Connection_Count_Count(ObjectOne, ObjectTwo):
	try:
		WCDMA_Single_RAB_Success = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_PS_SingleRAB_SuccessCount')))
		WCDMA_Multi_RAB_Success =int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_PS_MultiRAB_SuccessCount')))

		LTE_success = Total_LTE_PS_Connection_Count(ObjectTwo)

		total = WCDMA_Single_RAB_Success+WCDMA_Multi_RAB_Success+LTE_success
		return total
	except Exception:
		logging.warning('Error While calculatiing Overall_PS_Connection_Count_count')
		return ''
def Overall_PS_Accessibility(ObjectOne, ObjectTwo):
	try:
		success_total = Overall_PS_Connection_Count_Count(ObjectOne, ObjectTwo) + Total_CSFB_PS_in_WCDMA_Connection_Count(ObjectTwo)
		WCDMA_Single_RAB_Attempt = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_PS_SingleRAB_AttemptCount')))
		WCDMA_Multi_RAB_Attempt = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_PS_MultiRAB_AttemptCount')))

		LTE_Attempt = Total_LTE_PS_Attempt(ObjectTwo)
		wcdma_attempt = Total_CSFB_PS_in_WCDMA_Attempt(ObjectTwo)
                return (success_total*100.0)/(WCDMA_Single_RAB_Attempt+WCDMA_Single_RAB_Attempt+LTE_Attempt+wcdma_attempt)
	except Exception:
		logging.warning('Error While calculatiing Overall_PS_Accessibility denominator zero')
		return ''
'''
#def Overall_PS_Retainability(ObjectOne, ObjectTwo):
	try:
		
		WCDMA_Single_RAB_Release = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_PS_SingleRAB_SuccessfulReleaseCount')))
		WCDMA_Multi_RAB_Release = int(ObjectOne.getLastValue(ObjectOne.getColumnIndexByName('anovaWCDMA_PS_MultiRAB_SuccessfulReleaseCount')))
		LTE_Single_RAB_Release = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('LTE_PS_Single_RAB_Successful_ReleaseCount ')))
		LTE_Multi_RAB_Release= int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('LTE_PS_Multi_RAB_Successful_ReleaseCount')))
		LTE_Only_Multi_RAB_Release = int(ObjectTwo.getLastValue(ObjectTwo.getColumnIndexByName('LTE_PS_Only_Multi_RAB_Successful_ReleaseCount')))
		
		success_total = Overall_PS_Connection_Count_Count(ObjectOne, ObjectTwo)
		
		release = WCDMA_Single_RAB_Release+WCDMA_Multi_RAB_Release+LTE_Single_RAB_Release+LTE_Multi_RAB_Release+LTE_Only_Multi_RAB_Release
		
                return release*100.0/success_total
	except Exception:
		logging.warning('Error While calculatiing Overall_PS_Retainability denominator zero')
		return ''
'''
def Overall_CS_Accessibility(ObjectOne, ObjectTwo):
	try:
		CS_Alert_total= Total_WCDMA_CS_AlertCount(ObjectOne)
		CM_ServReq_Setup= Total_WCDMA_CM(ObjectOne)
		success = Overall_CSFB_Success_Count(ObjectTwo)
		attempt = Overall_CSFB_Attempt_Count(ObjectTwo)
	
                return (CS_Alert_total+success)*100.0/(CM_ServReq_Setup+attempt)
	except Exception:
		logging.warning('Error While calculatiing Overall_CS_Accessibility denominator zero')
		return ''
def Overall_CS_Retainability(ObjectOne, ObjectTwo):
	try:
		CS_Alert_total= Total_WCDMA_CS_AlertCount(ObjectOne)
		CS_Disconnect_total= Overall_WCDMA_CS_Disconnect(ObjectOne)
		success = Overall_CSFB_Success_Count(ObjectTwo)
		disconnect =Overall_CSFB_SuccessfulRelease_Count(ObjectTwo)
                return (CS_Disconnect_total + disconnect)*100.0/(CS_Alert_total + success)
	except Exception:
		logging.warning('Error While calculatiing Overall_CS_Retainability denominator zero')
		return ''
		
def LTE_PS_Accessibility_Total(Object):
	try:
		success = Total_LTE_PS_Connection_Count(Object)
		attempt = Total_LTE_PS_Attempt(Object)
                return (success)*100.0/(attempt)
	except Exception:
		logging.warning('Error While calculatiing LTE_PS_Accessibility_Total denominator zero')
		return ''

def LTE_PS_Accessibility_PS_Only_Multi_RAB(Object):
	return successRateCalculator('LTE_PS_Only_Multi_RAB_AttemptCount','LTE_PS_Only_Multi_RAB_SuccessCount',Object)

def Total_PS_Drop_WCDMA_Count(ObjectWCDMA, ObjectLTE):
	try:
		a = Total_PS_Drop_WCDMA_Only_Count(ObjectWCDMA)
		b = Total_CSFB_PS_Drop_in_WCDMA_Count(ObjectLTE)
		return (a+b)
	except Exception:
		logging.warning('error in Total_PS_Drop_WCDMA_Count')
		return ''
	
def Overall_PS_Drop_Count(ObjectWCDMA, ObjectLTE):
	try:
		a = Total_PS_Drop_WCDMA_Only_Count(ObjectWCDMA)
		b = Total_CSFB_PS_Drop_in_WCDMA_Count(ObjectLTE)
		c = Total_PS_Drop_LTE_Count(ObjectLTE)
		return (a+b+c)
	except Exception:
		logging.warning('error in Overall_PS_Drop_Count')
		return ''


def Overall_CS_Single_RAB_Access_Time(ObjectWCDMA_C,ObjectWCDMA_K,ObjectLTE_C,ObjectLTE_K):
	try:
		one = ObjectLTE_K.getAllColumnValuesByIndex(ObjectLTE_K.getColumnIndexByName('CSFB_MO_Single_RAB_ConnectTime'))
		two = ObjectLTE_K.getAllColumnValuesByIndex(ObjectLTE_K.getColumnIndexByName('CSFB_MT_Single_RAB_ConnectTime'))
		three = ObjectWCDMA_K.getAllColumnValuesByIndex(ObjectWCDMA_K.getColumnIndexByName('WCDMA_CS_MOCALL_SINGLE_RAB_CONNECT_TIME'))
		four = ObjectWCDMA_K.getAllColumnValuesByIndex(ObjectWCDMA_K.getColumnIndexByName('WCDMA_CS_MTCALL_SINGLE_RAB_CONNECT_TIME'))
		colList = two + one + three +four

		a = int(ObjectLTE_C.getLastValue(ObjectLTE_C.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessCount')))
		b = int(ObjectLTE_C.getLastValue(ObjectLTE_C.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessCount')))
		c = int(ObjectWCDMA_C.getLastValue(ObjectWCDMA_C.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_SuccessCount')))
		d = int(ObjectWCDMA_C.getLastValue(ObjectWCDMA_C.getColumnIndexByName('anovaWCDMA_CSMT_SingleRAB_SuccessCount')))
		add = a + b + c + d

		colList = filter(None, colList)
                colList = filter(lambda a: a != ' ', colList)
                colList = map(float, colList)
                avg = sum(colList)/(add*1000)        # In second

                return avg
	except Exception:
		logging.warning('Error in Overall_CS_Single_RAB_Access_Time')
		return ''
def Overall_PS_Setup_Success_Rate(ObjectWCDMA, ObjectLTE):
	try:
		
		a = Total_PS_WCDMA_Only_Count(ObjectWCDMA)	#include 2 kpi
		b =  Total_LTE_PS_Connection_Count(ObjectLTE)	#include 3 kpi
		c = Total_CSFB_PS_in_WCDMA_Connection_Count(ObjectLTE)	#include 4 kpi
		success = a + b + c

		d = Total_WCDMA_Only_PS_Attempt(ObjectWCDMA)
		e = Total_LTE_PS_Attempt(ObjectLTE)
		f = Total_CSFB_PS_in_WCDMA_Attempt(ObjectLTE)
		attempt = d + e + f
		return success*100.0/attempt
	except Exception:
		logging.warning('Error in Overall_PS_Setup_Success_Rate')
		return ''
def sum_List_element(colList, typeTomap = float):
		colList = filter(None, colList)
		colList = filter(lambda a: a != ' ', colList)
		colList = map(typeTomap, colList)
		sum_result = sum(colList)
		return sum_result
def Calculate_mean(colList):
	'''
	This function calculate the mean of List by maping it to float
	'''
	try:
		temp_sum = sum_List_element(colList) #, typeTomap = float)
		mean = int(temp_sum/len(colList))
		return mean
	except Exception:
		logging.warning('Error Denominator- While Calculating Mean')
		return ''
def Overall_CS_MO_Single_RAB_Mean_Call_Connect_Time(ObjectWCDMA, ObjectLTE):		
	try:
		one = ObjectWCDMA.getAllColumnValuesByIndex(ObjectWCDMA.getColumnIndexByName('WCDMA_CS_MOCALL_SINGLE_RAB_CONNECT_TIME'))
		two = ObjectLTE.getAllColumnValuesByIndex(ObjectLTE.getColumnIndexByName('CSFB_MO_Single_RAB_ConnectTime'))
		colList = one + two
		return Calculate_mean(colList)
	except Exception:
		logging.warning('some error in  Overall_CS_MO_Single_RAB_Mean_Call_Connect_Time')
		return ''
def Overall_CS_MO_Multi_RAB_Mean_Call_Connect_Time(ObjectWCDMA, ObjectLTE):		
	try:
		one = ObjectWCDMA.getAllColumnValuesByIndex(ObjectWCDMA.getColumnIndexByName('WCDMA_CS_MOCALL_MULTIPLE_RAB_CONNECT_TIME'))
		two = ObjectLTE.getAllColumnValuesByIndex(ObjectLTE.getColumnIndexByName('CSFB_MO_Multi_RAB_ConnectTime'))
		colList = one + two
		return Calculate_mean(colList)
	except Exception:
		logging.warning('some error in  Overall_CS_MO_Multi_RAB_Mean_Call_Connect_Time')
		return ''
def Overall_CS_MT_Access_Mean_Call_Connect_Time(ObjectWCDMA, ObjectLTE):		
	try:
		csfb_mt = CSFB_MT_ConnectTime(ObjectLTE)
		wcdma_cs = WCDMA_CS_MTCALL_CONNECT_TIME(ObjectWCDMA)
		colList = csfb_mt + wcdma_cs
		mean = Calculate_mean(colList)
		return mean
	except Exception:
		logging.warning('some error in  Overall_CS_MT_Access_Mean_Call_Connect_Time')
		return ''

def Overall_CS_Single_RAB_Access_Time(ObjectWCDMA_C,ObjectWCDMA_K,ObjectLTE_C,ObjectLTE_K):
	try:
		one = ObjectLTE_K.getAllColumnValuesByIndex(ObjectLTE_K.getColumnIndexByName('CSFB_MO_Single_RAB_ConnectTime'))
		two = ObjectLTE_K.getAllColumnValuesByIndex(ObjectLTE_K.getColumnIndexByName('CSFB_MT_Single_RAB_ConnectTime'))
		three = ObjectWCDMA_K.getAllColumnValuesByIndex(ObjectWCDMA_K.getColumnIndexByName('WCDMA_CS_MOCALL_SINGLE_RAB_CONNECT_TIME'))
		four = ObjectWCDMA_K.getAllColumnValuesByIndex(ObjectWCDMA_K.getColumnIndexByName('WCDMA_CS_MTCALL_SINGLE_RAB_CONNECT_TIME'))
		colList = two + one + three +four

		a = int(ObjectLTE_C.getLastValue(ObjectLTE_C.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessCount')))
		b = int(ObjectLTE_C.getLastValue(ObjectLTE_C.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessCount')))
		c = int(ObjectWCDMA_C.getLastValue(ObjectWCDMA_C.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_SuccessCount')))
		d = int(ObjectWCDMA_C.getLastValue(ObjectWCDMA_C.getColumnIndexByName('anovaWCDMA_CSMT_SingleRAB_SuccessCount')))
		add = a + b + c + d

		colList = filter(None, colList)
                colList = filter(lambda a: a != ' ', colList)
                colList = map(float, colList)
                avg = sum(colList)/(add*1000)        # In second

                return avg
	except Exception:
		logging.warning('Error in Overall_CS_Single_RAB_Access_Time')
		return ''
def Overall_PS_Setup_Success_Rate(ObjectWCDMA, ObjectLTE):
	try:
		
		a = Total_PS_WCDMA_Only_Count(ObjectWCDMA)	#include 2 kpi
		b =  Total_LTE_PS_Connection_Count(ObjectLTE)	#include 3 kpi
		c = Total_CSFB_PS_in_WCDMA_Connection_Count(ObjectLTE)	#include 4 kpi
		success = a + b + c

		d = Total_WCDMA_Only_PS_Attempt(ObjectWCDMA)
		e = Total_LTE_PS_Attempt(ObjectLTE)
		f = Total_CSFB_PS_in_WCDMA_Attempt(ObjectLTE)
		attempt = d + e + f
		return success*100.0/attempt
	except Exception:
		logging.warning('Error in Overall_PS_Setup_Success_Rate')
		return ''
def sum_List_element(colList, typeTomap = float):
		colList = filter(None, colList)
		colList = filter(lambda a: a != ' ', colList)
		colList = map(typeTomap, colList)
		sum_result = sum(colList)
		return sum_result
def Calculate_mean(colList):
	'''
	This function calculate the mean of List by maping it to float
	'''
	try:
		temp_sum = sum_List_element(colList) #, typeTomap = float)
		mean = temp_sum/len(colList)
		return mean
	except Exception:
		logging.warning('Error Denominator- While Calculating Mean')
		return ''
def Overall_CS_MO_Single_RAB_Mean_Call_Connect_Time(ObjectWCDMA, ObjectLTE):		
	try:
		one = ObjectWCDMA.getAllColumnValuesByIndex(ObjectWCDMA.getColumnIndexByName('WCDMA_CS_MOCALL_SINGLE_RAB_CONNECT_TIME'))
		two = ObjectLTE.getAllColumnValuesByIndex(ObjectLTE.getColumnIndexByName('CSFB_MO_Single_RAB_ConnectTime'))
		colList = one + two
		return Calculate_mean(colList)
	except Exception:
		logging.warning('some error in  Overall_CS_MO_Single_RAB_Mean_Call_Connect_Time')
		return ''
def Overall_CS_MO_Multi_RAB_Mean_Call_Connect_Time(ObjectWCDMA, ObjectLTE):		
	try:
		one = ObjectWCDMA.getAllColumnValuesByIndex(ObjectWCDMA.getColumnIndexByName('WCDMA_CS_MOCALL_MULTIPLE_RAB_CONNECT_TIME'))
		two = ObjectLTE.getAllColumnValuesByIndex(ObjectLTE.getColumnIndexByName('CSFB_MO_Multi_RAB_ConnectTime'))
		colList = one + two
		return Calculate_mean(colList)
	except Exception:
		logging.warning('some error in  Overall_CS_MO_Multi_RAB_Mean_Call_Connect_Time')
		return ''
def Overall_CS_MT_Access_Mean_Call_Connect_Time(ObjectWCDMA, ObjectLTE):		
	try:
		csfb_mt = CSFB_MT_ConnectTime(ObjectLTE)
		wcdma_cs = WCDMA_CS_MTCALL_CONNECT_TIME(ObjectWCDMA)
		colList = csfb_mt + wcdma_cs
		mean = Calculate_mean(colList)
		return mean
	except Exception:
		logging.warning('some error in  Overall_CS_MT_Access_Mean_Call_Connect_Time')
		return ''
'''
def Total_CS_MO_Single_RAB_Retainability(ObjectWCDMA, ObjectLTE):
	try:
		a = ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessfulReleaseCount'))
		b = ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_SuccessfulReleaseCount'))
		c = ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessCount'))
		d = ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_SuccessCount'))
		Retainability = (a+b)*100/(c+d)
		return Retainability
	except Exception:
		logging.warning('some error in  Total_CS_MO_Single_RAB_Retainability')
		return ''
'''		
def Total_CS_MO_Single_RAB_Setup_Success_Rate(ObjectWCDMA, ObjectLTE):
	try:
		a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessCount')))
		b = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_SuccessCount')))
		c = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MO_Single_RAB_AttemptCount')))
		d = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_AttemptCount')))
		sr = (a+b)*100.0/(c+d)
		return sr
	except Exception:
		logging.warning('some error in  Total_CS_MO_Single_RAB_Setup_Success_Rate')
		return ''
			
def Total_CS_MO_Multi_RAB_Setup_Success_Rate(ObjectWCDMA, ObjectLTE):
	try:
		a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MO_Multi_RAB_SuccessCount')))
		b = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMO_MultiRAB_SuccessCount')))
		c = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MO_Multi_RAB_AttemptCount')))
		d = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMO_MultiRAB_AttemptCount')))
		sr = (a+b)*100.0/(c+d)
		return sr
	except Exception:
		logging.warning('some error in  Total_CS_MO_Multi_RAB_Setup_Success_Rate')
		return ''
		
def Overall_CS_MT_Access_Attempts(ObjectWCDMA, ObjectLTE):
	try:
		a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MT_Single_RAB_AttemptCount')))
		b = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMT_SingleRAB_AttemptCount')))
		c = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MT_Multi_RAB_AttemptCount')))
		d = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMT_MultiRAB_AttemptCount')))
		sr = (a+b+c+d)
		return sr
	except Exception:
		logging.warning('some error in  Overall_CS_MT_Access_Attempts')
		return ''

def Overall_CS_MT_Success(ObjectWCDMA, ObjectLTE):
	try:
		a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessCount')))
		b = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMT_SingleRAB_SuccessCount')))
		c = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MT_Multi_RAB_SuccessCount')))
		d = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMT_MultiRAB_SuccessCount')))
		sr = (a+b+c+d)
		return sr
	except Exception:
		logging.warning('some error in  Overall_CS_MT_Success')
		return ''

def Overall_CS_MT_Access_Release(ObjectWCDMA, ObjectLTE):
	try:
		a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessfulReleaseCount')))
		b = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMT_SingleRAB_SuccessfulReleaseCount')))
		c = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MT_Multi_RAB_SuccessfulReleaseCount')))
		d =int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMT_MultiRAB_SuccessfulReleaseCount')))
		sr = (a+b+c+d)
		return sr
	except Exception:
		logging.warning('some error in  Overall_CS_MT_Access_Release')
		return ''

def Total_CS_MT_Access_Setup_Success_Rate(ObjectWCDMA, ObjectLTE):
	try:
		success = Overall_CS_MT_Success(ObjectWCDMA, ObjectLTE)
		attempt = Overall_CS_MT_Access_Attempts(ObjectWCDMA, ObjectLTE)
		
		sr = (success)*100.0/(attempt)
		return sr
	except Exception:
		logging.warning('denominator error in  Total_CS_MT_Access_Setup_Success_Rate')
		return ''

def Total_CS_MT_Retainability(ObjectWCDMA, ObjectLTE):
	try:
		success =Overall_CS_MT_Success(ObjectWCDMA, ObjectLTE)
		relese = Overall_CS_MT_Access_Release(ObjectWCDMA, ObjectLTE)
		
		sr = (relese)*100.0/(success)
		return sr
	except Exception:
		logging.warning('denominator error in Total_CS_MT_Retainability ')
		return ''
def Total_CS_MO_Single_RAB_Success_Count(ObjectWCDMA, ObjectLTE):
	a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MO_Single_RAB_SuccessCount')))
	b = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_SuccessCount')))
	ret = a+b
	return ret
def Total_CS_MO_Single_RAB_Drop_Count(ObjectWCDMA, ObjectLTE):
	a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('anovaCSFB_MO_SingleRAB_DropCount_in_WCDMA')))
	b = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMO_SingleRAB_DropCount')))
	ret = a+b
	return ret
def Total_CS_MO_Multi_RAB_Success_Count(ObjectWCDMA, ObjectLTE):
	a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MO_Multi_RAB_SuccessCount')))
	b = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMO_MultiRAB_SuccessCount')))
	ret = a+b
	return ret
def Total_CS_MO_Multi_RAB_Drop_Count(ObjectWCDMA, ObjectLTE):
	a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('anovaCSFB_MO_MultiRAB_DropCount_in_WCDMA')))
	b = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMO_MultiRAB_DropCount')))
	ret = a+b
	return ret

def Overall_CSFB_MT_DropCount(ObjectLTE):
	a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('anovaCSFB_MT_SingleRAB_DropCount_in_WCDMA')))
	b = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('anovaCSFB_MT_MultiRAB_DropCount_in_WCDMA')))
	ret = a+b
	return ret
def Overall_CS_MT_DropCount(ObjectWCDMA, ObjectLTE):
	CSFB = Overall_CSFB_MT_DropCount(ObjectLTE)
	a = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMT_SingleRAB_DropCount')))
	b = int(ObjectWCDMA.getLastValue(ObjectWCDMA.getColumnIndexByName('anovaWCDMA_CSMT_MultiRAB_DropCount')))
	ret = CSFB + a + b
	return ret

def Overall_CSFB_MT_Success(ObjectLTE):
	a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MT_Single_RAB_SuccessCount')))
	b = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('CSFB_MT_Multi_RAB_SuccessCount')))
	ret = a+b
	return ret

def Intra_LTE_HO_Attempt(ObjectLTE):
	try:
		a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('Intra_LTE_HO_Failure')))
		b = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('Intra_LTE_HO_Success')))
		return a+b
	except Exception:
		logging.warning(' error in Intra_LTE_HO_Attempt')

def Inter_LTE_HO_Attempt(ObjectLTE):
	try:
		a = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('Inter_LTE_HO_Failure')))
		b = int(ObjectLTE.getLastValue(ObjectLTE.getColumnIndexByName('Inter_LTE_HO_Success')))
		return a+b
	except Exception:
		logging.warning(' error in Inter_LTE_HO_Attempt')

########################################################################L3MessageObject#################################################
def Technology_split_GSM(Dict_of_time_in_technologies_L3Messages):
	return Dict_of_time_in_technologies_L3Messages['GSM']*100/Dict_of_time_in_technologies_L3Messages['Total']

def Technology_split_WCDMA(Dict_of_time_in_technologies_L3Messages):
	return Dict_of_time_in_technologies_L3Messages['WCDMA']*100/Dict_of_time_in_technologies_L3Messages['Total']

def Technology_split_LTE(Dict_of_time_in_technologies_L3Messages):
	return Dict_of_time_in_technologies_L3Messages['LTE']*100/Dict_of_time_in_technologies_L3Messages['Total']

def Local_time():
	"""
	return the the current time of the system
	"""
	localtime = time.asctime(time.localtime(time.time()))
	return localtime
	
def main(argv):
	'''This gets the argument from terminal in format python filename.py -i inputfolder'''
	inputstring = ''
	testfileid = ''

	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print "invalid input type input format python filename.py -i inputfolder"
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-i","--ifile"):
			inputstring = arg
		elif opt in ("-o","--ofile"):
			testfileid = arg
		else:
			print "invalid input type input format python filename.py -i inputfolder"
	testfileid = testfileid.strip()
	print 'Input String is "', inputstring
	print 'Test Id is "', testfileid
	#Getting path of the csv files
	GSMWCDMACOUNTERFILE = GSM_WCDMA_COUNTER_FILE_PATH(inputstring,testfileid)
	LTECOUNTERFILE = LTE_COUNTER_FILE_PATH(inputstring,testfileid)
	GSMWCDMAKPIFILE = SHORT_WCDMA_GSM_KPI_FILE(inputstring,testfileid)
	LTEKPIFILE = SHORT_LTE_KPI_FILE(inputstring,testfileid)
	L3MessagesFile = L3_Messages_FILE_PATH(inputstring,testfileid)
	#Creating object from the file path after uncompressing it from gzip format
	GSM_WCDMA_COUNTER_FILE = gzip.open(GSMWCDMACOUNTERFILE,'rb')
	LTE_COUNTER_FILE = gzip.open(LTECOUNTERFILE,'rb')
	GSM_WCDMA_KPI_FILE = gzip.open(GSMWCDMAKPIFILE,'rb')
	LTE_KPI_FILE = gzip.open(LTEKPIFILE,'rb')
	L3Messages_File = gzip.open(L3MessagesFile,'rb')
	GSM_WCDMA_COUNTER_OBJECT = ParseCSV(GSM_WCDMA_COUNTER_FILE)
	GSM_WCDMA_KPI_OBJECT = ParseCSV(GSM_WCDMA_KPI_FILE)
	LTE_KPI_OBJECT = ParseCSV(LTE_KPI_FILE)
	LTE_COUNTER_OBJECT = ParseCSV(LTE_COUNTER_FILE)
	#This gives a list containing float integers representing the time spend in GSM and WCDMA in format (GSM_TIME,WCDMA_TIME)
	Dict_of_time_in_technologies_L3Messages = Time_Calculation_GSM_WCDMA.Calculate_Time_Technologies_L3Messages(L3Messages_File)
	#Dict_of_time_in_technologies_L3Messages = Time_Calculation_GSM_WCDMA.Calculate_Time_Technology(GSM_WCDMA_COUNTER_OBJECT)
	Calculate_Time_RRC_State = Time_Calculation_GSM_WCDMA.Calculate_Time_RRC_State_Information(LTE_KPI_OBJECT)	#returns time in second
	Calculate_Time_RRC_State_From_WCDMA_KPI_FILE = Time_Calculation_GSM_WCDMA.Calculate_Time_RRC_State_Information_From_WCDMA_KPI_FILE(GSM_WCDMA_KPI_OBJECT)
	#Getting path of outputfile and then creating object and then writing to it
	outputfile = output_file_path(inputstring,testfileid)
	output_File = gzip.open(outputfile,"wb")
	writer = csv.writer(output_File, delimiter=',')
	#writing to the csv outputfile
#WCDMA_PS_Drop_Count  as this kpi is commented so i removed it from write row function.  //sk  update
	writer.writerow(['Time_Stamp']+['WCDMA_PS_Setup_success_rate_SingleRAB']+['WCDMA_PS_Setup_success_rate_MultiRAB']+['PS_After_ESR_MO_Accessibility_in_WCDMA']+['PS_After_ESR_MT_Accessibility_in_WCDMA']+['PS_With_CSFB_MO_Accessibility_in_WCDMA']+['PS_With_CSFB_MT_Accessibility_in_WCDMA']+['WCDMA_PS_Accessibility_Total']+['WCDMA_PS_Only_Retainability_MultiRAB']+['WCDMA_PS_Only_Retainability_SingleRAB']+['WCDMA_Only_PS_Retainability_Total']+['Total_WCDMA_PS_Attempts']+['Total_CSFB_PS_in_WCDMA_Attempt']+['Total_WCDMA_Only_PS_Attempt']+['Total_WCDMA_PS_Connection_Count']+['Total_PS_Drop_WCDMA_Only_Count']+['WCDMA_CS_MO_Single_RAB_Mean_Call_Connect_Time']+['WCDMA_CS_MO_Multi_RAB_Mean_Call_Connect_Time']+['WCDMA_CS_MT_Access_Mean_Call_Connect_Time']+['WCDMA_SoftHandover_Failures']+['WCDMA_Soft_Handover_success_rate']+['WCDMA_Inter_Frequency_Handover_Failures']+['WCDMA_Inter_Frequency_Handover_success_rate']+['WCDMA_Intra_Frequency_Handover_Failures']+['WCDMA_Intra_Frequency_Handover_success_rate']+['WCDMA_RACH_Failures']+['WCDMA_RACH_Failure_Rate']+['WCDMA_Time_Between_Soft_Handover_Second']+['WCDMA_Time_Between_Inter_Frequency_Handover_Second']+['WCDMA_Time_Between_Hard_Intra_Frequency_Handover_Second']+['WCDMA_CS_Accessibility_Single_RAB_MO']+['WCDMA_CS_Accessibility_Single_RAB_MT']+['WCDMA_CS_Accessibility_Multi_RAB_MO']+['WCDMA_CS_Accessibility_Multi_RAB_MT']+['WCDMA_CS_Accessibility_Total']+['WCDMA_LAU_Success_Rate']+['WCDMA_CS_Retainability_Single_RAB_MO']+['WCDMA_CS_Retainability_Multi_RAB_MO']+['WCDMA_CS_Retainability_Single_RAB_MT']+['WCDMA_CS_Retainability_Multi_RAB_MT']+['WCDMA_CS_Retainability_Total']+['WCDMA_Network_Attach_Success_Rate']+['UMTS_To_LTE_Redirection_Success_Rate']+['WCDMA_Time_Between_Hard_Intra_Frequency_HO']+['WCDMA_Time_Between_Hard_Inter_Frequency_HO']+['WCDMA_Time_Between_Soft_HO']+['WCDMA_Minutes_Per_RRC_Drop']+['WCDMA_Only_Minutes_Per_PS_Drop']+['WCDMA_CS_Transmit_Power_Count']+['WCDMA_CS_Transmit_Power_Average']+['WCDMA_PS_Transmit_Power_Count']+['WCDMA_PS_Transmit_Power_Average']+['WCDMA_CS_EcIo_Count']+['WCDMA_CS_EcIo_Average']+['WCDMA_PS_EcIo_Count']+['WCDMA_PS_EcIo_Average']+['WCDMA_Median_RRC_Setup_Time']+['Total_WCDMA_CS_Mean_Call_Connect_Time']+['Last_Preamble_Tx_Power_Avg']+['WCDMA_Adjusted_Closed_Loop_Power_Avg']+['Mean_CSFB_MO_MultiRAB_Call_Connect_Time']+['Mean_CSFB_MO_Call_Connect_Time_SingleRAB']+['Mean_CSFB_MT_Call_Connect_Time_MultiRAB']+['Mean_CSFB_MT_Call_Connect_Time_SingleRAB']+['LTE_Mean_Resource_Block_Allocation']+['LTE_Mean_Rank_Indicator']+['Median_CSFB_Redirect_Time_SingleRAB']+['Median_CSFB_Redirect_Time_MultiRAB']+['LTE_Median_Data_Interrupt_Time_PS_Only_SingleRAB']+['LTE_Median_Data_Interrupt_Time_PS_Only_MultiRAB']+['LTE_Median_Data_Interrupt_Time_CSFB_MO']+['LTE_Median_Data_Interrupt_Time_CSFB_MT']+['LTE_Mean_RB_Count']+['Mean_CSFB_UMTS_To_LTE_Redirection_Time_SingleRAB']+['Mean_CSFB_UMTS_To_LTE_Redirection_Time_MultiRAB']+['LTE_DL_PDSCH_ThroughputCount']+['LTE_DL_PDSCH_ThroughputAverage']+['LTE_UL_PUSCH_ThroughputCount']+['LTE_UL_PUSCH_ThroughputAverage']+['LTE_PDSCH_Mean_Frame_Usage']+['LTE_RRC_connected_time']+['Overall_Median_CSFB_Interruption_Time']+['LTE_Spectral_Efficiency_DL']+['LTE_Median_RRC_Setup_Time']+['LTE_Mean_CQI']+['LTE_Minutes_Per_Drop']+['CSFB_LTE_To_UMTS_Redirection_Success_Rate_SingleRAB']+['CSFB_LTE_To_UMTS_Redirection_Success_Rate_MultiRAB']+['CSFB_MO_SingleRAB_Setup_Success_Rate']+['CSFB_MT_Setup_Success_Rate_SingleRAB']+['LTE_To_UMTS_HO_Success_Rate_PS_Only_Single_RAB']+['LTE_To_UMTS_HO_Success_Rate_PS_Only_Multi_RAB']+['LTE_QAM_USAGE']+['CSFB_MO_PS_Setup_Success_Rate']+['CSFB_MT_PS_Setup_Success_Rate']+['LTE_RRC_Detach_Drops']+['LTE_RRC_Attach_Drops']+['LTE_RRC_Retainability_Rate']+['LTE_RRC_Reestablishment_Success_Rate']+['CSFB_MO_Single_RAB_Drop_Count']+['CSFB_MO_Multi_RAB_Drop_Count']+['CSFB_MT_Single_RAB_Drop_Count']+['CSFB_MT_Multi_RAB_Drop_Count']+['CSFB_Retainability_Rate_SingleRAB']+['CSFB_Retainability_Rate_MultiRAB']+['CSFB_Drop_Count_SingleRAB']+['CSFB_Drop_Count_MultiRAB']+['CSFB_UMTS_To_LTE_Redirection_Success_Rate_SingleRAB']+['CSFB_UMTS_To_LTE_Redirection_Success_Rate_MultiRAB']+['LTE_To_UMTS_Redirection_Failures']+['LTE_IRAT_Success_Rate']+['LTE_Network_Attach_Success_Rate']+['LTE_RACH_Failure_Rate']+['LTE_PS_Accessibility_Single_RAB']+['LTE_PS_Accessibility_Multi_RAB']+['LTE_PS_Accessibility_Total']+['LTE_CSFB_Accessibility_Single_RAB_MO']+['LTE_CSFB_Accessibility_Single_RAB_MT']+['LTE_CSFB_Accessibility_Multi_RAB_MO']+['LTE_CSFB_Accessibility_Multi_RAB_MT']+['LTE_CSFB_Accessibility_Total']+['LTE_CSFB_Retainability_Single_RAB_MO']+['LTE_CSFB_Retainability_Single_RAB_MT']+['LTE_CSFB_Retainability_Multi_RAB_MO']+['LTE_CSFB_Retainability_Multi_RAB_MT']+['LTE_CSFB_Retainability_Total']+['LTE_Intra_Frequency_HO_Success_Rate']+['LTE_Inter_Frequency_HO_Success_Rate']+['LTE_Network_Attach_Success_Rate']+['LTE_TAU_Success_Rate']+['LTE_RRC_Connection_Success_Rate']+['LTE_Time_Between_Inter_Frequency_HO']+['LTE_Time_Between_Intra_Frequency_HO']+['Technology_split_GSM']+['Technology_split_WCDMA']+['Technology_split_LTE']+['Median_LTE_Time_To_First_Byte']+['Median_WCDMA_Time_To_First_Byte']+['LTE_IRAT_Success_Rate_Redirection_PS_Only_Single_RAB']+['LTE_IRAT_Success_Rate_Redirection_PS_Only_Multi_RAB']+['CSFB_UMTS_To_LTE_Reselection_Failure_Single_RAB']+['CSFB_UMTS_To_LTE_Reselection_Failure_Multi_RAB']+['Overall_Mean_CSFB_UMTS_To_LTE_Redirection_Time']+['LTE_Overall_Median_Data_Interrupt_Time']+['LTE_Median_Data_Interrupt_Time_PS_After_ESR_MO']+['LTE_Median_Data_Interrupt_Time_PS_After_ESR_MT']+['Overall_CSFB_LTE_To_UMTS_Redirection_Success_Rate']+['Overall_CSFB_UMTS_To_LTE_Reselection_Success_Rate']+['Overall_CS_Setup_Success_Rate']+['Overall_LTE_To_UMTS_HO_Success_Rate']+['Overall_Median_UMTS_To_LTE_Redirect_Time']+['Overall_CSFB_PS_Setup_Success_Rate']+['LTE_PS_After_ESR_MO_Setup_Success_Rate']+['LTE_PS_After_ESR_MT_Setup_Success_Rate']+['Overall_LTE_Mean_Incremental_CS_Call_Connect_Time']+['LTE_Mean_Incremental_CS_MO_Single_RAB_Call_Connect_Time']+['LTE_Mean_Incremental_CS_MO_Multi_RAB_Call_Connect_Time']+['LTE_Mean_Incremental_CS_MT_Single_RAB_Call_Connect_Time']+['LTE_Mean_Incremental_CS_MT_Multi_RAB_Call_Connect_Time']+['Total_LTE_CSFB_Call_Connect_Time']+['LTE_Mean_CSFB_MO_Multi_RAB_Call_Connect_Time']+['LTE_Mean_CSFB_MO_Single_RAB_Call_Connect_Time']+['Overall_CSFB_Attempt_Count']+['Overall_CSFB_Success_Count']+['Overall_CSFB_SuccessfulRelease_Count']+['Overall_CSFB_Drop_Count']+['Overall_CSFB_UMTS_To_LTE_Redirection_Attempt']+['Overall_CSFB_UMTS_To_LTE_Redirection_Faiure']+['Median_CSFB_MO_Interruption_Time']+['Median_CSFB_MT_Interruption_Time']+['LTE_PRACH_Tx_Power_Sample_Count']+['LTE_PS_Retainability_Single_RAB']+['LTE_PS_Retainability_Multi_RAB_During_CSFB']+['LTE_PS_Retainability_PS_Only_Multi_RAB']+['LTE_PS_Overall_Retainability']+['Overall_PS_Attempts']+['Overall_PS_Setup_Success_Rate']+['Overall_PS_Accessibility']+['Overall_CS_Accessibility']+['Overall_CS_Retainability']+['LTE_PS_Accessibility_Total']+['LTE_PS_Accessibility_PS_Only_Multi_RAB']+['Overall_CS_Mean_Call_Connect_Time']+['Total_LTE_PS_Attempt']+['Total_CSFB_PS_in_WCDMA_Connection_Count']+['Total_PS_WCDMA_Only_Count']+['Total_LTE_PS_Connection_Count']+['Overall_PS_Connection_Count']+['Total_CSFB_PS_Drop_in_WCDMA_Count']+['Total_PS_Drop_LTE_Count']+['LTE_RRC_Drop_Count']+['Total_PS_Drop_WCDMA_Count']+['Overall_PS_Drop_Count']+['PS_With_CSFB_MO_Retainability_Rate']+['PS_With_CSFB_MT_Retainability_Rate']+['LTE_PS_After_ESR_MO_Retainability_Rate_in_WCDMA']+['LTE_PS_After_ESR_MT_Retainability_Rate_in_WCDMA']+['Total_CSFB_PS_Retainability_in_WCDMA']+['Total_WCDMA_PS_Retainability_Rate']+['Overall_PS_Retainability']+['Overall_CS_Single_RAB_Access_Time']+['Overall_CS_MO_Single_RAB_Mean_Call_Connect_Time']+['Overall_CS_MO_Multi_RAB_Mean_Call_Connect_Time']+['Overall_CS_MT_Access_Mean_Call_Connect_Time']+['Total_PS_Connected_Time_in_LTE']+['Overall_PS_Connected_Time']+['PS_Retainability_LTE_to_UMTS_Redirection_CSFB']+['Total_CS_MO_Single_RAB_Retainability']+['Total_CS_MO_Single_RAB_Setup_Success_Rate']+['Total_CS_MO_Multi_RAB_Setup_Success_Rate']+['Total_CS_MO_Single_RAB_Attempts']+['Total_CS_MO_Multi_RAB_Attempts']+['Overall_CS_MT_Access_Attempts']+['Total_CS_MT_Access_Setup_Success_Rate']+['PS_Retainability_with_CSFB_MO_in_WCDMA']+['PS_Retainability_with_CSFB_MT_in_WCDMA']+['PS_Retainability_After_ESR_MO_in_WCDMA']+['PS_Retainability_After_ESR_MT_in_WCDMA']+['Total_PS_Retainability_CSFB_in_WCDMA']+['Total_CS_MO_Multi_RAB_Retainability']+['Total_PS_Accessibility_WCDMA_Only']+['Total_CS_MT_Retainability']+['Total_WCDMA_Minutes_Per_Drop']+['Overall_Minutes_Per_Drop']+['Total_CS_MO_Single_RAB_Success_Count']+['Total_CS_MO_Single_RAB_Drop_Count']+['Total_CS_MO_Multi_RAB_Success_Count']+['Total_CS_MO_Multi_RAB_Drop_Count']+['Overall_CS_MT_Success']+['Normalized_PS_Retainability_Rate']+['Overall_CS_MT_DropCount']+['Overall_CSFB_MT_Success']+['Overall_CSFB_MT_DropCount']+['Intra_LTE_HO_Attempt']+['Inter_LTE_HO_Attempt']+['Mean_CSFB_MO_SingleRAB_IncrementSetupTime']+['Mean_CSFB_MT_IncrementalSetupTime']+['Mean_UMTS_LTE_CSFB_Reselect_Duration']+['Median_UMTS_LTE_CSFB_Reselect_Duration']+['UMTS_LTE_CSFB_Reselect_Success_Rate']+['UMTS_LTE_CSFB_Reselect_Failure_Rate']+['PS_Accessibility_LTE_to_UMTS_Redirection_CSFB']+['LTE_MIMO_USAGE']+['LAST'])
	
#WCDMA_PS_Drop_Count    //SZ updated
	writer.writerow([Local_time()]+[WCDMA_PS_Setup_success_rate_SingleRAB(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_PS_Setup_success_rate_MultiRAB(GSM_WCDMA_COUNTER_OBJECT)]+[PS_After_ESR_MO_Accessibility_in_WCDMA(LTE_COUNTER_OBJECT)]+[PS_After_ESR_MT_Accessibility_in_WCDMA(LTE_COUNTER_OBJECT)]+[PS_With_CSFB_MO_Accessibility_in_WCDMA(LTE_COUNTER_OBJECT)]+[PS_With_CSFB_MT_Accessibility_in_WCDMA(LTE_COUNTER_OBJECT)]+[WCDMA_PS_Accessibility_Total(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[WCDMA_PS_Only_Retainability_MultiRAB(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_PS_Only_Retainability_SingleRAB(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_Only_PS_Retainability_Total(GSM_WCDMA_COUNTER_OBJECT)]+[Total_WCDMA_PS_Attempts(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[Total_CSFB_PS_in_WCDMA_Attempt(LTE_COUNTER_OBJECT)]+[Total_WCDMA_Only_PS_Attempt(GSM_WCDMA_COUNTER_OBJECT)]+[Total_WCDMA_PS_Connection_Count(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[Total_PS_Drop_WCDMA_Only_Count(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_CS_MO_Single_RAB_Mean_Call_Connect_Time(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_CS_MO_Multi_RAB_Mean_Call_Connect_Time(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_CS_MT_Access_Mean_Call_Connect_Time(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_SoftHandover_Failures(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_Soft_Handover_success_rate(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_Inter_Frequency_Handover_Failures(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_Inter_Frequency_Handover_success_rate(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_Intra_Frequency_Handover_Failures(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_Intra_Frequency_Handover_success_rate(GSM_WCDMA_COUNTER_OBJECT)]+[RACH_FAILURE_WCDMA(GSM_WCDMA_COUNTER_OBJECT)]+[RACH_Failure_Rate_WCDMA(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_Time_Between_Soft_Handover_Second(GSM_WCDMA_COUNTER_OBJECT,Calculate_Time_RRC_State_From_WCDMA_KPI_FILE)]+[WCDMA_Time_Between_Inter_Frequency_Handover_Second(GSM_WCDMA_COUNTER_OBJECT,Calculate_Time_RRC_State_From_WCDMA_KPI_FILE)]+[WCDMA_Time_Between_Hard_Intra_Frequency_Handover_Second(GSM_WCDMA_COUNTER_OBJECT,Calculate_Time_RRC_State_From_WCDMA_KPI_FILE)]+[WCDMA_CS_Accessibility_Single_RAB_MO(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_CS_Accessibility_Single_RAB_MT(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_CS_Accessibility_Multi_RAB_MO(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_CS_Accessibility_Multi_RAB_MT(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_CS_Accessibility_Total(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_LAU_Success_Rate(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_CS_Retainability_Single_RAB_MO(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_CS_Retainability_Multi_RAB_MO(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_CS_Retainability_Single_RAB_MT(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_CS_Retainability_Multi_RAB_MT(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_CS_Retainability_Total(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_Network_Attach_Success_Rate(GSM_WCDMA_COUNTER_OBJECT)]+[UMTS_To_LTE_Redirection_Success_Rate(GSM_WCDMA_COUNTER_OBJECT)]+[WCDMA_Time_Between_Hard_Intra_Frequency_HO(GSM_WCDMA_COUNTER_OBJECT,Calculate_Time_RRC_State_From_WCDMA_KPI_FILE)]+[WCDMA_Time_Between_Hard_Inter_Frequency_HO(GSM_WCDMA_COUNTER_OBJECT,Calculate_Time_RRC_State_From_WCDMA_KPI_FILE)]+[WCDMA_Time_Between_Soft_HO(GSM_WCDMA_COUNTER_OBJECT,Calculate_Time_RRC_State_From_WCDMA_KPI_FILE)]+[WCDMA_Minutes_Per_RRC_Drop(GSM_WCDMA_COUNTER_OBJECT,Dict_of_time_in_technologies_L3Messages)]+[WCDMA_Only_Minutes_Per_PS_Drop(GSM_WCDMA_COUNTER_OBJECT,Dict_of_time_in_technologies_L3Messages)]+[WCDMA_CS_Transmit_Power_Count(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_CS_Transmit_Power_Average(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_PS_Transmit_Power_Count(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_PS_Transmit_Power_Average(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_CS_EcIo_Count(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_CS_EcIo_Average(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_PS_EcIo_Count(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_PS_EcIo_Average(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_Median_RRC_Setup_Time(GSM_WCDMA_KPI_OBJECT)]+[Total_WCDMA_CS_Mean_Call_Connect_Time(GSM_WCDMA_KPI_OBJECT)]+[Last_Preamble_Tx_Power_Avg(GSM_WCDMA_KPI_OBJECT)]+[WCDMA_Adjusted_Closed_Loop_Power_Avg(GSM_WCDMA_KPI_OBJECT)]+[Mean_CSFB_MO_MultiRAB_Call_Connect_Time(LTE_KPI_OBJECT)]+[Mean_CSFB_MO_Call_Connect_Time_SingleRAB(LTE_KPI_OBJECT)]+[Mean_CSFB_MT_Call_Connect_Time_MultiRAB(LTE_KPI_OBJECT)]+[Mean_CSFB_MT_Call_Connect_Time_SingleRAB(LTE_KPI_OBJECT)]+[LTE_Mean_Resource_Block_Allocation(LTE_KPI_OBJECT)]+[LTE_Mean_Rank_Indicator(LTE_KPI_OBJECT)]+[Median_CSFB_Redirect_Time_SingleRAB(LTE_KPI_OBJECT)]+[Median_CSFB_Redirect_Time_MultiRAB(LTE_KPI_OBJECT)]+[LTE_Median_Data_Interrupt_Time_PS_Only_SingleRAB(LTE_KPI_OBJECT)]+[LTE_Median_Data_Interrupt_Time_PS_Only_MultiRAB(LTE_KPI_OBJECT)]+[LTE_Median_Data_Interrupt_Time_CSFB_MO(LTE_KPI_OBJECT)]+[LTE_Median_Data_Interrupt_Time_CSFB_MT(LTE_KPI_OBJECT)]+[LTE_Mean_RB_Count(LTE_KPI_OBJECT)]+[Mean_CSFB_UMTS_To_LTE_Redirection_Time_SingleRAB(LTE_KPI_OBJECT)]+[Mean_CSFB_UMTS_To_LTE_Redirection_Time_MultiRAB(LTE_KPI_OBJECT)]+[LTE_DL_PDSCH_ThroughputCount(LTE_KPI_OBJECT)]+[LTE_DL_PDSCH_ThroughputAverage(LTE_KPI_OBJECT)]+[LTE_UL_PUSCH_ThroughputCount(LTE_KPI_OBJECT)]+[LTE_UL_PUSCH_ThroughputAverage(LTE_KPI_OBJECT)]+[LTE_PDSCH_Mean_Frame_Usage(LTE_KPI_OBJECT)]+[Calculate_Time_RRC_State]+[Overall_Median_CSFB_Interruption_Time(LTE_KPI_OBJECT)]+[LTE_Spectral_Efficiency_DL(LTE_KPI_OBJECT)]+[LTE_Median_RRC_Setup_Time(LTE_KPI_OBJECT)]+[LTE_Mean_CQI(LTE_KPI_OBJECT)]+[LTE_Minutes_Per_Drop(LTE_COUNTER_OBJECT,Calculate_Time_RRC_State)]+[CSFB_LTE_To_UMTS_Redirection_Success_Rate_SingleRAB(LTE_COUNTER_OBJECT)]+[CSFB_LTE_To_UMTS_Redirection_Success_Rate_MultiRAB(LTE_COUNTER_OBJECT)]+[CSFB_MO_SingleRAB_Setup_Success_Rate(LTE_COUNTER_OBJECT)]+[CSFB_MT_Setup_Success_Rate_SingleRAB(LTE_COUNTER_OBJECT)]+[LTE_To_UMTS_HO_Success_Rate_PS_Only_Single_RAB(LTE_COUNTER_OBJECT)]+[LTE_To_UMTS_HO_Success_Rate_PS_Only_Multi_RAB(LTE_COUNTER_OBJECT)]+[LTE_QAM_USAGE(LTE_KPI_OBJECT)]+[CSFB_MO_PS_Setup_Success_Rate(LTE_COUNTER_OBJECT)]+[CSFB_MT_PS_Setup_Success_Rate(LTE_COUNTER_OBJECT)]+[LTE_RRC_Detach_Drops(LTE_COUNTER_OBJECT)]+[LTE_RRC_Attach_Drops(LTE_COUNTER_OBJECT)]+[LTE_RRC_Retainability_Rate(LTE_COUNTER_OBJECT)]+[LTE_RRC_Reestablishment_Success_Rate(LTE_COUNTER_OBJECT)]+[CSFB_MO_Single_RAB_Drop_Count(LTE_COUNTER_OBJECT)]+[CSFB_MO_Multi_RAB_Drop_Count(LTE_COUNTER_OBJECT)]+[CSFB_MT_Single_RAB_Drop_Count(LTE_COUNTER_OBJECT)]+[CSFB_MT_Multi_RAB_Drop_Count(LTE_COUNTER_OBJECT)]+[CSFB_Retainability_Rate_SingleRAB(LTE_COUNTER_OBJECT)]+[CSFB_Retainability_Rate_MultiRAB(LTE_COUNTER_OBJECT)]+[CSFB_Drop_Count_SingleRAB(LTE_COUNTER_OBJECT)]+[CSFB_Drop_Count_MultiRAB(LTE_COUNTER_OBJECT)]+[CSFB_UMTS_To_LTE_Redirection_Success_Rate_SingleRAB(LTE_COUNTER_OBJECT)]+[CSFB_UMTS_To_LTE_Redirection_Success_Rate_MultiRAB(LTE_COUNTER_OBJECT)]+[LTE_To_UMTS_Redirection_Failures(LTE_COUNTER_OBJECT)]+[LTE_IRAT_Success_Rate(LTE_COUNTER_OBJECT)]+[LTE_Network_Attach_Success_Rate(LTE_COUNTER_OBJECT)]+[LTE_RACH_Failure_Rate(LTE_COUNTER_OBJECT)]+[LTE_PS_Accessibility_Single_RAB(LTE_COUNTER_OBJECT)]+[LTE_PS_Accessibility_Multi_RAB(LTE_COUNTER_OBJECT)]+[LTE_PS_Accessibility_Total(LTE_COUNTER_OBJECT)]+[LTE_CSFB_Accessibility_Single_RAB_MO(LTE_COUNTER_OBJECT)]+[LTE_CSFB_Accessibility_Single_RAB_MT(LTE_COUNTER_OBJECT)]+[LTE_CSFB_Accessibility_Multi_RAB_MO(LTE_COUNTER_OBJECT)]+[LTE_CSFB_Accessibility_Multi_RAB_MT(LTE_COUNTER_OBJECT)]+[LTE_CSFB_Accessibility_Total(LTE_COUNTER_OBJECT)]+[LTE_CSFB_Retainability_Single_RAB_MO(LTE_COUNTER_OBJECT)]+[LTE_CSFB_Retainability_Single_RAB_MT(LTE_COUNTER_OBJECT)]+[LTE_CSFB_Retainability_Multi_RAB_MO(LTE_COUNTER_OBJECT)]+[LTE_CSFB_Retainability_Multi_RAB_MT(LTE_COUNTER_OBJECT)]+[LTE_CSFB_Retainability_Total(LTE_COUNTER_OBJECT)]+[LTE_Intra_Frequency_HO_Success_Rate(LTE_COUNTER_OBJECT)]+[LTE_Inter_Frequency_HO_Success_Rate(LTE_COUNTER_OBJECT)]+[LTE_Network_Attach_Success_Rate(LTE_COUNTER_OBJECT)]+[LTE_TAU_Success_Rate(LTE_COUNTER_OBJECT)]+[LTE_RRC_Connection_Success_Rate(LTE_COUNTER_OBJECT)]+[LTE_Time_Between_Inter_Frequency_HO(LTE_COUNTER_OBJECT,Calculate_Time_RRC_State)]+[LTE_Time_Between_Intra_Frequency_HO(LTE_COUNTER_OBJECT,Calculate_Time_RRC_State)]+[Technology_split_GSM(Dict_of_time_in_technologies_L3Messages)]+[Technology_split_WCDMA(Dict_of_time_in_technologies_L3Messages)]+[Technology_split_LTE(Dict_of_time_in_technologies_L3Messages)]+[Median_LTE_Time_To_First_Byte(GSM_WCDMA_KPI_OBJECT)]+[Median_WCDMA_Time_To_First_Byte(LTE_KPI_OBJECT)]+[LTE_IRAT_Success_Rate_Redirection_PS_Only_Single_RAB(LTE_COUNTER_OBJECT)]+[LTE_IRAT_Success_Rate_Redirection_PS_Only_Multi_RAB(LTE_COUNTER_OBJECT)]+[CSFB_UMTS_To_LTE_Reselection_Failure_Single_RAB(LTE_COUNTER_OBJECT)]+[CSFB_UMTS_To_LTE_Reselection_Failure_Multi_RAB(LTE_COUNTER_OBJECT)]+[Overall_Mean_CSFB_UMTS_To_LTE_Redirection_Time(LTE_KPI_OBJECT)]+[LTE_Overall_Median_Data_Interrupt_Time(LTE_KPI_OBJECT)]+[LTE_Median_Data_Interrupt_Time_PS_After_ESR_MO(LTE_KPI_OBJECT)]+[LTE_Median_Data_Interrupt_Time_PS_After_ESR_MT(LTE_KPI_OBJECT)]+[Overall_CSFB_LTE_To_UMTS_Redirection_Success_Rate(LTE_COUNTER_OBJECT)]+[Overall_CSFB_UMTS_To_LTE_Reselection_Success_Rate(LTE_COUNTER_OBJECT)]+[Overall_CS_Setup_Success_Rate(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[Overall_LTE_To_UMTS_HO_Success_Rate(LTE_COUNTER_OBJECT)]+[Overall_Median_UMTS_To_LTE_Redirect_Time(LTE_KPI_OBJECT)]+[Overall_CSFB_PS_Setup_Success_Rate(LTE_COUNTER_OBJECT)]+[LTE_PS_After_ESR_MO_Setup_Success_Rate(LTE_COUNTER_OBJECT)]+[LTE_PS_After_ESR_MT_Setup_Success_Rate(LTE_COUNTER_OBJECT)]+[Overall_LTE_Mean_Incremental_CS_Call_Connect_Time(LTE_KPI_OBJECT)]+[LTE_Mean_Incremental_CS_MO_Single_RAB_Call_Connect_Time(LTE_KPI_OBJECT)]+[LTE_Mean_Incremental_CS_MO_Multi_RAB_Call_Connect_Time(LTE_KPI_OBJECT)]+[LTE_Mean_Incremental_CS_MT_Single_RAB_Call_Connect_Time(LTE_KPI_OBJECT)]+[LTE_Mean_Incremental_CS_MT_Multi_RAB_Call_Connect_Time(LTE_KPI_OBJECT)]+[Total_LTE_CSFB_Call_Connect_Time(LTE_KPI_OBJECT)]+[LTE_Mean_CSFB_MO_Multi_RAB_Call_Connect_Time(LTE_KPI_OBJECT)]+[LTE_Mean_CSFB_MO_Single_RAB_Call_Connect_Time(LTE_KPI_OBJECT)]+[Overall_CSFB_Attempt_Count(LTE_COUNTER_OBJECT)]+[Overall_CSFB_Success_Count(LTE_COUNTER_OBJECT)]+[Overall_CSFB_SuccessfulRelease_Count(LTE_COUNTER_OBJECT)]+[Overall_CSFB_Drop_Count(LTE_COUNTER_OBJECT)]+[Overall_CSFB_UMTS_To_LTE_Redirection_Attempt(LTE_COUNTER_OBJECT)]+[Overall_CSFB_UMTS_To_LTE_Redirection_Faiure(LTE_COUNTER_OBJECT)]+[Median_CSFB_MO_Interruption_Time(LTE_KPI_OBJECT)]+[Median_CSFB_MT_Interruption_Time(LTE_KPI_OBJECT)]+[LTE_PRACH_Tx_Power_Sample_Count(LTE_KPI_OBJECT)]+[LTE_PS_Retainability_Single_RAB(LTE_COUNTER_OBJECT)] +[LTE_PS_Retainability_Multi_RAB_During_CSFB(LTE_COUNTER_OBJECT)]+[LTE_PS_Retainability_PS_Only_Multi_RAB(LTE_COUNTER_OBJECT)]+[LTE_PS_Overall_Retainability(LTE_COUNTER_OBJECT)]+[Overall_PS_Attempts(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[Overall_PS_Setup_Success_Rate(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[Overall_PS_Accessibility(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[Overall_CS_Accessibility(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[Overall_CS_Retainability(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[LTE_PS_Accessibility_Total(LTE_COUNTER_OBJECT)]+[LTE_PS_Accessibility_PS_Only_Multi_RAB(LTE_COUNTER_OBJECT)]+[Overall_CS_Mean_Call_Connect_Time(GSM_WCDMA_KPI_OBJECT,LTE_KPI_OBJECT)]+[Total_LTE_PS_Attempt(LTE_COUNTER_OBJECT)]+[Total_CSFB_PS_in_WCDMA_Connection_Count(LTE_COUNTER_OBJECT)]+[Total_PS_WCDMA_Only_Count(GSM_WCDMA_COUNTER_OBJECT)]+[Total_LTE_PS_Connection_Count(LTE_COUNTER_OBJECT)]+[Overall_PS_Connection_Count(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT)]+[Total_CSFB_PS_Drop_in_WCDMA_Count(LTE_COUNTER_OBJECT)]+[Total_PS_Drop_LTE_Count(LTE_COUNTER_OBJECT)]+[LTE_RRC_Drop_Count(LTE_COUNTER_OBJECT)]+[Total_PS_Drop_WCDMA_Count(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[Overall_PS_Drop_Count(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[PS_With_CSFB_MO_Retainability_Rate(LTE_COUNTER_OBJECT)]+[PS_With_CSFB_MT_Retainability_Rate(LTE_COUNTER_OBJECT)]+[LTE_PS_After_ESR_MO_Retainability_Rate_in_WCDMA(LTE_COUNTER_OBJECT)]+[LTE_PS_After_ESR_MT_Retainability_Rate_in_WCDMA(LTE_COUNTER_OBJECT)]+[Total_CSFB_PS_Retainability_in_WCDMA(LTE_COUNTER_OBJECT)]+[Total_WCDMA_PS_Retainability_Rate(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT)]+[Overall_PS_Retainability(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[Overall_CS_Single_RAB_Access_Time(GSM_WCDMA_COUNTER_OBJECT,GSM_WCDMA_KPI_OBJECT,LTE_COUNTER_OBJECT,LTE_KPI_OBJECT)]+[Overall_CS_MO_Single_RAB_Mean_Call_Connect_Time(GSM_WCDMA_KPI_OBJECT, LTE_KPI_OBJECT)]+[Overall_CS_MO_Multi_RAB_Mean_Call_Connect_Time(GSM_WCDMA_KPI_OBJECT, LTE_KPI_OBJECT)]+[Overall_CS_MT_Access_Mean_Call_Connect_Time(GSM_WCDMA_KPI_OBJECT, LTE_KPI_OBJECT)]+[Total_PS_Connected_Time_in_LTE(LTE_KPI_OBJECT)]+[Overall_PS_Connected_Time(GSM_WCDMA_KPI_OBJECT, LTE_KPI_OBJECT)]+[PS_Retainability_LTE_to_UMTS_Redirection_CSFB(LTE_COUNTER_OBJECT)]+[Total_CS_MO_Single_RAB_Retainability(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT)]+[Total_CS_MO_Single_RAB_Setup_Success_Rate(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT)]+[Total_CS_MO_Multi_RAB_Setup_Success_Rate(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT)]+[Total_CS_MO_Single_RAB_Attempts(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT)]+[Total_CS_MO_Multi_RAB_Attempts(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT)]+[Overall_CS_MT_Access_Attempts(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[Total_CS_MT_Access_Setup_Success_Rate(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[PS_Retainability_with_CSFB_MO_in_WCDMA(LTE_COUNTER_OBJECT)]+[PS_Retainability_with_CSFB_MT_in_WCDMA(LTE_COUNTER_OBJECT)]+[PS_Retainability_After_ESR_MO_in_WCDMA(LTE_COUNTER_OBJECT)]+[PS_Retainability_After_ESR_MT_in_WCDMA(LTE_COUNTER_OBJECT)]+[Total_PS_Retainability_CSFB_in_WCDMA(LTE_COUNTER_OBJECT)]+[Total_CS_MO_Multi_RAB_Retainability(GSM_WCDMA_COUNTER_OBJECT,LTE_COUNTER_OBJECT)]+[Total_PS_Accessibility_WCDMA_Only(GSM_WCDMA_COUNTER_OBJECT)]+[Total_CS_MT_Retainability(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT)]+[Total_WCDMA_Minutes_Per_Drop(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT, Calculate_Time_RRC_State_From_WCDMA_KPI_FILE)]+[Overall_Minutes_Per_Drop(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT, Calculate_Time_RRC_State_From_WCDMA_KPI_FILE, Calculate_Time_RRC_State)]+[Total_CS_MO_Single_RAB_Success_Count(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT)]+[Total_CS_MO_Single_RAB_Drop_Count(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT)]+[Total_CS_MO_Multi_RAB_Success_Count(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT)]+[Total_CS_MO_Multi_RAB_Drop_Count(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT)]+[Overall_CS_MT_Success(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT)]+[Normalized_PS_Retainability_Rate(GSM_WCDMA_COUNTER_OBJECT,GSM_WCDMA_KPI_OBJECT,LTE_COUNTER_OBJECT,LTE_KPI_OBJECT,Calculate_Time_RRC_State)]+[Overall_CS_MT_DropCount(GSM_WCDMA_COUNTER_OBJECT, LTE_COUNTER_OBJECT)]+[Overall_CSFB_MT_Success(LTE_COUNTER_OBJECT)]+[Overall_CSFB_MT_DropCount(LTE_COUNTER_OBJECT)]+[Intra_LTE_HO_Attempt(LTE_COUNTER_OBJECT)]+[Inter_LTE_HO_Attempt(LTE_COUNTER_OBJECT)]+[Mean_CSFB_MO_SingleRAB_IncrementSetupTime(LTE_KPI_OBJECT)]+[Mean_CSFB_MT_IncrementalSetupTime(LTE_KPI_OBJECT)]+[Mean_UMTS_LTE_CSFB_Reselect_Duration(LTE_KPI_OBJECT)]+[Median_UMTS_LTE_CSFB_Reselect_Duration(LTE_KPI_OBJECT)]+[UMTS_LTE_CSFB_Reselect_Success_Rate(LTE_COUNTER_OBJECT)]+[UMTS_LTE_CSFB_Reselect_Failure_Rate(LTE_COUNTER_OBJECT)]+[PS_Accessibility_LTE_to_UMTS_Redirection_CSFB(LTE_COUNTER_OBJECT)]+[LTE_MIMO_USAGE(LTE_KPI_OBJECT)]+['last'])
	output_File.close()
	tempfilename = inputstring + 'temp.csv.gz'
	os.remove(tempfilename)
	tempfilename = inputstring + 'temp2.csv.gz'
	os.remove(tempfilename)

main(sys.argv[1:])
