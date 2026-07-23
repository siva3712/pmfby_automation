from playwright.sync_api import TimeoutError

from wait_engine import WaitEngine
from pmfby_selectors import Selectors


class PMFBYNavigator:

    def __init__(self, browser):

        self.browser = browser
        self.page = browser.get_page()

        self.wait = WaitEngine(
            self.page
        )

    ###################################################

    def select_scheme(self):

        print("Waiting for Scheme Selection...")

        self.wait.visible(
            self.page.get_by_role(
                "button",
                name="Submit"
            )
        )

    ###################################################

    def submit_scheme(self):

        self.page.get_by_role(
            "button",
            name="Submit"
        ).click()

        self.wait.ajax_complete()

    ###################################################

    def open_kcc_beneficiary(self):

        print("Opening KCC Beneficiary...")

        self.page.get_by_text(
            "or go to KCC Beneficiary tab"
        ).click()

        self.wait.ajax_complete()

    ###################################################

    def select_branch(self, branch_value):

        print(f"Selecting Branch : {branch_value}")

        combo = self.page.get_by_role(
            "combobox"
        )

        self.wait.dropdown_loaded(
            combo
        )

        combo.select_option(
            value=branch_value
        )

        self.wait.ajax_complete()

        self.page.get_by_role(
            "link",
            name="Submit"
        ).click()

        self.wait.ajax_complete()

    ###################################################

    def search_account(self, account_no):

        print(f"Searching Account : {account_no}")

        self.page.locator(
            Selectors.SEARCH_BY
        ).select_option(
            "2"
        )

        self.page.locator(
            Selectors.ACCOUNT_NO
        ).fill(
            account_no
        )

        self.page.locator(
            Selectors.SEARCH_BUTTON
        ).click()

        # self.wait.ajax_complete()

    ###################################################

    def has_pending_application(self):

        try:

            self.page.get_by_role(
                "link",
                name="Create Policy"
            ).wait_for(
                timeout=5000
            )

            return True

        except TimeoutError:

            return False

    ###################################################

    def open_policy(self):

        self.page.get_by_role(
            "link",
            name="Create Policy"
        ).click()

        self.wait.ajax_complete()

        ################################################

        ## Ensure User is navigated to kccBeneficiaryDetails page

    def ensure_kcc_beneficiary_page(self):

        if not self.page.locator(Selectors.SEARCH_BY).is_visible(timeout=3000):
            raise Exception(
               "Please navigate to the KCC Beneficiary page, select the branch, and click Submit before starting the upload."
            )

    ##########################################################

  ##########################################################

   ##########################################################

    def return_to_kcc_beneficiary(self):

        ##################################################
        # Maximum recovery attempts
        ##################################################

        for _ in range(5):

            ##################################################
            # Already on KCC page
            ##################################################

            if self.is_kcc_beneficiary_page():

                self.prepare_account_search()

                return True

            ##################################################
            # Preview Page
            ##################################################

            if self.try_back():

                continue

            ##################################################
            # Aadhaar Page
            ##################################################

            if self.try_go_to_kcc():

                continue

            ##################################################
            # Give React time
            ##################################################

            self.page.wait_for_timeout(500)

        ##################################################

        return False

    ##########################################################

    def try_back(self):

        try:

            back = self.page.get_by_text(
                "← Back",
                exact=True
            )

            if back.is_visible(timeout=1000):

                back.click()

                # self.wait.ajax_complete()
                self.page.wait_for_timeout(500)

                return True

        except Exception:

            pass

        return False

        ##########################################################

    def try_go_to_kcc(self):

        ##################################################
        # Yellow shortcut
        ##################################################

        try:

            link = self.page.get_by_text(
                "Go to KCC Beneficiary",
                exact=True
            )

            if link.is_visible(timeout=1000):

                link.click()

                # self.wait.ajax_complete()
                self.page.wait_for_timeout(500)

                return True

        except Exception:

            pass

        ##################################################
        # Top navigation (future proof)
        ##################################################

        try:

            others = self.page.get_by_text(
                "Others",
                exact=True
            )

            if others.is_visible(timeout=500):

                others.click()

                self.page.get_by_text(
                    "KCC Beneficiary",
                    exact=True
                ).click()

                # self.wait.ajax_complete()
                self.page.wait_for_timeout(500)

                return True

        except Exception:

            pass

        return False

    ##########################################################

    def is_kcc_beneficiary_page(self):

        try:

            search = self.page.get_by_role(

                "textbox",

                name="Enter Account Number"

            )

            return search.is_visible(timeout=1000)

        except Exception:

            return False

    def prepare_account_search(self):

        ##################################################
        # Wait for Search By
        ##################################################

        search_by = self.page.locator(
            Selectors.SEARCH_BY
        )

        self.wait.visible(
            search_by
        )

        ##################################################
        # Always Search by Account Number
        ##################################################

        search_by.select_option("2")

        ##################################################
        # Wait for Account textbox
        ##################################################

        account_box = self.page.locator(
            Selectors.ACCOUNT_NO
        )

        self.wait.visible(
            account_box
        )

        ##################################################
        # Clear previous value
        ##################################################

        account_box.click()

        account_box.press("Control+A")

        account_box.press("Delete")