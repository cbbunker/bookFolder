import unittest
from imageProcessor import imageProcessor

CMPERPIXEL = 2.0

class bookFolding(object):
    def getInstructions(self, fileName, sheetsNeeded, totalPages):
        imageProc = imageProcessor()
        result = imageProc.getRangesFromImage(fileName, sheetsNeeded)
        print(result)

        result = self.scaleAndShiftAllColumns(result, 0)
        print(result)

        startPage = self.calculateStartPage(sheetsNeeded, totalPages)
        pagedResult = self.paginateColumns(result, startPage)
        print(pagedResult)

        print(self.printInstructionsToCSV(pagedResult, "test.csv" ))
        return result

    def scaleAndShiftAllColumns(self, rangeArray, shift):
        for i in range(len(rangeArray)):
            rangeArray[i] = self.scaleColumn(rangeArray[i], CMPERPIXEL)
            rangeArray[i] = self.shiftColumn(rangeArray[i], shift)
        return rangeArray

    def scaleColumn(self, colArray, cmPerPixel):
        result = []
        for i in range(len(colArray)):
            result.append(  tuple([cmPerPixel*x for x in colArray[i]  ]) )
        return result

    def shiftColumn(self, colArray, shift):
        result = []
        for i in range(len(colArray)):
            result.append(  tuple([x+shift for x in colArray[i]  ]) )
        return result

    def paginateArray(self,  arrayOfColArrays, startPage):
        for i in range(len(arrayOfColArrays)):
            arrayOfColArrays[i] = self.paginateColumns(arrayOfColArrays[i], startPage)
        return arrayOfColArrays

    def paginateColumns(self, arrayOfColArrays, startPage):
        result = []
        for i in range(len(arrayOfColArrays)):
            if  arrayOfColArrays[i] != []:
                result.append(  (startPage+i*2, arrayOfColArrays[i]  )   )
        return result

    #This is a little strange, 1 sheet needed with 5 pages gives us a page of 1
    def calculateStartPage(self, totalSheetsNeeded, totalBookPages):
        return int((totalBookPages - totalSheetsNeeded*2)/2)

    def printInstructionsFromPageMeasurementTuples(self, arrayOfPageArrays):
        result = ""
        for i in range(len(arrayOfPageArrays)):
            result += "Page: "+ str(arrayOfPageArrays[i][0])+", Fold 1: "+str(arrayOfPageArrays[i][1][0])+", Fold 2: "+str(arrayOfPageArrays[i][1][1])+"\n"
        return result

    def printInstructionsToCSV(self, arrayOfPageArrays, fileName):
        f = open(fileName, 'w+')
        result = "Page,Fold 1, Fold 2\n"
        for i in range(len(arrayOfPageArrays)):
            result += str(arrayOfPageArrays[i][0]) + "," + str(arrayOfPageArrays[i][1][0][0]) + "," + str(arrayOfPageArrays[i][1][0][1]) + "\n"
        f.write(result)
        return result


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_getInstructions(self):
        bF = bookFolding()
        bF.getInstructions("testFiles/batmanlogo.jpg", 60, 150)

    def test_printInstructiuons(self):
        bF = bookFolding()

        print(bF.printInstructionsFromPageMeasurementTuples([(5, (1.0, 0)), (6, (4, 0)), (8, (6, 0)), (9, (5, 4))]) )
        print(bF.printInstructionsToCSV([(5, (1.2, 0)), (6, (4, 0)), (8, (6, 0)), (9, (5, 4))], "instructions.csv") )

    def test_calculateStartPage(self):
        bF = bookFolding()

        result = bF.calculateStartPage(2, 20)

        self.assertEqual(result, 8 )

    def test_calculateStartPage_highNumber(self):
        bF = bookFolding()

        result = bF.calculateStartPage(160, 500)

        self.assertEqual(result, 90 )

    def test_paginateColumns_givenEmptyList_returnEmptyList(self):
        bF = bookFolding()

        arrayOfCol = []
        result = bF.paginateColumns(arrayOfCol, 5)

        self.assertEqual(result, [] )

    def test_paginateColumns_givenAList_returnPaginatedList(self):
        bF = bookFolding()

        arrayOfCol = [(1,0),(4,0), (), (6,0), (5,4)]
        result = bF.paginateColumns(arrayOfCol, 5)

        self.assertEqual(result, [ (5, (1,0)), (6,(4,0)), (8,(6,0)), (9,(5,4)) ])

    def test_scaleColumn_givenEmptyList_returnEmptyList(self):
        bF = bookFolding()

        col = []
        result = bF.scaleColumn(col, 1)

        self.assertEqual(result, [])

    def test_scaleColumn_givenOneItem_returnOneItemScaled(self):
        bF = bookFolding()

        col = [(1,2)]
        result = bF.scaleColumn(col, 2.0)

        self.assertEqual(result, [(2.0, 4.0)])

    def test_scaleColumn_givenTwoItems_returnTwoItemsScaled(self):
        bF = bookFolding()

        col = [(1,2), (4,4) ]
        result = bF.scaleColumn(col, 2.0)

        self.assertEqual(result, [(2.0, 4.0), (8.0, 8.0)])

    def test_transposeColumn(self):
        bF = bookFolding()

        col = [(1,2), (4.0,4.0) ]
        result = bF.shiftColumn(col, 0.5)

        self.assertEqual(result, [(1.5, 2.5), (4.5, 4.5)])

if __name__ == '__main__':
    unittest.main()
