@app.route('/run')
def scraper_app():
    #---Scraper code---
    #variables for the scraper
    # the URL for the first page you want to scrape
    first_page = request.form['first_page']
    # the URl for the last page you want to scrape (optional)
    last_page = request.form['last_page']
    # what the next button's text is
    next_button = request.form['next_button']
    # the name of the manga series as it is in the URLs
    series_name = request.form['series_name']
    # sometimes the next link only contains the partial URL. this will fill in the full URL
    URL_beginning = request.form['URL_beginning']
    # where you want to save
    save_path = request.form['save_path']
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