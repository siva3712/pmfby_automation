class ChangeAccount:

    def __init__(
        self,
        account_no,
        new_account_no
    ):

        self.account_no = str(
            account_no
        ).strip()

        self.new_account_no = str(
            new_account_no
        ).strip()