from playwright.sync_api import TimeoutError

from pmfby_selectors import Selectors


class NotEligibleProcessor:

    ##########################################################

    def __init__(
        self,
        navigator,
        reporter,
        pdf_file
    ):

        self.navigator = navigator

        self.page = navigator.page

        self.wait = navigator.wait

        self.reporter = reporter

        self.pdf_file = pdf_file

    ##########################################################

    def process(self, account):

        account_no = account.account_no

        try:

            ##################################################
            # Search By
            ##################################################

            self.reporter.info(

                account_no,

                "SEARCH_ACCOUNT",

                "Selecting search by Account Number."

            )

            self.wait.select(

                self.page.locator(
                    Selectors.SEARCH_BY
                ),

                "2"

            )

            ##################################################
            # Account Number
            ##################################################

            self.reporter.info(

                account_no,

                "SEARCH_ACCOUNT",

                "Entering Account Number."

            )

            self.wait.fill(

                self.page.get_by_role(
                    "textbox",
                    name="Enter Account Number"
                ),

                account_no

            )

            ##################################################
            # Search
            ##################################################

            self.reporter.info(

                account_no,

                "SEARCH_ACCOUNT",

                "Searching..."

            )

            self.wait.click(

                self.page.get_by_title(
                    "Search"
                )

            )

            ##################################################
            # Wait for Not Eligible option
            ##################################################

            not_eligible = self.page.locator(

                'a[title="Not Eligible for PMFBY"]'

            )

            not_eligible.wait_for(

                state="visible",

                timeout=10000

            )

            self.reporter.log(

                account_no,

                "SEARCH_ACCOUNT",

                "SUCCESS",

                "Account found."

            )

            ##################################################
            # Check Not Eligible status
            ##################################################

            style = (

                not_eligible
                .get_attribute("style")
                or ""

            ).lower()

            ##################################################
            # Not Eligible disabled
            ##################################################

            if "cursor: not-allowed" in style:

                message = (

                    "Cannot mark account as Not Eligible. "

                    "Not Eligible option is disabled."

                )

                self.reporter.error(

                    account_no,

                    "NOT_ELIGIBLE",

                    message

                )

                self.reporter.record_result(

                    account=account_no,

                    stage="NOT_ELIGIBLE",

                    status="FAILURE",

                    message=message

                )

                return False

            ##################################################
            # Open Not Eligible modal
            ##################################################

            self.reporter.info(

                account_no,

                "NOT_ELIGIBLE",

                "Opening Not Eligible form."

            )

            self.wait.click(

                not_eligible

            )

            ##################################################
            # Modal
            ##################################################

            modal = self.page.locator(

                "div.privacyDetailsModal"

            )

            modal.wait_for(

                state="visible",

                timeout=10000

            )

            ##################################################
            # Reason
            ##################################################

            reason = modal.locator(

                'select[name="searchBy"]'

            )

            self.wait.select(

                reason,

                account.reason

            )

            self.reporter.info(

                account_no,

                "REASON",

                f"Selected : {account.reason}"

            )

            ##################################################
            # PDF
            ##################################################

            file_input = modal.locator(

                'input[type="file"]'

            )

            file_input.set_input_files(

                self.pdf_file

            )

            self.reporter.info(

                account_no,

                "DOCUMENT",

                "PDF uploaded."

            )

            ##################################################
            # Remarks
            ##################################################

            remarks = modal.locator(

                "textarea"

            )

            self.wait.fill(

                remarks,

                account.remarks

            )

            self.reporter.info(

                account_no,

                "REMARKS",

                "Remarks entered."

            )

            ##################################################
            # Submit
            ##################################################

            submit = modal.get_by_role(

                "button",

                name="Submit",

                exact=True

            )

            submit.wait_for(

                state="visible",

                timeout=5000

            )

            self.reporter.info(

                account_no,

                "NOT_ELIGIBLE",

                "Submitting."

            )

            self.wait.click(

                submit

            )

            ##################################################
            # Wait for modal to close
            ##################################################

            modal.wait_for(

                state="hidden",

                timeout=15000

            )

            ##################################################
            # Success
            ##################################################

            # self.reporter.account_success(

            #     account_no,

            #     "Account marked Not Eligible successfully."

            # )

            self.reporter.record_result(

                account=account_no,

                stage="NOT_ELIGIBLE",

                status="SUCCESS",

                message=(

                    "Marked Not Eligible successfully. "

                    f"Reason: {account.reason}"

                )

            )

            return True

        ######################################################
        # Timeout
        ######################################################

        except TimeoutError as ex:

            message = (

                f"Not Eligible processing timeout: {str(ex)}"

            )

            self.reporter.error(

                account_no,

                "NOT_ELIGIBLE",

                message

            )

            self.reporter.record_result(

                account=account_no,

                stage="NOT_ELIGIBLE",

                status="FAILURE",

                message=message

            )

            return False

        ######################################################
        # General exception
        ######################################################

        except Exception as ex:

            self.reporter.error(

                account_no,

                "NOT_ELIGIBLE",

                str(ex)

            )

            self.reporter.record_result(

                account=account_no,

                stage="NOT_ELIGIBLE",

                status="FAILURE",

                message=str(ex)

            )

            return False