from playwright.sync_api import TimeoutError


class AadhaarVerificationProcessor:

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
            # Aadhaar State
            ##################################################

            state = self.get_aadhaar_state()

            ##################################################
            # Already Verified
            ##################################################

            if state == "VERIFIED":

                self.reporter.info(

                    account_no,

                    "AADHAAR",

                    "Already verified."

                )

            ##################################################
            # Needs Verification
            ##################################################

            elif state == "VERIFY":

                verify_button = self.page.locator(
                    "a.custom__textVerifyGroup___3Uyaq"
                )

                self.reporter.info(

                    account_no,

                    "AADHAAR",

                    "Clicking Verify."

                )

                self.wait.click(
                    verify_button
                )

                ##################################################
                # Wait until Green Tick appears
                ##################################################

                verified = self.page.locator(
                    "a.custom__textValidGroup___3HCPC"
                )

                self.wait.visible(
                    verified
                )

                self.reporter.log(

                    account_no,

                    "AADHAAR",

                    "SUCCESS",

                    "Aadhaar verified."

                )

            ##################################################
            # Unknown State
            ##################################################

            else:

                self.reporter.error(

                    account_no,

                    "AADHAAR",

                    "Unknown Aadhaar verification state."

                )

                self.reporter.record_result(

                    account=account_no,

                    stage="AADHAAR",

                    status="ERROR",

                    message="Unknown Aadhaar verification state."

                )

                return False

            ##################################################
            # Nominee Checkbox
            ##################################################

            checkbox = self.page.get_by_role(
                "checkbox"
            )

            if checkbox.is_checked():

                self.reporter.info(

                    account_no,

                    "NOMINEE",

                    "Already checked."

                )

            else:

                self.wait.check(checkbox)

                self.reporter.info(

                    account_no,

                    "NOMINEE",

                    "Checked."

                )

            ##################################################
            # Save & Continue
            ##################################################

            self.reporter.info(

                account_no,

                "SAVE_CONTINUE",

                "Submitting."

            )

            self.wait.click(

                self.page.get_by_role(
                    "button",
                    name="Save & Continue"
                )

            )
            

            ##################################################
            # Wait for Success OR Validation Error
            ##################################################

            district = self.page.locator(
                'select[name="INSURANCE District"]'
            )

            alert = self.page.locator(
                'div.alert.alert-danger.alert-dismissable'
            )

            result = self.wait.wait_for_any({

                "SUCCESS": district,

                "ERROR": alert

            })

            ##################################################
            # Success
            ##################################################

            if result == "SUCCESS":

                self.reporter.log(

                    account_no,

                    "SAVE_CONTINUE",

                    "SUCCESS",

                    "Crop Details page opened."

                )

                return True

            ##################################################
            # Validation Failed
            ##################################################

            message = alert.locator("p").inner_text().strip()

            self.reporter.error(

                account_no,

                "VALIDATION",

                message

            )

            self.reporter.record_result(

                account=account_no,

                stage="AADHAAR",

                status="ERROR",

                message=message

            )

            return False

        ##################################################
        # Validation Failed
        ##################################################

        except TimeoutError:

            self.reporter.error(

                account_no,

                "AADHAAR",

                "Timed out while verifying Aadhaar or waiting for next page."

            )

            self.reporter.record_result(

                account=account_no,

                stage="AADHAAR",

                status="ERROR",

                message="Timed out while verifying Aadhaar or waiting for next page."

            )

            return False



        ##########################################################

    def get_aadhaar_state(self):

        verify = self.page.locator(
            'a[title="Verify"]'
        )

        verified = self.page.locator(
            'a[title="Check"]'
        )

        result = self.wait.wait_for_any({

            "VERIFY": verify,

            "VERIFIED": verified

        })

        return result or "UNKNOWN"