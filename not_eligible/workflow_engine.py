from processors.not_eligible_processor import (
    NotEligibleProcessor
)


class NotEligibleWorkflowEngine:

    def __init__(
        self,
        navigator,
        reporter,
        worker,
        pdf_file,
        progress_callback=None
    ):

        self.navigator = navigator

        self.reporter = reporter

        self.worker = worker

        self.pdf_file = pdf_file

        self.progress_callback = progress_callback

        self.processor = NotEligibleProcessor(
            navigator=navigator,
            reporter=reporter,
            pdf_file=pdf_file
        )

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
        # Ensure KCC page
        ##################################################

        self.navigator.ensure_kcc_beneficiary_page()

        ##################################################
        # Accounts
        ##################################################

        for index, account in enumerate(
            accounts,
            start=1
        ):

            if self.worker.is_cancelled():

                self.reporter.warning(
                    account.account_no,
                    "UPLOAD",
                    "Processing cancelled by user."
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

            if success:

                self.reporter.account_success(

                    account.account_no,

                    "Account marked Not Eligible successfully."

                )

            else:

                self.reporter.account_failed(

                    account.account_no,

                    "Unable to mark account as Not Eligible."

                )

        ##################################################
        # Final progress
        ##################################################

        if self.progress_callback:

            self.progress_callback(

                current=total,

                total=total,

                success=self.reporter.success_count,

                failed=self.reporter.failed_count,

                skipped=self.reporter.skipped_count

            )