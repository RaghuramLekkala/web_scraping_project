# Import necessary libraries for CSV handling and web scraping.
import csv
import mechanicalsoup

# Define the URL and IDs for the website elements we'll interact with.
url = "http://www.oklegislature.gov/"
input_id = "ctl00_ContentPlaceHolder2_txtBill"
element_id = "ctl00_ContentPlaceHolder2_btnBillSearch"

# Define a list of legislative sessions and their codes.
sessions = [
    "2023 Second Special Session",
    "2024 Regular Session",
    "2023 First Special Session",
    "2023 Regular Session",
    "2022 Third Special Session",
    "2022 Second Special Session",
    "2022 Regular Session",
    "2021 First Special Session",
    "2021 Regular Session",
    "2020 Second Special Session",
    "2020 Regular Session",
    "2020 First Special Session",
    "2019 Regular Session",
    "2018 Regular Session",
    "2017 Second Special Session",
    "2017 First Special Session",
    "2017 Regular Session",
    "2016 Regular Session",
    "2015 Regular Session",
    "2014 Regular Session",
    "2013 Special Session",
    "2013 Regular Session",
    "2012 Regular Session",
    "2011 Regular Session",
    "2010 Regular Session",
    "2009 Regular Session",
    "2008 Regular Session",
    "2007 Regular Session",
    "2006 Second Special Session",
    "2006 Regular Session",
    "2005 Special Session",
    "2005 Regular Session",
    "2004 Special Session",
    "2004 Regular Session",
    "2003 Regular Session",
    "2002 Regular Session",
    "2001 Special Session",
    "2001 Regular Session",
    "2012 Special Session",
    "2000 Regular Session",
    "1999 Special Session",
    "1999 Regular Session",
    "1998 Regular Session",
    "1997 Regular Session",
    "1996 Regular Session",
    "1995 Regular Session",
    "1994 Second Special Session",
    "1994 First Special Session",
    "1994 Regular Session",
    "1993 Regular Session"
]
session_values = ["232X",
                  "2400",
                  "231X",
                  "2300",
                  "223X",
                  "222X",
                  "2200",
                  "211X",
                  "2100",
                  "202X",
                  "2000",
                  "201X",
                  "1900",
                  "1800",
                  "172X",
                  "171X",
                  "1700",
                  "1600",
                  "1500",
                  "1400",
                  "131X",
                  "1300",
                  "1200",
                  "1100",
                  "1000",
                  "0900",
                  "0800",
                  "0700",
                  "062X",
                  "0600",
                  "051X",
                  "0500",
                  "041X",
                  "0400",
                  "0300",
                  "0200",
                  "011X",
                  "0100",
                  "121X",
                  "0000",
                  "991X",
                  "9900",
                  "9800",
                  "9700",
                  "9600",
                  "9500",
                  "942X",
                  "941X",
                  "9400",
                  "9300"]
# Create a mapping of element names to their corresponding table IDs.
element_table_mapping = {
    "History": "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1_tblHouseActions",
    "Amendments": "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2_tblAmendments",
    "BillSummaries": "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel3_tblBillSum",
    "Versions": "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel4_tblVersions",
    "Votes": "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel5_tblVotes",
    "Authors": "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel6_tblCoAuth"
}


# Function to display session options to the user.
def print_session_options():
    for i, session in enumerate(sessions):
        print(f"{i} - {session}")


# Function to save scraped data to a CSV file.
def scrape_to_csv(element, filename):
    if element:
        with open(filename, "w", newline=None) as csvfile:
            csvwriter = csv.writer(csvfile)
            # Extract and write table headers to the CSV file.
            headers = [header.text.strip() for header in element.find_all("th")]
            csvwriter.writerow(headers)

            # Extract and write each row of data to the CSV file.
            for row in element.find_all("tr")[1:]:
                cols = [col.text.strip() for col in row.find_all("td")]

                # Check if there's a link in the row, add it to the data.
                link_element = row.find("a", href=True)
                if link_element:
                    link = link_element["href"]
                else:
                    link = ""

                cols.append(link)
                csvwriter.writerow(cols)

        print(f"Data scraped and saved to {filename}.")
    else:
        print("Table not found on the web page.")


# Function to interact with the website, fill in values, and retrieve data.
def click_element(url_value, id_value):
    selected_session_value = ""

    browser = mechanicalsoup.StatefulBrowser()
    try:
        browser.open(url_value)
        value_to_fill = input("Enter the value to fill in the input field: ")
        print_session_options()
        selected_option = int(input("Enter the number of your selected session: "))

        # Check if the session option is valid.
        if 0 <= selected_option < len(session_values):
            selected_session_value = session_values[selected_option]
            print(f"Selected session value: {selected_session_value}")
        else:
            print("Invalid choice. Please select a valid option.")

        input_element = browser.page.find("input", {"id": id_value})
        response = browser.submit(input_element,
                                  url=f"{url_value}BillInfo.aspx?Bill={value_to_fill}&Session={selected_session_value}")
        return response
    except Exception as e:
        return str(e)


# Main part of the program that runs when the script is executed.
if __name__ == "__main__":
    # Main loop to repeat the entire process.
    while True:
        res = click_element(url_value=url, id_value=element_id)

        # Inner loop to select and scrape different elements.
        while True:
            print("Available keys for element_table_mapping:")
            for key in element_table_mapping.keys():
                print(key)
            select_element_to_scrape = input("Enter the key from element_table_mapping: ")

            table_id = element_table_mapping.get(select_element_to_scrape)
            if table_id:
                table_element = res.soup.find("table", {"id": table_id})
                scrape_to_csv(table_element, f"house_actions_{select_element_to_scrape.lower()}.csv")
            else:
                print("Invalid element selection. Please choose a valid key from element_table_mapping.")

            # Ask the user if they want to scrape another element.
            repeat = input("Do you want to scrape another element? (yes/no): ").lower()
            if repeat != "yes":
                break

        # Ask the user if they want to repeat the entire process.
        repeat_process = input("Do you want to repeat the entire process? (yes/no): ").lower()
        if repeat_process != "yes":
            break
