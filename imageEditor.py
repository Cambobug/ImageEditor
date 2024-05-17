from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math as m
import copy as c

class UserImage:
    def __init__(self, img, colour, width, height):
        self.img = img
        self.colour = colour
        self.width = width
        self.height = height

    def setImg(self, newImage):
        self.img = newImage

    def getImg(self):
        return self.img
    
    def setColour(self, colour):
        self.colour = colour

    def getColour(self):
        return self.colour

    def setWidth(self, newWidth):
        self.width = newWidth

    def getWidth(self):
        return self.width

    def setHeight(self, newHeight):
        self.height = newHeight

    def getHeight(self):
        return self.height
    
    def scaleColourLevels(self, img_Array):
        h = self.getHeight()
        w = self.getWidth()
        
        rMax = -100000
        rMin = 100000
        gMax = -100000
        gMin = 100000
        bMax = -100000
        bMin = 100000
        
        for y in range(0, h):
            for x in range(0, w):
                
                pixel = img_Array[y][x]
                
                #gets the max and min value in each of the 3 colour channels
                if(pixel[0] > rMax):
                    rMax = pixel[0]
                elif(pixel[0] < rMin):
                    rMin = pixel[0]
                    
                if(pixel[1] > gMax):
                    gMax = pixel[1]
                elif(pixel[1] < gMin):
                    gMin = pixel[1]
                    
                if(pixel[2] > bMax):
                    bMax = pixel[2]
                elif(pixel[2] < bMin):
                    bMin = pixel[2]
        
        #normalizes and scales each value down to a value between 0 255
        for y in range(0, h):
            for x in range(0, w):
                
                pixel = img_Array[y][x]
                
                scaledRValue = m.floor(((pixel[0] - rMin)/(rMax - rMin))*255)
                scaledGValue = m.floor(((pixel[1] - gMin)/(rMax - gMin))*255)
                scaledBValue = m.floor(((pixel[2] - bMin)/(bMax - bMin))*255)
                
                pixel[0] = int(scaledRValue)
                pixel[1] = int(scaledGValue)
                pixel[2] = int(scaledBValue)
                
        return img_Array
    
    #function converts an image to a gray level image
    def convertToGray(self):
        copy = self.getImg().copy()
        grayImg = copy.load()
        
        for i in range(0 ,self.width):
            for j in range(0, self.height):
                
                r,g,b,a = copy.getpixel((i,j))
                
                grayscale = (0.299*r + 0.587*g + 0.114*b)
                
                grayImg[i,j] = (int(grayscale), int(grayscale), int(grayscale))
                
        return UserImage(copy, False, self.width, self.height)

    #function crops and image
    def crop(self, nWidth, nHeight, xStart, yStart):
        if(xStart + nWidth > self.getWidth() or yStart + nHeight > self.getHeight()):
            print("ERROR: Inputted width or height exceeds the size of original image!")
            return

        #creates new image
        tempImg = Image.new("RGBA", size = (nWidth, nHeight))
        tempImg_Array = np.array(tempImg)

        #creates array for old image
        img = self.getImg()
        img_Array = np.array(img)

        #moves to starting point of crop and takes m*n pixels from there and places them in new image
        for y in range(yStart, yStart + nHeight):
            for x in range(xStart, xStart + nWidth):
                try:
                    pixel = img_Array[y][x]
                    tempImg_Array[y - yStart][x - xStart] = pixel
                except: 
                    print("ERROR: Crop operation attempted to access pixels not in the scope of the image!")
                    return self

        tempImg = Image.fromarray(tempImg_Array)
        return UserImage(tempImg, False, nWidth, nHeight)

    def flipHorizontal(self):
        #creates new image
        tempImg = Image.new("RGBA", size = (self.getWidth(), self.getHeight()))
        tempImg_Array = np.array(tempImg)

        #creates array for old image
        img = self.getImg()
        img_Array = np.array(img)
        h = self.getHeight()
        w = self.getWidth()

        # mirrors every picel on the y (x) axis
        for y in range(0, h):
            for x in range(0, w):
                try:
                    pixel = img_Array[y][x]
                    tempImg_Array[h - y - 1][x] = pixel
                except:
                    print(str(w) + " " + str(h))
                    print(str(y) + " " + str(x))
                    print("ERROR: Horizontal flip attempted to access pixels not in the scope of the image!")
                    return self
                
        tempImg = Image.fromarray(tempImg_Array)
                
        return UserImage(tempImg, False, self.width, self.height)

    def flipVertical(self):
        tempImg = Image.new("RGBA", size = (self.getWidth(), self.getHeight()))
        tempImg_Array = np.array(tempImg)

        img = self.getImg()
        img_Array = np.array(img)
        h = self.getHeight()
        w = self.getWidth()
        #mirrors every pixel on the x (y) axis
        for y in range(0, h):
            for x in range(0, w):
                try:
                    pixel = img_Array[y][x]
                    tempImg_Array[y][w - x - 1] = pixel
                except:
                    print(str(w) + " " + str(h))
                    print(str(y) + " " + str(x))
                    print("ERROR: Vertical flip attempted to access pixels not in the scope of the image!")
                    return self
                
        tempImg = Image.fromarray(tempImg_Array)
                
        return UserImage(tempImg, False, self.width, self.height)

    def scaleImage(self, newWidth, newHeight, method):
        tempImg = Image.new("RGBA", size = (newWidth, newHeight))
        newImage = UserImage(tempImg, True, newWidth, newHeight)

        img = self.getImg()
        oldHeight = self.getHeight()
        oldWidth = self.getWidth()
        
        heightRatio = newHeight / oldHeight # >0 if the new image is larger, <0 if the new image is smaller
        widthRatio = newWidth / oldWidth # >0 if the new image is larger, <0 if the new image is smaller
        
        newImgArray = np.array(newImage.getImg())
        oldImgArray = np.array(img)
        
        for y in range(0, oldHeight):
            for x in range(0, oldWidth):
                roundedY = round(y * heightRatio)
                roundedX = round(x * widthRatio)
                
                if(roundedY == newHeight):
                    roundedY -= 1
                if(roundedX == newWidth):
                    roundedX -= 1
                    
                newImgArray[roundedY][roundedX] = oldImgArray[y][x]
        
        if(heightRatio > 0 or widthRatio > 0): #will be missing pixels, need to add methods of scaling
            
            if(method == 0): #nearest neighbour method of scaling  
                for y in range(0, newHeight):
                    for x in range(0, newWidth):
                        pixel = newImgArray[y][x]
                        if((int(pixel[0]) + int(pixel[1]) + int(pixel[2]) + int(pixel[3])) == 0):
                            #print(str(y) + " " + str(x))
                            roundedY = round(y / heightRatio)
                            roundedX = round(x / widthRatio)
                            
                            if(roundedY == oldHeight):
                                roundedY -= 1
                            if(roundedX == oldWidth):
                                roundedX -= 1
                            
                            newImgArray[y][x] = oldImgArray[roundedY][roundedX]
            
            if(method == 1):
                for y in range(0, newHeight):
                    for x in range(0, newWidth):
                        pixel = newImgArray[y][x]
                        if((int(pixel[0]) + int(pixel[1]) + int(pixel[2]) + int(pixel[3])) == 0):
                            decimalY = (y / heightRatio)
                            decimalX = (x / widthRatio) # X.xxxxx
                            
                            x0 = round(np.floor(decimalX)) #gets the x postions of the left pixels
                            x1 = x0 + 1 #gets the x positions of the right pixels
                            y0 = round(np.floor(decimalY)) #gets the position of the top pixels
                            y1 = y0 + 1 #gets the position of the bottom
                            
                            s = decimalX - x0
                            t = decimalY - y0
                            
                            if(x1 == oldWidth):
                                x1 -= 1
                            if(y1 == oldHeight):
                                y1 -= 1
                            
                            a = oldImgArray[y0][x0] #top left 1
                            b = oldImgArray[y0][x1] #top right 3 
                            c = oldImgArray[y1][x0] #bottom left 2
                            d = oldImgArray[y1][x1] #bottom right 4

                            f1 = a * (1-s) + c * s
                            f2 = b * (1-s) + d * s
                            f = f1 * (1-t) + f2 * t
                            
                            newImgArray[y][x] = f
                            
                            
        newImage.setImg(Image.fromarray(newImgArray))      
        
        return newImage
    
    def rotate(self, angle):
        
        rads = m.radians(angle)
        
        img_Array = np.array(self.getImg())
        
        #determines the height and width of the image after the rotation
        rotatedHeight = round(abs(img_Array.shape[1] * m.sin(rads))) + round(abs(img_Array.shape[0] * m.cos(rads))) + 1
        rotatedWidth = round(abs(img_Array.shape[1] * m.cos(rads))) + round(abs(img_Array.shape[0] * m.sin(rads))) + 1
        
        #creates an array with an appropriate size to hold the image
        rotatedImg_Array = np.uint8(np.zeros((rotatedHeight, rotatedWidth, img_Array.shape[2]))) 
        
        midOrgX = img_Array.shape[1] // 2 #gets the middle of the original image on the x axis
        midOrgY = img_Array.shape[0] // 2 #gets the middle of the original image on the y axis
        
        midRotX = rotatedWidth // 2 #gets middle of the image on the x axis using the calculated size of the rotated image
        midRotY = rotatedHeight // 2 #gets middle of the image on the y axis using the calculated size of the rotated image

        #loops through the image
        for i in range(0, rotatedImg_Array.shape[0]):
            for j in range(0, rotatedImg_Array.shape[1]):
                
                #applies rotation formula to the pixel and based on the radians
                rotX = (i - midRotX)*m.cos(rads) + (j-midRotY)*m.sin(rads)
                rotY = -(i - midRotX)*m.sin(rads) + (j-midRotY)*m.cos(rads)
                
                #offsets the pixel by the origin
                rotX = round(rotX) + midOrgY
                rotY = round(rotY) + midOrgX
                
                # sets the pixel of the rotated image to its corresponding pixel in the original image
                if (rotX >= 0 and rotY >= 0 and rotX < img_Array.shape[0] and  rotY < img_Array.shape[1]):
                    rotatedImg_Array[i,j,:] = img_Array[rotX,rotY,:]
            
        rotatedImg = Image.fromarray(rotatedImg_Array) 
        rot = UserImage(rotatedImg, self.colour, rotatedWidth, rotatedHeight) 
        return  rot
    
    def linearMap(self, a, b):
        linImg = self.getImg().copy()

        h = self.getHeight()
        w = self.getWidth()

        linImg_Array = np.array(linImg)

        for y in range(0, h):
            for x in range(0, w):
                pixel = linImg_Array[y][x]

                pixel[0] = min(255, max(-255, (a*pixel[0]) + b))
                pixel[1] = min(255, max(-255, (a*pixel[1]) + b))
                pixel[2] = min(255, max(-255, (a*pixel[2]) + b))

        linImg = Image.fromarray(linImg_Array)
        newImage = UserImage(linImg, self.getColour(), self.getWidth(), self.getHeight())

        return newImage
 
    def powerMap(self, gamma):
        powImg = self.getImg().copy()

        h = self.getHeight()
        w = self.getWidth()

        powImg_Array = np.array(powImg)
        #applies power mapping formula on each channel of the pixel
        for y in range(0, h):
            for x in range(0, w):
                pixel = powImg_Array[y][x]

                pixel[0] = min(255, max( -255, (255)*pow( (pixel[0] / 255), gamma) ) ) 
                pixel[1] = min(255, max( -255, (255)*pow( (pixel[1] / 255), gamma) ) )
                pixel[2] = min(255, max( -255, (255)*pow( (pixel[2] / 255), gamma) ) )

        powImg = Image.fromarray(powImg_Array)
        newImage = UserImage(powImg, self.getColour(), self.getWidth(), self.getHeight())

        return newImage


    def histogram(self):
        if(self.getColour() == True):
            print("Histogram Error: Input image must be a gray level image")
            return

        h = self.getHeight()
        w = self.getWidth()

        img_Array = np.array(self.getImg())
        #creates an array holding every pixels value 
        img_HisArray = []
        for y in range(0, h):
            for x in range(0, w):
                pixel = img_Array[y][x]

                img_HisArray.append(pixel[0])
                
        plt.hist(img_HisArray, bins=255, range=[0,255])
        plt.show()

    def histoEqualization(self):
        if(self.getColour() == True):
            print("Histogram Error: Input image must be a gray level image")
            return
        
        histEquImg = self.getImg().copy()
        histEquImg_Array = np.array(histEquImg)
        
        h = self.getHeight()
        w = self.getWidth()
        hist_Array = np.zeros(256, dtype=int)
        #creates an array with the amount of each pixel value in order from 0 to 256
        for y in range(0, h):
            for x in range(0, w):
                pixel = histEquImg_Array[y][x]

                hist_Array[pixel[0]] += 1
                
        for y in range(0, h):
            for x in range(0, w):
                pixel = histEquImg_Array[y][x]
                
                value = 0
                
                #gets the cumulative normalized array of value pixel
                for i in range(0, pixel[0]):
                    value += hist_Array[i]/(h*w)
                    
                value = m.floor(255 * value)

                pixel[0] = value
                pixel[1] = value
                pixel[2] = value
        
        histEquImg = Image.fromarray(histEquImg_Array)
        newImage = UserImage(histEquImg, self.getColour(), self.getWidth(), self.getHeight())    
        
        return newImage          
    
    def grayConvolution(self, m, n, filePath):
        
        if(self.getColour() == True):
            print("Gray Convolution Error: Input image must be a gray level image")
            return self
        
        try:
            data = open(filePath, "r")
        except:
            print("Failed to open kernel file")
            return self
        #creates convolution kernel from a file
        convKernel = []
        for i in range(0, m):
            line = data.readline()
            line = line.strip()
            if(len(line) == 0):
                print("ERROR: Kernel is of height " + str(i) +". Expected: " + str(m))
                return self
            nums = line.split(" ")
            if(len(nums) != n):
                print("ERROR: Kernel is of width " + str(len(nums)) +". Expected: " + str(n))
                return self
            convRow = []
            for j in nums:
                convRow.append(float(c.deepcopy(j)))
            convKernel.append(c.deepcopy(convRow))
            
        h = self.getHeight()
        w = self.getWidth()
        #convolves the image
        orgImg = self.getImg()
        orgImg_Array = np.array(orgImg)
        convImg = self.getImg().copy()
        convImg_Array = np.array(convImg)
        
        if(m % 2 == 0): #even m
            iBoundStart = round(m/2)
            iBoundEnd = round(m/2)
        else:
            iBoundStart = round((m-1)/2)
            iBoundEnd = round((m-1)/2) + 1
            
        if(n % 2 == 0): #even n
            jBoundStart = round(n/2)
            jBoundEnd = round(n/2)
        else:
            jBoundStart = round((n-1)/2)
            jBoundEnd = round((n-1)/2) + 1
            
        
        for y in range(0, h):
            for x in range(0, w):
                total = 0
                
                for i in range(0 - iBoundStart, iBoundEnd):
                    for j in range(0 - jBoundStart, jBoundEnd):
                        #if the kernel is out of bounds
                        if((y - i < 0) or (y - i > h - 1)): #if the kernel pixel is out of bounds on the top or bottom
                            total += 0
                        elif((x - j < 0) or (x - j > w - 1)): #if the kernel pixel is out of bounds on the left or right
                            total += 0
                        else: #if the kernel pixel is in the bounds of the image
                            total += round(convKernel[i + iBoundStart][j + jBoundStart] * orgImg_Array[y - i][x - j][0])
                            
                pixel = convImg_Array[y][x]
                pixel[0] = total
                pixel[1] = total
                pixel[2] = total 
        
        convImg_Array = self.scaleColourLevels(convImg_Array)               
                            
        convImg = Image.fromarray(convImg_Array)
        newImage = UserImage(convImg, self.getColour(), self.getWidth(), self.getHeight())
        
        return newImage
    
    def colourConvolution(self, m, n, filePath):
        
        if(self.getColour() == False):
            print("Colour Convolution Error: Input image must be an RGB level image")
            return self
        
        data = open(filePath, "r")
        #creates convolution kernel from a file
        convKernel = []
        for i in range(0, m):
            line = data.readline()
            line = line.strip()
            if(len(line) == 0):
                print("ERROR: Kernel is of height " + str(i) +". Expected: " + str(m))
                return self
            nums = line.split(" ")
            if(len(nums) != n):
                print("ERROR: Kernel is of width " + str(len(nums)) +". Expected: " + str(n))
                return self
            convRow = []
            for j in nums:
                convRow.append(float(c.deepcopy(j)))
            convKernel.append(c.deepcopy(convRow))
            
        h = self.getHeight()
        w = self.getWidth()
        #convolves the image
        orgImg = self.getImg()
        orgImg_Array = np.array(orgImg)
        convImg = self.getImg().copy()
        convImg_Array = np.array(convImg)
        
        if(m % 2 == 0): #even m
            iBoundStart = round(m/2)
            iBoundEnd = round(m/2)
        else:
            iBoundStart = round((m-1)/2)
            iBoundEnd = round((m-1)/2) + 1
            
        if(n % 2 == 0): #even n
            jBoundStart = round(n/2)
            jBoundEnd = round(n/2)
        else:
            jBoundStart = round((n-1)/2)
            jBoundEnd = round((n-1)/2) + 1
        
        for y in range(0, h):
            for x in range(0, w):
                
                Rtotal = 0
                Gtotal = 0
                Btotal = 0
                
                for i in range(0 - iBoundStart, iBoundEnd):
                    for j in range(0 - jBoundStart, jBoundEnd):
                        if((y - i < 0) or (y - i > h - 1)): #if the kernel pixel is out of bounds on the top or bottom
                            Rtotal += 0
                            Gtotal += 0
                            Btotal += 0
                        elif((x - j < 0) or (x - j > w - 1)): #if the kernel pixel is out of bounds on the left or right
                            Rtotal += 0
                            Gtotal += 0
                            Btotal += 0
                        else: #if the kernel pixel is in the bounds of the image
                            Rtotal += round(convKernel[i + iBoundStart][j + jBoundStart] * orgImg_Array[y - i][x - j][0])
                            Gtotal += round(convKernel[i + iBoundStart][j + jBoundStart] * orgImg_Array[y - i][x - j][1])
                            Btotal += round(convKernel[i + iBoundStart][j + jBoundStart] * orgImg_Array[y - i][x - j][2])
                            
                pixel = convImg_Array[y][x]
                pixel[0] = Rtotal
                pixel[1] = Gtotal
                pixel[2] = Btotal
                
        convImg_Array = self.scaleColourLevels(convImg_Array)
                   
        convImg = Image.fromarray(convImg_Array)
        newImage = UserImage(convImg, self.getColour(), self.getWidth(), self.getHeight())
        
        return newImage
    
    def orderStatisticFilter(self, pos, m, n):
        
        if(self.getColour() == True):
            print("Order Statistic Filter Error: Input image must be a graylevel image")
            return self
        
        h = self.getHeight()
        w = self.getWidth()
        
        orgImg = self.getImg()
        orgImg_Array = np.array(orgImg)
        filtImg = self.getImg().copy()
        filtImg_Array = np.array(filtImg)
        
        for y in range(0, h):
            for x in range(0, w):
                
                iBound = round((m-1)/2)
                jBound = round((n-1)/2)
                
                vals_Array = []
                
                for i in range(0 - iBound, iBound + 1):
                    for j in range(0 - jBound, jBound + 1):                   
                        if((y - i > 0) and (y - i < h - 1) and (x - j > 0) and (x - j < w - 1)): #if the kernel pixel is in the bounds of the image
                            vals_Array.append(orgImg_Array[y - i][x - j][0])
                        else:
                            vals_Array.append(0)
                
                vals_Array.sort()
                if(pos > len(vals_Array)):
                    newPos = len(vals_Array) - 1
                    pixel = filtImg_Array[y][x]
                    pixel[0] = vals_Array[newPos]
                    pixel[1] = vals_Array[newPos]
                    pixel[2] = vals_Array[newPos]
                else:
                    pixel = filtImg_Array[y][x]
                    pixel[0] = vals_Array[pos]
                    pixel[1] = vals_Array[pos]
                    pixel[2] = vals_Array[pos]
                    
        filtImg = Image.fromarray(filtImg_Array)
        newImage = UserImage(filtImg, self.getColour(), self.getWidth(), self.getHeight())
        
        return newImage
    
    def minFilter(self, m, n):
        
        return self.orderStatisticFilter(0, m, n)
    
    def maxFilter(self, m, n):
        
        return self.orderStatisticFilter((m * n) - 1, m, n)
    
    def medianFilter(self, m, n):
        
        return self.orderStatisticFilter(round((m * n)/2), m, n)
    
    def alphaTrimmedFilter(self, alpha, m, n):
        
        if(self.getColour() == True):
            print("Alpha Trimmed Filter Error: Input image must be a graylevel image")
            return self

        h = self.getHeight()
        w = self.getWidth()
        
        orgImg = self.getImg()
        orgImg_Array = np.array(orgImg)
        filtImg = self.getImg().copy()
        filtImg_Array = np.array(filtImg)
        
        for y in range(0, h):
            for x in range(0, w):
                
                iBound = round((m-1)/2)
                jBound = round((n-1)/2)
                
                vals_Array = []
                
                for i in range(0 - iBound, iBound + 1):
                    for j in range(0 - jBound, jBound + 1):                   
                        if((y - i > 0) and (y - i < h - 1) and (x - j > 0) and (x - j < w - 1)): #if the kernel pixel is in the bounds of the image
                            vals_Array.append(orgImg_Array[y - i][x - j][0])
                        else:
                            vals_Array.append(0)
                
                vals_Array.sort()
                
                if(alpha * 2 >= len(vals_Array)):
                    print("Alpha Trimmed Filter Error: Alpha value exceeds half the size of mxn")
                    return self
                
                total = 0
                for i in range(0 + alpha, len(vals_Array) - alpha): #starts at alpha, goes until end-alpha
                    total += vals_Array[i]
                total = round(total/(len(vals_Array) - alpha*2))
                
                pixel = filtImg_Array[y][x]
                pixel[0] = total
                pixel[1] = total
                pixel[2] = total
        
        filtImg = Image.fromarray(filtImg_Array)
        newImage = UserImage(filtImg, self.getColour(), self.getWidth(), self.getHeight())
        
        return newImage