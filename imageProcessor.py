
import unittest, numpy
from email.mime import image

from PIL import Image

BLACK = 0
WHITE = 255

class imageProcessor(object):
    fileName = ""
    im = None

    def __init__(self):
        pass

    def getRangesFromImage(self, fileName,size=50):
        imageProc = imageProcessor()
        imageProc.loadImage(fileName)
        imageProc.cleanImage()
        imageProc.resizeImage(size)
        imageProc.cleanImage(30)
        imageProc.saveImageWithPostfix("BW")
        print(imageProc.printBWImage())
        result = imageProc.getColoredRangesFromImage()
        return result

    def loadImage(self, fileName):
        self.fileName = fileName
        self.im = Image.open(fileName)

    def cleanImage(self,threshold=120):
        self.im = self.im.convert('L')
        image = numpy.array(self.im)
        for i in range(len(image)):
            for j in range (len(image[0])):
                if image[i][j] > threshold:
                    image[i][j] = WHITE
                else:
                    image[i][j] = BLACK
        self.im = Image.fromarray(image)

    #Horizontal_size is the number of pages
    def resizeImage(self, horizontal_size):
        scalingFactor = self.im.getbbox()[2]/horizontal_size
        vertical_size = int(self.im.getbbox()[3]/scalingFactor)
        size = horizontal_size, vertical_size
        self.im = self.im.resize(size)

    def saveImageWithPostfix(self, postfix):
        self.im.save(self.fileName + "." + postfix, "BMP")

    def getColoredRangesFromImage(self):
        imageRanges = []
        self.im = self.im.rotate(90, expand = 1)
        self.saveImageWithPostfix("rotate")
        image = numpy.array(self.im)
        for col in range(len(image)):
            ranges = self.getRangesFromArray(image[col])
            print(ranges)
            imageRanges.append(ranges)
        return imageRanges

    def getRangesFromArray(self, columnArray, threshold = 0):
        resultList = []

        i = 0
        while (i < len(columnArray) ):
            if(columnArray[i] == BLACK):
                j = i+1
                while (  (j < len(columnArray)) and columnArray[j] == BLACK ):
                    j+=1
                resultList.append((i,j))
                i=j
            else:
                i+=1

        return resultList

    def printBWImage(self):
        totalImage = ""
        image = numpy.array(self.im)
        for i in range(len(image)):
            row = ""
            for j in range(len(image[0])):
                if image[i][j] == 0:
                    row += "."
                else:
                    row += " "
            totalImage += row +"\n"
        return totalImage

class imageProcessorTests(unittest.TestCase):
    def test_getRangesFromArray(self):
        imageProc = imageProcessor()
        indexArray = []
        result = imageProc.getRangesFromArray(indexArray)
        self.assertEqual(result, [])

    def test_getRangesFromArray_noBlack(self):
        imageProc = imageProcessor()
        indexArray = [WHITE, WHITE, WHITE]
        result = imageProc.getRangesFromArray(indexArray)
        self.assertEqual(result, [])

    def test_getRangesFromArray_oneBlack(self):
        imageProc = imageProcessor()
        indexArray = [BLACK]
        result = imageProc.getRangesFromArray(indexArray)
        self.assertEqual(result, [ (0,1) ])

    def test_getRangesFromArray_twoBlack(self):
        imageProc = imageProcessor()
        indexArray = [BLACK, BLACK]
        result = imageProc.getRangesFromArray(indexArray)
        self.assertEqual(result, [(0, 2)])

    def test_getRangesFromArray_fiveBlack(self):
        imageProc = imageProcessor()
        indexArray = [BLACK, BLACK, BLACK, BLACK, BLACK]
        result = imageProc.getRangesFromArray(indexArray)
        self.assertEqual(result, [(0, 5)])

    def test_getRangesFromArray_lots(self):
        imageProc = imageProcessor()
        indexArray = [WHITE, BLACK, BLACK, BLACK, BLACK, BLACK, WHITE, BLACK, BLACK, BLACK, WHITE, WHITE, WHITE, BLACK]
        result = imageProc.getRangesFromArray(indexArray)
        self.assertEqual(result, [(1,6), (7,10), (13,14)])

    def test_test(self):
        imageProc = imageProcessor()
        print(imageProc.getRangesFromImage("testFiles/batmanlogo.jpg",50))

if __name__ == '__main__':
    unittest.main()

