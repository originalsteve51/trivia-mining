import re
from dbaccess import DatabaseAccessor

def extract_web_ids(filename):
    webids = []
    # Open the log file and read it line by line
    with open(filename, 'r') as file:
        for line in file:
            # Search for the substring followed by one or more numeric characters
            match = re.search(r'from web_id (\d+)', line)
            if match:
                # Convert the extracted substring to an integer and append to the list
                webid = int(match.group(1))
                webids.append(webid)
    return webids



if __name__ == "__main__":

    db = DatabaseAccessor('jtrivia.db')

    # Specify the path to the log file
    filename = 'jscrape.log'
    webids = extract_web_ids(filename)
    
    for webid in webids:
        db.update_webref_downloaded_for_webref(webid, False, True)