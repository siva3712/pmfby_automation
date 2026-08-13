from playwright.sync_api import TimeoutError
from pmfby_selectors import Selectors

class AccountSearchProcessor:

    def __init__(self, navigator, reporter):

        self.navigator = navigator

        self.page = navigator.page

        self.wait = navigator.wait

        self.reporter = reporter

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
            # Wait for Search Result
            ##################################################

            create_policy = self.page.get_by_role(
                "link",
                name="Create Policy"
            )

            # self.wait.visible(
            #     create_policy
            # )
            create_policy.wait_for(
                timeout=10000
            )

            self.reporter.log(

                account_no,

                "SEARCH_ACCOUNT",

                "SUCCESS",

                "Pending application found."

            )

         ##################################################
        # Open Policy
        ##################################################
            self.wait.click(
                create_policy
            )
          
            self.reporter.log(

                account_no,

                "CREATE_POLICY",

                "SUCCESS",

                "Policy page opened."

            )

            return True

        except TimeoutError:

            self.reporter.error(

                account_no,

                "SEARCH_ACCOUNT",

                "Pending application not found."

            )

            self.reporter.record_result(

                account=account_no,

                stage="SEARCH_ACCOUNT",

                status="ERROR",

                message="Pending application not found."

            )

            return False

        except Exception as ex:

            self.reporter.error(

                account_no,

                "SEARCH_ACCOUNT",

                str(ex)

            )
            self.reporter.record_result(

                account=account_no,

                stage="SEARCH_ACCOUNT",

                status="ERROR",

                message=str(ex)

            )

            return False