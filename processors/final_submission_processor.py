from playwright.sync_api import TimeoutError

from pmfby_selectors import Selectors


class FinalSubmissionProcessor:

    ##########################################################

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
            # Final Submit
            ##################################################

            self.reporter.info(

                account_no,

                "FINAL_SUBMIT",

                "Submitting policy."

            )

            self.wait.click(

                self.page.locator(

                    Selectors.FINAL_SUBMIT

                )

            )

             ##################################################
            # Wait for Success Modal
            ##################################################

            modal = self.page.get_by_text(
                "Policy & Insured Area Details",
                exact=True
            )

            modal.wait_for(
                state="visible",
                timeout=10000
            )

            ##################################################
            # Capture Policy Number
            ##################################################

            policy = self.page.locator(
                "text=Policy ID"
            ).locator(
                "xpath=following-sibling::i"
            ).inner_text()

            self.reporter.info(

                account_no,

                "POLICY",

                f"Policy ID : {policy}"

            )

            ##################################################
            # Close
            ##################################################

            self.wait.click(

                self.page.get_by_role(

                    "button",

                    name="Close"

                )

            )

            self.reporter.account_success(

                account_no,

                "Policy created successfully."

            )

            self.reporter.record_result(
                account=account_no,
                stage="FINAL_SUBMIT",
                status="SUCCESS",
                message=f"Policy created successfully. ({policy})"  
            )


            ##################################################
            # Give React time to navigate
            ##################################################

            self.page.wait_for_timeout(1000)

            print("URL :", self.page.url)

            print("TITLE :", self.page.title())

            ##################################################
            # Return to KCC Beneficiary
            ##################################################

            if not self.navigator.return_to_kcc_beneficiary():

                raise Exception(
                    "Unable to return to KCC Beneficiary."
                )

      
            return True

        ######################################################

        except TimeoutError:

            self.reporter.error(

                account_no,

                "Final submission timeout."

            )

            self.reporter.record_result(
                
                account=account_no,

                stage="FINAL_SUBMIT",

                status="FAILURE",

                message="Final submission timeout."

            )

            return False

        ######################################################

        except Exception as ex:

            self.reporter.error(

                account_no,

                str(ex)

            )

            self.reporter.record_result(
                account=account_no,
                stage="FINAL_SUBMIT",
                status="FAILURE",
                message=str(ex)
            )

            return False