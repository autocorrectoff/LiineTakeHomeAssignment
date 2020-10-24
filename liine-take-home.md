### Liine Take Home 

__Python is preferred, but if you feel unable to complete it using python, use whatever programming language you feel most comfortable in.__

Take a CSV file of restaurant names and a human-readable, string-formatted list of open hours (example csv given in this gist) and write a function `find_open_restaurants(csv_filename, search_datetime)` which takes as parameters a filename and a datetime object and returns a list of restaurant names which are open on that date and time. Optimized solutions are great, but correct solutions are more important. Make sure whatever solution you come up with can account for restaurants with hours not included in the examples given in the CSV.

### Assumptions:
* If a day of the week is not listed, the restaurant is closed on that day
* All times are local — don’t worry about timezone-awareness
* The CSV file will be well-formed, assume all names and hours are correct

If you have any questions, let me know. Use git to track your progress, and push your solution to a github repository (public or if private just give me access @sharpmoose)