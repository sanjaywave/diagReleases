import numpy
import datetime
import sys
'''
set the pricision value of output to 16 ex:-0.1234567891234567
'''
numpy.set_printoptions(precision=16)

class ParseCSV(object):
    '''
    This class loads and parses a csv file to a numpy list array. Exposes various mathematical functions to calculate stats 
    '''
    csvList = None
    
    def __init__(self, csv_file):
        '''
        Constructor
        '''
        if csv_file is None:
            print "invalid input type input format python filename.py -i inputfolder"
            sys.exit(2)
        self.csvList = numpy.loadtxt(csv_file, dtype=str, delimiter=',')
    def striplist(self,l):
        '''
        This deletes ' ' at the end of pased string
        '''        
        return([x.strip() for x in l])
    
    def index_containing_substring(self,the_list, substring):
        '''
        Search for a substrin in the list
        '''

#	if substring in 'PS_With_CSFBMO_SuccessCount':
#		print "  ^^^^^----indexxxxxxxxxxxxx ", i
        for i, s in enumerate(the_list):
		if substring in s:
			return i
        return -1
    def getColumnIndexByName(self, columnName):
        '''
        returns the Column index of the input string in the file
        '''
	return self.index_containing_substring(self.csvList[0],columnName)
#        return self.index_containing_substring(self.csvList[0],columnName)
    def getAllColumnValuesByIndex(self, columnIndex):
        '''
        returns a list of values in the coloum without the none '' values
        '''
        try:
            output_list = self.csvList[1:,columnIndex]
            output_list = filter(lambda a: a != ' ', output_list)
            output_list = filter(None, output_list)
            return output_list
        except Exception:
            print 'Exception:One of the pased file is empty'
            return []

    def getAllColumnValuesByIndexWithSpaces(self, columnIndex):
        return self.csvList[1:,columnIndex]


    def getLastValue(self,columnIndex):
        '''
        returns last value in the pased column
        '''
        try:
        	return self.csvList[-1][columnIndex]
        except Exception:
        	print 'Warning:No elements in the list'
        	return 0

    def getNumOfValuesInColumn(self,columnIndex):
        '''
        returns count of values in the column
        '''
        try:
            colList = self.csvList[1:,columnIndex]
            colList = filter(None, colList)
            colList = filter(lambda a: a != ' ', colList)
            return len(colList)
        except Exception:
            print 'Exception:One of the pased file is empty'
            return []

    def getSumOfValuesInColumn(self,columnIndex):
        '''
        returns sum of values in the column
        '''
        try:
            colList = self.csvList[1:,columnIndex]
            colList = filter(None, colList)
            colList = filter(lambda a: a != ' ', colList)
            colList = map(float, colList)
            return sum(colList)
        except Exception:
            print 'Exception:One of the pased file is empty'
            return []
    '''
    not used anywhere
    def getLogSumOfValuesInColumn(self,columnIndex, base=10):
        """
        This is to be worked out
        """
        colList = self.csvList[1:,columnIndex]
        # assuming the values are in log form ...doubt here...
        colList = filter(None, colList)
        colList = map(float, colList)
        return sum(colList)
    '''
    def getAverageValueInColumn(self,columnIndex):
        '''
        returns average value of values in coloum
        '''
        try:
#            print self.getSumOfValuesInColumn(columnIndex),self.getNumOfValuesInColumn(columnIndex)
            return self.getSumOfValuesInColumn(columnIndex)/self.getNumOfValuesInColumn(columnIndex)
        except Exception:
            print "Warning:Zero input to the denominator while calculating average"
            return ''

    def getMedianValueInColumn(self,columnIndex):
        '''
        returns Median values of the elements of column
        '''
        inputList = self.getAllColumnValuesByIndex(columnIndex)
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


    def getPercentageValueInColumn(self,columnIndex,maxValue):
        '''
        returns percantage value of values
        '''
        return (self.getSumOfValuesInColumn(self.csvList,columnIndex)/(self.getNumOfValuesInColumn(self.csvList,columnIndex)*maxValue) *100)
