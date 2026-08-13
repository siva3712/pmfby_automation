from playwright.sync_api import TimeoutError


class ChangeAccountProcessor:

    ##########################################################

    def __init__(
        self,
        navigator,
        reporter
    ):

        self.navigator = navigator

        self.page = navigator.page

        self.wait = navigator.wait

        self.reporter = reporter

    ##########################################################

    def process(self, account):

        account_no = account.account_no

        new_account_no = account.new_account_no

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
                    'select[name="searchBy"]'
                ),

                "2"

            )

            ##################################################
            # Old Account Number
            ##################################################

            self.reporter.info(

                account_no,

                "SEARCH_ACCOUNT",

                "Entering old Account Number."

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

            # self.reporter.info(

            #     account_no,

            #     "SEARCH_ACCOUNT",

            #     "Searching..."

            # )

            # self.wait.click(

            #     self.page.get_by_title(
            #         "Search"
            #     )

            # )

            ##################################################
            # Wait for Change A/c
            ##################################################

            change_account = self.page.locator(

                'a[title="Change A/c"]'

            )

            change_account.wait_for(

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
            # Check disabled state
            ##################################################

            style = (

                change_account
                .get_attribute("style")
                or ""

            ).lower()

            if "cursor: not-allowed" in style:

                message = (

                    "Cannot change account number. "

                    "Change A/c option is disabled."

                )

                self.reporter.error(

                    account_no,

                    "CHANGE_ACCOUNT",

                    message

                )

                self.reporter.record_result(

                    account=account_no,

                    stage="CHANGE_ACCOUNT",

                    status="FAILURE",

                    message=message

                )

                return False

            ##################################################
            # Open Change Account modal
            ##################################################

            self.reporter.info(

                account_no,

                "CHANGE_ACCOUNT",

                "Opening Change A/c form."

            )

            self.wait.click(

                change_account

            )

            ##################################################
            # Modal
            ##################################################

            modal = self.page.locator(

                "div.modal-content"

            ).filter(

                has_text="Change KCC Account Number"

            )

            modal.wait_for(

                state="visible",

                timeout=10000

            )

            ##################################################
            # New Account Number
            ##################################################

            new_account = modal.locator(

                'input[placeholder="New Account Number"]'

            )

            confirm_account = modal.locator(

                'input[placeholder="Confirm New Account Number"]'

            )

            self.wait.fill(

                new_account,

                new_account_no

            )

            self.reporter.info(

                account_no,

                "CHANGE_ACCOUNT",

                "New Account Number entered."

            )

            ##################################################
            # Confirm New Account Number
            ##################################################

            self.wait.fill(

                confirm_account,

                new_account_no

            )

            self.reporter.info(

                account_no,

                "CHANGE_ACCOUNT",

                "New Account Number confirmed."

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

                "CHANGE_ACCOUNT",

                "Submitting account number change."

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

            self.reporter.record_result(

                account=account_no,

                stage="CHANGE_ACCOUNT",

                status="SUCCESS",

                message=(

                    "Account number changed successfully. "

                    f"Old Account: {account_no}, "

                    f"New Account: {new_account_no}"

                )

            )

            return True

        ######################################################
        # Timeout
        ######################################################

        except TimeoutError as ex:

            message = (

                f"Change Account processing timeout: {str(ex)}"

            )

            self.reporter.error(

                account_no,

                "CHANGE_ACCOUNT",

                message

            )

            self.reporter.record_result(

                account=account_no,

                stage="CHANGE_ACCOUNT",

                status="FAILURE",

                message=message

            )

            return False

        ######################################################
        # Exception
        ######################################################

        except Exception as ex:

            self.reporter.error(

                account_no,

                "CHANGE_ACCOUNT",

                str(ex)

            )

            self.reporter.record_result(

                account=account_no,

                stage="CHANGE_ACCOUNT",

                status="FAILURE",

                message=str(ex)

            )

            return False