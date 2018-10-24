# Manga Scraper v1.2
# Maddie Fialla
# 7/5/18

#---Usage---

# This script iterates through each page of a manga series hosted online.
# On each page, it rips the image file that contains the actual comic page, and saves it to a directory.
# Then it effectively clicks 'Next' on the page, and navigates through the website that way.
# The default directory where images are saved to is the one where Manga Scraper v1 is located.

#---Version Notes---

# v1.1 removes an error at the end of the loop and adds more documentation.
# v1.2 clearer documentation, added variables for user changes
# v1.2.1 fixes a bug where the script wouldn't stop on the designated last page by changing 'is' to !=

#---Libraries---

# Regex library.
import re

# Library that parses files.
import requests

# Library that extracts info from files.
from bs4 import BeautifulSoup

import os.path

#---Variables that YOU the user should change as needed. Make sure they're within quotes.---

# Replace 'starting page' with your starting URL.
page = 'http://www1.readheroacademia.com/manga/boku-no-hero-academia-chapter-3/'

# If you want to break the loop before a certain webpage, replace 'last page' with that URL.
last_page = 'http://www1.readheroacademia.com/manga/boku-no-hero-academia-chapter-4/'

# Replace 'Next' with the text in the button that leads to the next page.
Next_button = 'Next Chapter'

# Change 'series name' as appropriate for the name of the series and how it's labeled in the page's URL.
# This can differ by site.
# It might look something like '/boku-no-hero-academia' or '/full-metal-alchemist'.
series_name = 'boku-no-hero-academia'

# You may need to look at what exactly the 'Next' link is. Sometimes it's the full URL for the next page and sometimes it's only part of it.
# For example, the 'Next' links at 'https://www.mangareader.net/' just look like this: '/boku-no-hero-academia/121/8'
# instead of the full URL, 'https://www.mangareader.net/boku-no-hero-academia/121/8'
        # If you're not sure this is the case, check the source code of the page for this.
        # If the script is only downloading the image of the first URL, it's probably the case.
            # https://www.computerhope.com/issues/ch000746.htm <--- Instructions for how to check the source code.
        # In the HTML source code, search 'Next' or whatever the button that takes you to the next page is called.
        # Look at the URL to the left of it in the brackets.
# If it's only a partial URL after all, add the beginning of the URL (in this example, 'https://www.mangareader.net') to this variable, replacing 'beginning of URL'.
beginning_of_URL = 'http://www1.readheroacademia.com/manga'

save_path = "C:/Users/Owner/Pictures/bnha"


#---Code---

# While there's a next page/chapter, this loop will run.
# If there's no 'next chapter' or 'next' button, this loop will break (stop).
while page and page != last_page:
    
    # Optional print to see your progress through the chapters.
    print(page)
    
    # Requests parses the page (your URL).
    response = requests.get(page)
    
    # BeautifulSoup takes the parsed page and stores it in 'soup' as an HTML file.
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Finds all links that have $Next_button and lead to the next page.
    # href looks for the links that contain $series_name specifically.
    end_URL = soup.find(string=Next_button, href=re.compile(series_name))

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
                URL = '{}{}'.format(page, URL)
                
            # Parse the URL file (the image source)
            response = requests.get(URL)
            
            # Write URL file to local directory file
            f.write(response.content)
            
    # If there is no next page, this breaks the loop before it returns an error.
    if end_URL == None:
        break
    else:
        # Changes the URL of the page being read in the loop to the next page.
        page = beginning_of_URL + end_URL['href']
