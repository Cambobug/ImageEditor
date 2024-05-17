import imageEditor as editor
from PIL import Image, ImageOps, ImageTk
import os as o
import tkinter as tk

folderPath = "C:\\Users\\Owner\\OneDrive\\University Files\\CIS 4720\\Final Project\\images\\"
#folderPath = "C:\\Users\\Cambo\\OneDrive\\University Files\\CIS 4720\\Final Project\\images\\"
imgFiles = o.listdir(folderPath)

try:
    selectedImage = Image.open(folderPath + imgFiles[1])
    selectedImage = selectedImage.convert("RGBA")
except:
    print("ERROR: Unable to open image.")

selectedImageName = imgFiles[1]
width, height = selectedImage.size
currImage = editor.UserImage(selectedImage, True, width, height)

loopProg = True

print("Welcome to Cameron's Image Toolbox!")

while(loopProg):
    
    print("-------------------------------------------------")
    print("The current image being edited is: " + selectedImageName + "\n")
    print("Please select an image manipulation from the following options:")
    print("     0. Display current image")
    print("     1. Change current working image")
    print("     2. Convert image to gray level image")
    print("     3. Crop Image")
    print("     4. Flip Image")
    print("     5. Resize Image")
    print("     6. Rotate Image")
    print("     7. Linear Mapping")
    print("     8. Power Map")
    print("     9. Show Image Histogram (Gray-Level Only)")
    print("     10. Histogram Equalization (Gray-Level Only)")
    print("     11. Gray-Level Convolution (Gray-Level Only)")
    print("     12. RGB-Level Convolution (RBG-Image Only)")
    print("     13. Order-Statistic Filtering (Gray-Level Only)")
    print("     14. Min-Filter (Gray-Level Only)")
    print("     15. Median-Filter (Gray-Level Only)")
    print("     16. Max-Filter (Gray-Level Only)")
    print("     17. Alpha-Trimmed Filtering (Gray-Level Only)")
    print("     18. Save current Image")
    print("     19. End Program")
    print("-------------------------------------------------")
    
    userInput = input("User Choice: ")

    

    try:
        if((int(userInput) >= 0) and (int(userInput) <= 20)):
            if(userInput == '19'):
                loopProg = False
            
            elif(userInput == '0'):
                
                currImage.getImg().show()
                
            elif(userInput == '1'):
                
                userImage = input("Please enter new image name: ")
                foundImage = False
                for i in imgFiles:
                    if(userImage == i):
                        foundImage = True
                
                if(foundImage == True):
                    selectedImageName = userImage
                    try:
                        selectedImage = Image.open(folderPath + userImage)
                        selectedImage = selectedImage.convert("RGBA")
                        width, height = selectedImage.size
                        currImage = editor.UserImage(selectedImage, True, width, height)
                    except:
                        print("Failed to open image!")
                        
            elif(userInput == '2'):
                
                currImage = currImage.convertToGray()
                
            elif(userInput == '3'):
                
                cropWidth = input("Input new width: ")
                cropHeight = input("Input new height: ")
                cropStartX = input("Input Y start position: ")
                cropStartY = input("Input X start position: ")
                
                currImage = currImage.crop(int(cropWidth), int(cropHeight), int(cropStartX), int(cropStartY))
                
            elif(userInput == '4'):
                
                axis = input("Would you like to flip along the X or Y axis: ")
                if(axis == "Y"):
                    currImage = currImage.flipHorizontal()
                elif(axis == "X"):
                    currImage = currImage.flipVertical()
                else:
                    print("Invalid user input!")
                    
            elif(userInput == '5'):
                
                yDim = input("New width: ")
                xDim = input("New height: ")
                method = input("Nearest Neightbour Method or Bilinear (NN/B): ")
                
                if(method == "NN"):
                    currImage = currImage.scaleImage(int(yDim), int(xDim), 0)
                elif(method == "B"):
                    currImage = currImage.scaleImage(int(yDim), int(xDim), 1)
                else:
                    print("Invalid user input!")
                    
            elif(userInput == '6'):
                
                angle = input("Angle of rotation in degrees: ")
                
                currImage = currImage.rotate(int(angle))
                
            elif(userInput == '7'):
                
                print("Linear Mapping: aX + b")
                a = input("Input gain: ")
                b = input("Input bias: ")
                
                currImage = currImage.linearMap(float(a), int(b))
                
            elif(userInput == '8'):
                
                gamma = input("Input gamma: ")
                
                currImage = currImage.powerMap(float(gamma))
                
            elif(userInput == '9'):
                
                currImage.histogram()
                
            elif(userInput == '10'):
                
                currImage = currImage.histoEqualization()
                
            elif(userInput == '11'):
                
                convFolderPath = "C:\\Users\\Owner\\OneDrive\\University Files\\CIS 4720\\Final Project\\kernels\\"
                #convFolderPath = "C:\\Users\\Cambo\\OneDrive\\University Files\\CIS 4720\\Final Project\\kernels\\"
                m = input("Please input width of kernel: ")
                n = input("Please input height of kernel: ")
                kernelFile = input("Please input kernel file name: ")
                
                currImage = currImage.grayConvolution(int(m), int(n), convFolderPath + kernelFile)
                
            elif(userInput == '12'):
                
                convFolderPath = "C:\\Users\\Owner\\OneDrive\\University Files\\CIS 4720\\Final Project\\kernels\\"
                #convFolderPath = "C:\\Users\\Cambo\\OneDrive\\University Files\\CIS 4720\\Final Project\\kernels\\"
                m = input("Please input width of kernel: ")
                n = input("Please input height of kernel: ")
                kernelFile = input("Please input kernel file name: ")
                
                currImage = currImage.colourConvolution(int(m), int(n), convFolderPath + kernelFile)
                
            elif(userInput == '13'):
                
                m = input("Please input width of kernel: ")
                n = input("Please input height of kernel: ")
                kernelPos = input("Please input kernel position for filtering: ")
                
                currImage = currImage.orderStatisticFilter(int(kernelPos), int(m), int(n))
                
            elif(userInput == '14'):
                
                m = input("Please input width of kernel: ")
                n = input("Please input height of kernel: ")
                
                currImage = currImage.minFilter(int(m), int(n))
                
            elif(userInput == '15'):
                
                m = input("Please input width of kernel: ")
                n = input("Please input height of kernel: ")
                
                currImage = currImage.medianFilter(int(m), int(n))
                
            elif(userInput == '16'):
                
                m = input("Please input width of kernel: ")
                n = input("Please input height of kernel: ")
                
                currImage = currImage.maxFilter(int(m), int(n))
                
            elif(userInput == '17'):
                
                m = input("Please input width of kernel: ")
                n = input("Please input height of kernel: ")
                alpha = input("Please input alpha value for filtering: ")
                
                currImage = currImage.alphaTrimmedFilter(int(alpha), int(m), int(n))
                
            elif(userInput == '18'):
                
                fileName = input("Name of file: ")
                
                currImage.setImg(currImage.getImg().convert("RGB"))
                currImage.getImg().save(fileName + ".jpeg", "jpeg")
                
        else:
            print("Invalid user input!")
    except:
        print("Unexpected Error: Input may be invalid")



