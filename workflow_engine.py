from processors.account_search_processor import AccountSearchProcessor
from processors.aadhaar_verification_processor import AadhaarVerificationProcessor
from processors.location_processor import LocationProcessor
from processors.land_details_processor import LandDetailsProcessor
from processors.preview_processor import PreviewProcessor
from processors.final_submission_processor import FinalSubmissionProcessor


class WorkflowEngine:

    ##########################################################

    def __init__(
        self,
        navigator,
        actions,
        reporter,
        worker,
        progress_callback=None
    ):

        self.navigator = navigator

        self.actions = actions

        self.reporter = reporter

        self.worker = worker

        self.progress_callback = progress_callback

        ######################################################
        # Processors
        ######################################################

        self.search = AccountSearchProcessor(
            navigator,
            reporter
        )

        self.aadhaar = AadhaarVerificationProcessor(
            navigator,
            reporter
        )

        self.location = LocationProcessor(

            navigator,

            reporter

        )

        self.land = LandDetailsProcessor(
            navigator,
            reporter,
            progress_callback=progress_callback
        )

        self.preview = PreviewProcessor(
            navigator,
            reporter
        )

        self.final_submit = FinalSubmissionProcessor(
            navigator,
            reporter
        )

    ##########################################################

    def process(self, accounts):

        total = len(accounts)

        self.reporter.info(
            "",
            "UPLOAD",
            "=" * 70
        )

        self.reporter.info(
            "",
            "UPLOAD",
            f"Loaded {total} Account(s)"
        )

        self.reporter.info(
            "",
            "UPLOAD",
            "=" * 70
        )

        ######################################################
        # Ensure user is on KCC Beneficiary page
        ######################################################

        self.navigator.ensure_kcc_beneficiary_page()

        ######################################################

        for index, account in enumerate(accounts, start=1):

            if self.worker.is_cancelled():

                self.reporter.warning(

                    account.account_no,

                    "UPLOAD",

                    "Upload cancelled by user."

                )

                return
             ##################################################
            # Update Progress
            ##################################################

            if self.progress_callback:

                self.progress_callback(

                    current=index,

                    total=len(accounts),

                    account=account.account_no,

                    khata="",

                    survey="",

                    success=self.reporter.success_count,

                    failed=self.reporter.failed_count,

                    skipped=self.reporter.skipped_count

                )


            self.reporter.info(

                account.account_no,

                "ACCOUNT",

                f"Processing Account {index} of {total}"

            )
            ##################################################
            # Process Account
            ##################################################

            self.process_account(account)

              ##################################################
            # Refresh statistics after processing account
            ##################################################

            if self.progress_callback:

                self.progress_callback(

                    current=index,

                    total=total,

                    account=account.account_no,

                    success=self.reporter.success_count,

                    failed=self.reporter.failed_count,

                    skipped=self.reporter.skipped_count

                )

    ##########################################################

    def process_account(self, account):

        ######################################################
        # Account Information
        ######################################################

        self.reporter.info(

            account.account_no,

            "ACCOUNT",

            f"District : {account.district}"

        )

        self.reporter.info(

            account.account_no,

            "ACCOUNT",

            f"Mandal : {account.mandal}"

        )

        self.reporter.info(

            account.account_no,

            "ACCOUNT",

            f"Village : {account.village}"

        )

        ######################################################
        # Milestone 1
        # Search Account + Open Policy
        ######################################################

        if not self.search.process(account):
            self.reporter.account_failed(

                account.account_no,

                "Account not found / Pending application not found."

            )

            return

        ######################################################
        # Milestone 2
        # Aadhaar Verification
        ######################################################

        if not self.aadhaar.process(account):
            self.reporter.account_failed(

                account.account_no,

                "Aadhaar / Save & Continue failed."

            )

            recovered = self.recover_to_kcc(

                account.account_no,

                "Aadhaar Verification Failed"

            )

            if not recovered:

                self.reporter.error(

                    account.account_no,

                    "RECOVERY",

                    "Unable to recover to KCC page."

                )

            return

        ######################################################
        # Milestone 3
        # Location Processor
        ######################################################

        ##################################################
        # Milestone 3
        ##################################################

        if not self.location.process(account):

            self.reporter.account_failed(

                account.account_no,

                "Location selection failed."

            )

            self.recover_to_kcc(

                account.account_no,

                "Location Selection Failed"

            )

            return


        ######################################################
        # Milestone 4
        # Land Details
        ######################################################

        for khata in account.khatas:

            if self.worker.is_cancelled():

                return
             ##################################################
             # Update Current Khata
             ##################################################

            if self.progress_callback:

                self.progress_callback(

                    account=account.account_no,

                    khata=khata.khata_no,

                    survey="",

                    success=self.reporter.success_count,

                    failed=self.reporter.failed_count,

                    skipped=self.reporter.skipped_count

                )

            ##################################################

            for crop in khata.crops:

                if self.worker.is_cancelled():

                    return

                self.reporter.info(

                    account.account_no,

                    "CROP",

                    f"Crop : {crop.crop_name}"

                )

                self.land.process(

                    account,

                    khata,

                    crop

                )

                  

        ######################################################
        # Milestone 5
        # Preview
        ######################################################

        if not self.preview.process(account):

            self.reporter.account_failed(

                account.account_no,

                "Preview failed."

            )

            self.recover_to_kcc(

                account.account_no,

                "Preview Failed"

            )

            return

        ######################################################
        # Milestone 6
        # Final Submit
        ######################################################
        if not self.final_submit.process(account):

            self.reporter.account_failed(

                account.account_no,

                "Final Submission failed."

            )

            self.recover_to_kcc(

                account.account_no,

                "Final Submission Failed"

            )

            return  
        # TODO

        ######################################################

      

    def recover_to_kcc(
        self,
        account_no,
        reason
    ):

        self.reporter.warning(

            account_no,

            "RECOVERY",

            reason

        )

        try:

            ok = self.navigator.return_to_kcc_beneficiary()

            if ok:

                self.reporter.info(

                    account_no,

                    "RECOVERY",

                    "Returned to KCC Beneficiary."

                )

            else:

                self.reporter.warning(

                    account_no,

                    "RECOVERY",

                    "Recovery returned False."

                )

            return ok

        except Exception as ex:

            self.reporter.error(

                account_no,

                "RECOVERY",

                str(ex)

            )

            return False