from playwright.sync_api import TimeoutError

from pmfby_selectors import Selectors


class LocationProcessor:

    ##########################################################

    def __init__(self, navigator, reporter):

        self.navigator = navigator
        self.page = navigator.page
        self.wait = navigator.wait
        self.reporter = reporter

    ##########################################################

    def process(self, account):

        try:

            self.select_district(account)

            self.select_mandal(account)

            self.select_gram_panchayat(account)

            self.select_village(account)

            return True

        except Exception as ex:

            self.reporter.error(

                account.account_no,

                "LOCATION",

                str(ex)

            )

            self.reporter.record_result(
                account=account.account_no,
                stage="LOCATION",
                status="FAILURE",
                message=str(ex)
            )

            return False
    def select_district(self, account):

        dropdown = self.page.locator(
            Selectors.INSURANCE_DISTRICT
        )

        self.reporter.info(

            account.account_no,

            "DISTRICT",

            f"Selecting : {account.district}"

        )

        self.wait.dropdown_loaded(dropdown)

        dropdown.select_option(
            label=account.district
        )

        ##################################################
        # Wait until React commits selection
        ##################################################

        value = ""

        for _ in range(20):

            value = dropdown.input_value()

            if value:

                break

            self.page.wait_for_timeout(100)

        if not value:

            raise Exception(
                "District selection failed."
            )

        ##################################################
        # Debug
        ##################################################

        # print("--------------------------------")
        # print("Selected Label :", account.district)
        # print("Selected Value :", value)
        # print("Selected Text  :", dropdown.locator("option:checked").text_content())
        # print("--------------------------------")

        ##################################################
        # Wait for Mandal to load
        ##################################################

        mandal = self.page.locator(
            Selectors.INSURANCE_MANDAL
        )

        self.wait.dropdown_loaded(
            mandal
        )

        ##################################################

        self.reporter.info(

            account.account_no,

            "DISTRICT",

            f"{account.district} selected."

        )
    def select_mandal(self, account):
        dropdown = self.page.locator(
            Selectors.INSURANCE_MANDAL
        )

        self.reporter.info(

            account.account_no,

            "MANDAL",

            f"Selecting : {account.mandal}"
        )

        self.wait.dropdown_loaded(
            dropdown
        )

        dropdown.select_option(
            label=account.mandal
        )

        ##################################################
        # Wait until selection is committed
        ##################################################

        value = ""

        for _ in range(20):

            value = dropdown.input_value()

            if value:

                break

            self.page.wait_for_timeout(100)

        if not value:

            raise Exception(
                "Mandal selection failed."
            )

        # print("--------------------------------")
        # print("Selected Mandal :", account.mandal)
        # print("Selected Value  :", value)
        # print("Selected Text   :", dropdown.locator("option:checked").text_content())
        # print("--------------------------------")

        ##################################################
        # Wait for Gram Panchayat to load
        ##################################################

        gram = self.page.locator(
            Selectors.INSURANCE_GRAM_PANCHAYAT
        )

        self.wait.dropdown_loaded(
            gram
        )

        self.reporter.log(

            account.account_no,

            "MANDAL",

            "SUCCESS",

            f"{account.mandal} selected."

        )

    def select_gram_panchayat(self, account):

        dropdown = self.page.locator(
            Selectors.INSURANCE_GRAM_PANCHAYAT
        )

        self.wait.dropdown_loaded(
            dropdown
        )

        ##################################################
        # Select Gram Panchayat
        gp = account.gram_panchayat.strip().lower()

        if gp in ("na","not available"):

            label = "not available"

        else:

            label = account.gram_panchayat

        ##################################################

        self.reporter.info(

            account.account_no,

            "GRAM_PANCHAYAT",

            f"Selecting : {label}"

        )

        dropdown.select_option(
            label=label
        )

        value = ""

        for _ in range(20):

            value = dropdown.input_value()

            if value:

                break

            self.page.wait_for_timeout(100)

        if not value:

            raise Exception(
                "Gram Panchayat selection failed."
            )

        # print("--------------------------------")
        # print("Selected GP :", label)
        # print("Selected Value :", value)
        # print("Selected Text :", dropdown.locator("option:checked").text_content())
        # print("--------------------------------")

        ##################################################
        # Wait for Village to load
        ##################################################

        village = self.page.locator(
            Selectors.INSURANCE_VILLAGE
        )

        self.wait.dropdown_loaded(
            village
        )

        self.reporter.log(

            account.account_no,

            "GRAM_PANCHAYAT",

            "SUCCESS",

            f"{label} selected."

        )

    def select_village(self, account):

        dropdown = self.page.locator(
            Selectors.INSURANCE_VILLAGE
        )

        self.wait.dropdown_loaded(
            dropdown
        )

        self.reporter.info(

            account.account_no,

            "VILLAGE",

            f"Selecting : {account.village}"

        )

        dropdown.select_option(
            label=account.village
        )

        value = ""

        for _ in range(20):

            value = dropdown.input_value()

            if value:

                break

            self.page.wait_for_timeout(100)

        if not value:

            raise Exception(
                "Village selection failed."
            )

        # print("--------------------------------")
        # print("Selected Village :", account.village)
        # print("Selected Value   :", value)
        # print("Selected Text    :", dropdown.locator("option:checked").text_content())
        # print("--------------------------------")

        self.reporter.log(

            account.account_no,

            "VILLAGE",

            "SUCCESS",

            f"{account.village} selected."

        )