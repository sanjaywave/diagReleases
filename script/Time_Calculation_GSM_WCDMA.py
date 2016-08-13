from csv_processor import ParseCSV
import datetime
import time
import csv

def parseDateTimeFromString(datetimeStr):
    """
    Parses a date time stamp in format "Tue Jun 10 15:33:51.231 2014" to python timestamp timetuple
    """
    x= datetimeStr.split(" ")
    i = len(x) - 1
    while i >= 0:
        if ( x[i] == ''):
            del x[i]
        i = i - 1

        

    newdate='{0} {1} {2} {3} {4}'.format(x[0],x[1],x[2],x[3],x[4])

    nofrag_dt = datetime.datetime.strptime(newdate, "%a %b %d %H:%M:%S.%f %Y")
    return nofrag_dt

def Get_Epoc_time_in_millisec(pased_time_string):
	"""
	Convert the time tuple into the epoc time in seconds
	"""
	parsed_time_tuple = parseDateTimeFromString(pased_time_string)
	sec_since_epoch = time.mktime(parsed_time_tuple.timetuple()) + parsed_time_tuple.microsecond/1000000.0
	return sec_since_epoch
#No longer required due to all time based calculation shifted to the L3Messages file calculation
"""
def Calculate_Time_Technology(Object):
	try:
		List_Of_Technology = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('Technology'))
		List_Of_Time = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('Date'))
		Current_Technology = List_Of_Technology[0].strip(' ')
		dict = {'WCDMA':0,'GSM':0,'LTE':0,'0':0}
		i = 0
		j = 0
		for elements in List_Of_Technology:
			elements = elements.strip(' ')
			if(Current_Technology.find(elements)==-1):
				previous_elements = List_Of_Technology[j-1].strip(' ')
				dict[previous_elements] = float(dict[previous_elements]) + Time_difference(List_Of_Time[j-1],List_Of_Time[i])
				i = j
				Current_Technology = List_Of_Technology[j].strip(' ')
			j = j + 1
		dict[Current_Technology] = float(dict[Current_Technology]) + Time_difference(List_Of_Time[j-1],List_Of_Time[i])
		return dict
	except Exception:
		print 'Error:Error returned by the Calculate_Time_Technologies'
		return {'WCDMA':0,'GSM':0,'LTE':0,'0':0,'Total':0}
"""

def Calculate_Time_RRC_State_Information(Object):
	try:
		List_Of_State = Object.getAllColumnValuesByIndexWithSpaces(Object.getColumnIndexByName('RRC State Information'))
		List_Of_Time = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('Date'))
		Current_State = List_Of_State[0]
		i = 0
		j = 0
		time = 0.000
		while(i<=len(List_Of_State)):
			if(('4' in Current_State)&(i<=(len(List_Of_State)-2))):
				initaitedTime = List_Of_Time[i]
				while(('4' in Current_State) and (i<=(len(List_Of_State)-2))):
					i = i + 1
					List_Of_State[i] = List_Of_State[i].strip(' ')
					if(List_Of_State[i]!=''):
						Current_State = List_Of_State[i]
				terminatedTime = List_Of_Time[i]
				time = time + Time_difference(terminatedTime,initaitedTime)
#				print"time :->", Time_difference(terminatedTime,initaitedTime)
			i = i + 1
			if(i<len(List_Of_State)):
				List_Of_State[i] = List_Of_State[i].strip(' ')
				if(List_Of_State[i]!=' '):
					Current_State = List_Of_State[i]
#		print"RRC_State time -------------------bfor if ", time
#		if('4' in Current_State):   			#commented bcoz bug found due to this zahid
#			time = time + Time_difference(terminatedTime,initaitedTime)
#			print"Time :->", Time_difference(terminatedTime,initaitedTime)
#		print"RRC_State time -------------------after if", time
		return time
	except Exception:
		print 'Error:Error while calculating time RRC state information'
		return 0.000


