from processors.change_account_processor import ChangeAccountProcessor
class ChangeAccountWorkflowEngine:

    def __init__(
        self,
        navigator,
        reporter,
        worker,
        progress_callback=None
    ):

        self.navigator = navigator

        self.reporter = reporter

        self.worker = worker

        self.progress_callback = progress_callback

        self.processor = ChangeAccountProcessor(

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

        ##################################################
        # Ensure KCC Beneficiary
        ##################################################

        self.navigator.ensure_kcc_beneficiary_page()

        ##################################################
        # Process accounts
        ##################################################

        for index, account in enumerate(
            accounts,
            start=1
        ):

            ##################################################
            # Cancellation
            ##################################################

            if self.worker.is_cancelled():

                self.reporter.warning(

                    account.account_no,

                    "UPLOAD",

                    "Upload cancelled by user."

                )

                return

            ##################################################
            # Progress
            ##################################################

            if self.progress_callback:

                self.progress_callback(

                    current=index,

                    total=total,

                    account=account.account_no,

                    khata="",

                    survey="",

                    success=self.reporter.success_count,

                    failed=self.reporter.failed_count,

                    skipped=self.reporter.skipped_count

                )

            ##################################################
            # Account
            ##################################################

            self.reporter.info(

                account.account_no,

                "ACCOUNT",

                f"Processing Account {index} of {total}"

            )

            ##################################################
            # Process
            ##################################################

            success = self.processor.process(

                account

            )

            ##################################################
            # Account-level counter
            ##################################################

            if success:

                self.reporter.account_success(

                    account.account_no,

                    "Account number changed successfully."

                )

            else:

                self.reporter.account_failed(

                    account.account_no,

                    "Account number change failed."

                )

            ##################################################
            # Return to KCC Beneficiary
            ##################################################

            if not self.navigator.return_to_kcc_beneficiary():

                self.reporter.error(

                    account.account_no,

                    "RECOVERY",

                    "Unable to return to KCC Beneficiary."

                )

                return

            ##################################################
            # Final progress update
            ##################################################

            if self.progress_callback:

                self.progress_callback(

                    current=index,

                    total=total,

                    account=account.account_no,

                    khata="",

                    survey="",

                    success=self.reporter.success_count,

                    failed=self.reporter.failed_count,

                    skipped=self.reporter.skipped_count

                )