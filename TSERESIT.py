import pytesseract #optical character recognition
import pandas #used to import and manipulate excel file data in python
import webbrowser #used to open the recipe link in the browser
from PIL import Image
import time
#below is used so user selects their image from the dialogue box/file directory rather than manually typing the file path
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename




def openrecipe(filename):
    img = Image.open(filename)#image file used
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'#location of the tesseract executable
    string=( pytesseract.image_to_string(img) )#the detected text from the image stored in a string
    words=(string.split())#stores list of the words detected on the image

    if(len(words))==0:
        print("Could not detect any text")

    for x in range (len(words)):#converts each word to lowercase (as items in excel are in lowercase)
        words[x]=words[x].lower()



    df = pandas.read_csv ('Recipes-All Recipes.csv')
    data=(df['ingredients'])

    count=0#stores the number of matched words
    for word in words:#compares each word detected on the image to each word under the 'ingredients' column in the excel file
        for e in data:
            if type(e) is str:#checks if string
                li=e.split(',')#seperates ingredients for a recipe in a list 
                if word in li:
                    if count==0:
                        print('ingredient:', word, '\n')
                    count+=1
                    recipe=(df.loc[df.ingredients == e, 'Link'].values[0])#gets the value from link column on same row as ingredients column
                    if recipe==str(recipe):#checks if recipe is a string (as some records are empty)
                        print('recipe:',(df.loc[df.ingredients == e, 'Name'].values[0]))#name of recipe
                        print('ingredients required:', li)#outputs the list of ingredients that with at least one in the list having been matched
                        print(recipe,'\n')
                        webbrowser.open(recipe)#opens recipe on user's default browser
         


    if count==0 and (len(words))>0:
        print('The text detected did not match items in the library')
        


print('in a few seconds, please select an image...')
time.sleep(3)

Tk().withdraw()
filename = askopenfilename()
openrecipe(filename)
