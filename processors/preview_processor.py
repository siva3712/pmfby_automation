from playwright.sync_api import TimeoutError

from pmfby_selectors import Selectors


class PreviewProcessor:

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
            # Open Preview
            ##################################################

            self.reporter.info(

                account_no,

                "PREVIEW",

                "Opening preview."

            )

            self.wait.click(

                self.page.locator(

                    Selectors.PREVIEW

                )

            )

            ##################################################
            # Wait for Consent Checkbox
            ##################################################

            consent = self.page.locator(

                Selectors.CONSENT

            )

            self.wait.visible(
                consent
            )

            ##################################################
            # Tick Consent
            ##################################################

            if consent.is_checked():

                self.reporter.info(

                    account_no,

                    "CONSENT",

                    "Already checked."

                )

            else:

                self.wait.check(
                    consent
                )

                self.reporter.info(

                    account_no,

                    "CONSENT",

                    "Consent checked."

                )

            ##################################################
            # Stop here
            ##################################################

            self.reporter.info(

                account_no,

                "PREVIEW",

                "Preview step is completed. Ready for final submission."

            )

            return True

        except TimeoutError:

            self.reporter.error(

                account_no,

                "PREVIEW",

                "Unable to open Preview."

            )

            self.reporter.record_result(

                account=account_no,

                stage="PREVIEW",

                status="FAILURE",

                message="Unable to open Preview."

            )

            return False

        except Exception as ex:

            self.reporter.error(

                account_no,

                "PREVIEW",

                str(ex)

            )

            self.reporter.record_result(
                
                account=account_no,

                stage="PREVIEW",

                status="FAILURE",

                message=str(ex)

            )

            return False