def Calculate_Time_RRC_State_Information_From_WCDMA_KPI_FILE(Object):
	try:
		List_Of_State = Object.getAllColumnValuesByIndexWithSpaces(Object.getColumnIndexByName('WCDMA_RRC_STATE '))
		List_Of_Time = Object.getAllColumnValuesByIndex(Object.getColumnIndexByName('Date'))
		Current_State = '0'
		i = 0
		while(i<len(List_Of_State)):
			if(List_Of_State[i]!=''):
				Current_State = List_Of_State[i]
			List_Of_State[i] = Current_State
			i = i + 1
		dict = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'RRC_Connected':0} #2:Cell_FACH, 3:Cell_DCH, 4:Cell_PCH 5:URA_PCH
		i = 0
		j = 0
		Current_Technology = List_Of_State[0]
#		print "-----------------",List_Of_State[0]
		for elements in List_Of_State:
			elements = elements.strip(' ')
			if(Current_Technology.find(elements)==-1):
				previous_elements = List_Of_State[j-1].strip(' ')
				dict[previous_elements] = float(dict[previous_elements]) + Time_difference(List_Of_Time[j-1],List_Of_Time[i])
#			print dict[previous_elements],List_Of_Time[j-1],List_Of_Time[i],previous_elements,Current_Technology
				i = j
				Current_Technology = List_Of_State[j].strip(' ')
			j = j + 1
		dict[Current_Technology] = float(dict[Current_Technology]) + Time_difference(List_Of_Time[j-1],List_Of_Time[i])

		dict['RRC_Connected'] = dict['2']+dict['3']+dict['4']+dict['5']
		return dict
	except Exception:
		print 'Error:Error returned by the Calculate_Time_RRC_State_Information'
		return 0


def Time_difference(Time_string_untillintialised,Time_string_intialised):
	"""
	Takes two time string and returns the difference between them in seconds
	"""
	Time_difference = Get_Epoc_time_in_millisec(Time_string_untillintialised) - Get_Epoc_time_in_millisec(Time_string_intialised)
	return Time_difference

def Calculate_Time_Technologies_L3Messages(csvfileBuffer):
	try:
		csvList = csv.reader(csvfileBuffer, delimiter=',')
		csvfileBuffer.seek(0)
		FirstLine = next(csvList)
		seek = csvfileBuffer.tell()
		List_Of_Technology = getColumnValuesByName('Technology ',seek,FirstLine,csvList,csvfileBuffer)
		List_Of_Time = getColumnValuesByName('Time Stamp ',seek,FirstLine,csvList,csvfileBuffer)
		Current_Technology = List_Of_Technology[0].strip(' ')
		dict = {'WCDMA':0,'GSM':0,'LTE':0,'0':0,'Total':0}
		i = 0
		j = 0
		for elements in List_Of_Technology:
			elements = elements.strip(' ')
			if(Current_Technology.find(elements)==-1):
				previous_elements = List_Of_Technology[j-1].strip(' ')
				dict[previous_elements] = float(dict[previous_elements]) + Time_difference(List_Of_Time[j-1],List_Of_Time[i])
#			print dict[previous_elements],List_Of_Time[j-1],List_Of_Time[i]
				i = j
				Current_Technology = List_Of_Technology[j].strip(' ')
			j = j + 1
		dict[Current_Technology] = float(dict[Current_Technology]) + Time_difference(List_Of_Time[j-1],List_Of_Time[i])
		dict['Total'] = Time_difference(List_Of_Time[-1],List_Of_Time[0])
		return dict
	except Exception:
		print 'Error:Error returned by the Calculate_Time_Technologies_L3Messages'
		return {'WCDMA':0,'GSM':0,'LTE':0,'0':0,'Total':0}

def getColumnValuesByName(string,seek,FirstLine,csvList,csvfileBuffer):
	Index = FirstLine.index(string)
	csvfileBuffer.seek(seek)
	Output_list = []
	for elem in csvList:
		Output_list.append(elem[Index])
	Output_list = filter(None, Output_list)
	return Output_list
