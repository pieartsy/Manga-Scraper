#lets app accept command line arguments
import sys

#imports the gui aspect of pyqt
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit, QVBoxLayout, QInputDialog)
from PyQt5.QtGui import QIcon

# Regex library.
import re

# Library that parses files.
import requests

# Library that extracts info from files.
from bs4 import BeautifulSoup

import os.path


#variables for the scraper
# the URL for the first page you want to scrape
first_page = ""
# the URl for the last page you want to scrape (optional)
last_page = ""
# what the next button's text is
next_button = ""
# the name of the manga series as it is in the URLs
series_name = ""
# sometimes the next link only contains the partial URL. this will fill in the full URL
URL_beginning = ""
# where you want to save
save_path = ""

#form class called Dialog with 6 rows and 2 buttons
class Dialog(QDialog):
    NumGridRows = 6
    NumButtons = 2

    def __init__(self):
        super(Dialog, self).__init__()
        self.createFormGroupBox()
        #two buttons, the first one runs the run_button_clicked function and the second one exits the program
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.run_button_clicked)
        buttonBox.rejected.connect(self.reject)


        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
        #sets window title to "Manga Scraper" and the icon next to the title to this weeb anime pic
        self.setWindowTitle("Manga Scraper")
        self.setWindowIcon(QIcon('weeb.png'))


    def createFormGroupBox(self):
        #makes variables that can store text
        self.first_page_edit = QLineEdit(self)
        self.last_page_edit = QLineEdit(self)
        self.next_button_edit = QLineEdit(self)
        self.series_name_edit = QLineEdit(self)
        self.URL_beginning_edit = QLineEdit(self)
        self.save_path_edit = QLineEdit(self)

        #makes a form box labeled "Manga Scraper" with 6 rows, each with a label and a box to input text into
        self.formGroupBox = QGroupBox("Manga Scraper")
        layout = QFormLayout()
        layout.addRow(QLabel("First page"), self.first_page_edit)
        layout.addRow(QLabel("Last page"), self.last_page_edit)
        layout.addRow(QLabel("Next button"), self.next_button_edit)
        layout.addRow(QLabel("Series name"), self.series_name_edit)
        layout.addRow(QLabel("Beginning of URL"), self.URL_beginning_edit)
        layout.addRow(QLabel("File path"), self.save_path_edit)
        self.formGroupBox.setLayout(layout)
    
    #saves the text in each input box into their respective variables
    def run_button_clicked(self):
        first_page = self.first_page_edit.text()
        last_page = self.last_page_edit.text()
        next_button = self.next_button_edit.text()
        series_name = self.series_name_edit.text()
        URL_beginning = self.URL_beginning_edit.text()
        save_path = self.save_path_edit.text()
        return first_page, last_page, next_button, series_name, URL_beginning, save_path

if __name__ == '__main__':
    #opens app
    app = QApplication(sys.argv)
    dialog = Dialog()
    #exit code
    dialog.exec_()

#---Scraper code---

# While there's a next page/chapter, this loop will run.
# If there's no 'next chapter' or 'next' button, this loop will break (stop).
while first_page and first_page != last_page:
    
    # Optional print to see your progress through the chapters.
    print(first_page)
    
    # Requests parses the page (your URL).
    response = requests.get(first_page)
    
    # BeautifulSoup takes the parsed page and stores it in 'soup' as an HTML file.
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Finds all links that have $next_button and lead to the next page.
    # href looks for the links that contain $series_name specifically.
    end_URL = soup.find(string=next_button, href=re.compile(series_name))

    # Gets all images from the page.
    img_tags = soup.find_all('img')
        
    # Finds the source URL of the images found.
    URLs = [img['src'] for img in img_tags]
    
    # For each URL in the URLs list
    for URL in URLs:
    
        # Names a file after the URL
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', URL)
        
        with open(os.path.join(save_path, filename.group(1)), 'wb') as f:
            
            if 'http' not in URL:
                #  Sometimes an image source can be relative.
                # If it is, this code provides the base URL, which also happens to be the page variable at the moment. 
                URL = '{}{}'.format(first_page, URL)
                
            # Parse the URL file (the image source)
            response = requests.get(URL)
            
            # Write URL file to local directory file
            f.write(response.content)
            
    # If there is no next page, this breaks the loop before it returns an error.
    if end_URL == None:
        break
    else:
        # Changes the URL of the page being read in the loop to the next page.
        first_page = URL_beginning + end_URL['href']
