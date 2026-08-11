class NotEligibleAccount:

    def __init__(
        self,
        account_no,
        reason,
        remarks
    ):

        self.account_no = str(account_no).strip()

        self.reason = str(reason).strip()

        self.remarks = str(remarks).strip()