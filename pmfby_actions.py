from pmfby_selectors import Selectors
from wait_engine import WaitEngine


class PMFBYActions:

    def __init__(self, browser):

        self.browser = browser

        self.page = browser.get_page()

        self.wait = WaitEngine(
            self.page
        )

    ##################################################

    def save_and_continue(self):

        self.page.get_by_role(
            "button",
            name="Save & Continue"
        ).click()

        self.wait.ajax_complete()

    ##################################################

    def select_district(self, district):

        combo = self.page.locator(
            Selectors.DISTRICT
        )

        self.wait.dropdown_loaded(combo)

        combo.select_option(
            label=district
        )

        self.wait.ajax_complete()

    ##################################################

    def select_mandal(self, mandal):

        combo = self.page.locator(
            Selectors.MANDAL
        )

        self.wait.dropdown_loaded(combo)

        combo.select_option(
            label=mandal
        )

        self.wait.ajax_complete()

    ##################################################

    def select_gram_panchayat(self, gp):

        combo = self.page.locator(
            Selectors.GRAM_PANCHAYAT
        )

        self.wait.dropdown_loaded(combo)

        combo.select_option(
            label=gp
        )

        self.wait.ajax_complete()

    ##################################################

    def select_village(self, village):

        combo = self.page.locator(
            Selectors.VILLAGE
        )

        self.wait.dropdown_loaded(combo)

        combo.select_option(
            label=village
        )

        self.wait.ajax_complete()

    ##################################################

    def select_crop(self, crop_name):

        combo = self.page.get_by_role(
            "cell",
            name="Select",
            exact=True
        ).get_by_role(
            "combobox"
        )

        self.wait.dropdown_loaded(combo)

        combo.select_option(
            label=crop_name
        )

        self.wait.ajax_complete()