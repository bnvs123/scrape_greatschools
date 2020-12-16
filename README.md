# scrape_greatschools

1) We use cities_all.csv containing list of all US cities with longitudes and latitudes 

2) scrape_greatschools.py gives nearby schools within longitude, latitude

3) scrape_schoolprofile.py gives detailed information on enrollment, teacher - student ratio and Demographics. 

4) remove_school_dups.py removes schools which appear more than once. 

5) Great schools api can only work with a longitude, latitude and radius, as we didn't want to miss any schools in our extract, we are greedy in setting the radius to a smaller number and then filter any schools when cities are closeby or dont have a 20m radius and get captured multiple times.