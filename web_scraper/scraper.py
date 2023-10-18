import mechanicalsoup

from web_scraper.handlers.element_handler import ElementHandler
from web_scraper.handlers.session_handler import SessionHandler


class WebScraper:
    def __init__(self, url, input_id, element_id):
        self.url = url
        self.input_id = input_id
        self.element_id = element_id

    def run(self):
        browser = mechanicalsoup.StatefulBrowser()
        try:
            browser.open(self.url)
            bill_no = input("Enter the Bill number you want to get information for: ")
            session_handler = SessionHandler()
            selected_session_value = session_handler.select_session()
            if not selected_session_value:
                return

            input_element = browser.page.find("input", {"id": self.input_id})
            response = browser.submit(
                input_element,
                url=f"{self.url}BillInfo.aspx?Bill={bill_no}&Session={selected_session_value}"
            )

            element_handler = ElementHandler(response, bill_no)
            element_handler.handle_elements()
        except Exception as e:
            print(str(e))
