from playwright.sync_api import TimeoutError

from pmfby_selectors import Selectors


class LandDetailsProcessor:

    ##########################################################

    def __init__(self, navigator, reporter,progress_callback=None):

        self.navigator = navigator

        self.page = navigator.page

        self.wait = navigator.wait

        self.reporter = reporter

        self.progress_callback = progress_callback

    ##########################################################

    def process(
        self,
        account,
        khata,
        crop
    ):

        account_no = account.account_no

        ######################################################

        for survey in crop.survey_numbers:

             ##################################################
            # Update Current Survey
            ##################################################

            if self.progress_callback:

                self.progress_callback(

                    account=account.account_no,

                    khata=khata.khata_no,

                    survey=survey,

                    success=self.reporter.success_count,

                    failed=self.reporter.failed_count,

                    skipped=self.reporter.skipped_count

                )


            self.reporter.info(

                account_no,

                "SURVEY",

                f"Processing Survey : {survey}"

            )

            try:

                ##################################################
                # Fill Crop Details
                ##################################################

                self.fill_crop_details(
                    account,
                    khata,
                    crop,
                    survey
                )
                ##################################################
                # Verify Land
                ##################################################

                result = self.verify_land(

                    account_no,

                    survey

                )

                ##################################################
                # Failed
                ##################################################

                if not result["success"]:

                    self.reporter.error(

                        account.account_no,

                        "VERIFY",

                        result["message"]

                    )

                    self.reporter.record_result(

                        account=account.account_no,

                        stage="LAND",

                        crop=crop.crop_name,

                        khata=khata.khata_no,

                        survey=survey,

                        status="FAILED",

                        message=result["message"]

                    )

                    continue

                ##################################################
                # Success
                ##################################################

                land = result["land"]

                ##################################################
                # Log fetched details
                ##################################################

                self.reporter.info(

                    account.account_no,

                    "LAND",

                    f"Farmer : {land['farmer']}"

                )

                self.reporter.info(

                    account.account_no,

                    "LAND",

                    f"Father : {land['father']}"

                )

                self.reporter.info(

                    account.account_no,

                    "LAND",

                    f"Area : {land['individual_area']} Ha"

                )

                ##################################################
                # Submit
                ##################################################
                if not self.submit_land(

                    account.account_no,

                    survey

                ):

                    self.reporter.record_result(

                        account=account.account_no,

                        stage="LAND",

                        crop=crop.crop_name,

                        khata=khata.khata_no,

                        survey=survey,

                        farmer=land["farmer"],

                        father=land["father"],

                        individual_area=land["individual_area"],

                        total_area=land["total_area"],

                        status="FAILED",

                        message="Unable to submit fetched land."

                    )

                    continue
          
                ##################################################
                # Success record
                ##################################################

                self.reporter.record_result(

                    account=account.account_no,

                    stage="LAND",

                    crop=crop.crop_name,

                    khata=khata.khata_no,

                    survey=survey,

                    farmer=land["farmer"],

                    father=land["father"],

                    individual_area=land["individual_area"],

                    total_area=land["total_area"],

                    status="SUCCESS",

                    message="Survey added successfully."

                )
                

            except Exception as ex:

                self.reporter.error(

                    account_no,

                    "SURVEY",

                    f"{survey} : {str(ex)}"

                )
                self.reporter.record_result(

                    account=account.account_no,

                    stage="LAND",

                    crop=crop.crop_name,

                    khata=khata.khata_no,

                    survey=survey,

                    status="FAILED",

                    message=str(ex)

                )

                continue

    ##########################################################

    def fill_crop_details(

            self,

            account,

            khata,

            crop,

            survey

        ):

            ##################################################
            # Crop
            ##################################################

            crop_dropdown = self.page.locator(
                Selectors.CROP
            )

            self.wait.dropdown_loaded(
                crop_dropdown
            )

            crop_dropdown.select_option(
                label=crop.crop_name
            )

            ##################################################
            # Premium Date
            ##################################################
            premium = self.page.locator(Selectors.PREMIUM_DATE)
            
            # If standard date input, YYYY-MM-DD prevents month flipping
            date_str_iso = crop.premium_debit_date.strftime("%Y-%m-%d")
            premium.fill(date_str_iso)
            
            # Trigger JS state listeners on the form
            premium.dispatch_event("input")
            premium.dispatch_event("change")
            premium.press("Tab")

            ##################################################
            # Sowing Date
            ##################################################
            sowing = self.page.locator(Selectors.SOWING_DATE)
            
            sowing_str_iso = crop.sowing_date.strftime("%Y-%m-%d")
            sowing.fill(sowing_str_iso)
            
            # Trigger JS state listeners on the form
            sowing.dispatch_event("input")
            sowing.dispatch_event("change")
            sowing.press("Tab")

            ##################################################
            # IMPORTANT
            #
            # Excel Survey -> Khata textbox
            ##################################################

            khata_box = self.page.locator(
                Selectors.KHATA
            )

            khata_box.fill(
                survey
            )

            ##################################################
            # Excel Khata -> Khasra textbox
            ##################################################

            survey_box = self.page.locator(
                Selectors.SURVEY
            )

            survey_box.fill(
                khata.khata_no
            )

            self.reporter.log(

                account.account_no,

                "SURVEY",

                "SUCCESS",

                f"{survey} entered."

            ) 
    ##########################################################

    def verify_land(

        self,

        account_no,

        survey

    ):

        self.reporter.info(

            account_no,

            "VERIFY",

            survey

        )

        self.wait.click(

            self.page.locator(
                Selectors.VERIFY_LAND
            )

        )

        radio = self.page.locator(
            Selectors.LAND_RADIO
        )

        # modal = self.page.get_by_text(
        #     "Farmer's Land Details From Land Record"
        # )

        close = self.page.locator(
            "div.custom__modalHeader___3PkpK button.close"
        )

        ##################################################
        # Wait up to 10 seconds
        ##################################################

        for _ in range(50):

            if radio.count() > 0 and radio.is_visible():

                land = self.fetch_land_information()

                self.wait.check(radio)

                return {

                    "success": True,

                    "land": land

                }

            if close.count() > 0 and close.is_visible():

                self.close_land_modal()

                #self.clear_crop_row()

                return {

                    "success": False,

                    "message": f"{survey} not found in land records."

                }

            self.page.wait_for_timeout(200)

        ##################################################
        # Nothing happened
        ##################################################

        return {

            "success": False,

            "message": "Verification timeout."

        }
    ##########################################################

    def submit_land(

        self,

        account_no,

        survey

    ):

        ##################################################
        # Submit
        ##################################################

        self.wait.click(

            self.page.locator(
                Selectors.LAND_SUBMIT
            )

        )

        ##################################################
        # Wait for Add Crop button
        ##################################################

        add_crop = self.page.locator(
            Selectors.ADD_CROP
        )

        self.wait.visible(
            add_crop
        )

        ##################################################
        # Click Add Crop
        ##################################################

        self.wait.click(
            add_crop
        )

        ##################################################
        # Verify crop added to summary
        ##################################################

        row = self.page.locator(

            f"table.tableData__customTable___1tQJH tbody tr:has(td:text('{survey}'))"

        )

        try:

            row.wait_for(
                timeout=2000
            )

        except TimeoutError:

            self.reporter.error(

                account_no,

                "LAND",

                f"{survey} was not added."

            )

            return False

        ##################################################
        # Wait until entry row becomes blank
        ##################################################

        crop = self.page.locator(
            Selectors.CROP
        )

        for _ in range(20):

            if crop.input_value() == "":

                break

            self.page.wait_for_timeout(100)

        self.reporter.log(

            account_no,

            "LAND",

            "SUCCESS",

            f"{survey} added successfully."

        )

        return True

    ###########################################################
    # Fetch land information to log the details in reporter
    ###########################################################
    def fetch_land_information(self):

        row = self.page.locator(
            "input[name='utrList']"
        ).locator(
            "xpath=ancestor::tr"
        )

        cells = row.locator("td")

        return {

            "survey": cells.nth(2).inner_text().strip(),

            "khata": cells.nth(3).inner_text().strip(),

            "khata_desc": cells.nth(4).inner_text().strip(),

            "individual_area": cells.nth(5).inner_text().strip(),

            "farmer": cells.nth(6).inner_text().strip(),

            "father": cells.nth(7).inner_text().strip(),

            "total_area": cells.nth(8).inner_text().strip()

        }
    ###########################################################
    #If survey is not found in land records, then close the modal and clear the crop row
    ###########################################################
    def close_land_modal(self):

        modal = self.page.get_by_text(

            "Farmer's Land Details From Land Record"

        )

        self.wait.visible(modal)

        self.page.locator(

            "div.custom__modalHeader___3PkpK button.close"

        ).click()

        modal.wait_for(
            state="hidden"
        )
        ############################################################
        # Clear the crop row after closing the land modal
        ############################################################
        #self.clear_crop_row()
    ############################################################
    # Clear the crop row after closing the land modal
    ############################################################
    def clear_crop_row(self):

        self.page.locator(
            Selectors.CROP
        ).select_option("")

        self.page.locator(
            Selectors.PREMIUM_DATE
        ).fill("")

        self.page.locator(
            Selectors.SOWING_DATE
        ).fill("")

        self.page.locator(
            Selectors.KHATA
        ).fill("")

        self.page.locator(
            Selectors.SURVEY
        ).fill("")