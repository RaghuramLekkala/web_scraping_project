import csv
import os


class CSVHandler:

    def __init__(self, element, filename, bill_no):
        self.element = element
        self.filename = filename
        self.bill_no = bill_no

    def save_to_csv(self):

        csv_path = os.path.join("scraped_data", self.bill_no)

        if os.path.exists(csv_path):
            pass
        else:
            os.makedirs(csv_path)

        csv_file_path = os.path.join(csv_path, self.filename)

        if self.element:
            with open(csv_file_path, "w", newline="") as csvfile:
                csvwriter = csv.writer(csvfile)
                headers = [header.text.strip() for header in self.element.find_all("th")]
                csvwriter.writerow(headers)

                for row in self.element.find_all("tr")[1:]:
                    cols = [col.text.strip() for col in row.find_all("td")]

                    link_element = row.find("a", href=True)
                    if link_element:
                        link = link_element["href"]
                    else:
                        link = ""

                    cols.append(link)
                    csvwriter.writerow(cols)

            print(f"Data scraped and saved to {csv_file_path}.")
        else:
            print("Table not found on the web page.")
