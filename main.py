from web_scraper.scraper import WebScraper

if __name__ == '__main__':
    url = "http://www.oklegislature.gov/"
    input_id = "ctl00_ContentPlaceHolder2_txtBill"
    element_id = "ctl00_ContentPlaceHolder2_btnBillSearch"

    while True:
        scraper = WebScraper(url, input_id, element_id)
        scraper.run()
        repeat = input("Do you want to repeat the entire process agian? (yes/no): ").lower()
        if repeat != "yes":
            break
