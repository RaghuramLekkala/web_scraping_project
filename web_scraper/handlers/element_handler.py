from web_scraper.handlers.csv_handler import CSVHandler


class ElementHandler:

    def __init__(self, response, bill_no):
        self.response = response
        self.bill_no = bill_no
        self.element_table_mapping = {
            "History": "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1_tblHouseActions",
            "Amendments": "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2_tblAmendments",
            "BillSummaries": "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel3_tblBillSum",
            "Versions": "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel4_tblVersions",
            "Votes": "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel5_tblVotes",
            "Authors": "ctl00_ContentPlaceHolder1_TabContainer1_TabPanel6_tblCoAuth"
        }

    def handle_elements(self):
        while True:
            print("Available keys for element_table_mapping:")
            for key in self.element_table_mapping.keys():
                print(key)
            select_element_to_scrape = input("Enter the key from element_table_mapping: ")

            table_id = self.element_table_mapping.get(select_element_to_scrape)
            if table_id:
                table_element = self.response.soup.find("table", {"id": table_id})
                if table_element:
                    filename = f"{select_element_to_scrape.lower()}.csv"
                    csv_handler = CSVHandler()
                    csv_handler.save_to_csv(table_element, filename, self.bill_no)
                else:
                    print(f"Table for '{select_element_to_scrape}' not found on the web page.")
            else:
                print("Invalid element selection. Please choose a valid key from element_table_mapping.")

            repeat = input("Do you want to scrape another element? (yes/no): ").lower()
            if repeat != "yes":
                break
