import tkinter as tkinter
import modules.output as output
import modules.image_processing as image_processing
import modules.painting as painting
from modules.window_management import setup_window

root = tkinter.Tk()
root.withdraw()

output.printMenu()
menuSelection = input("   Main Menu | Choose: ")

if menuSelection in ["1", "01"]:
    output.clear()
    output.printCustom()
    customSelection = input("   Custom Image | Choose: ")

    if customSelection in ["1", "01"]:
        image_pixels, image_name = image_processing.process_image_from_path()
    elif customSelection in ["2", "02"]:
        image_pixels, image_name = image_processing.process_image_from_url()
    else:
        output.clear()
        quit()

    painting.start_painting(image_pixels, image_name)

elif menuSelection in ["2", "02"]:
    output.printRandom()
    randomSelection = input("   Random Image | Choose: ")
    image_pixels, image_name = image_processing.process_random_image(randomSelection)

    painting.start_painting(image_pixels, image_name)

else:
    if menuSelection != "99":
        output.printError("Invalid option!")
    output.clear()
    quit()
