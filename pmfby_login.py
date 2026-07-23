from playwright.sync_api import TimeoutError


class PMFBYLogin:

    def __init__(self, browser):

        self.browser = browser
        self.page = browser.get_page()

    def login(self, mobile, password):

        self.page.goto(
            "https://pmfby.gov.in/",
            wait_until="domcontentloaded"
        )

        self.page.get_by_role(
            "button",
            name="Sign In"
        ).click()

        self.page.locator(
            'input[name="username"]'
        ).fill(mobile)

        self.page.locator(
            'input[name="password"]'
        ).fill(password)

        print()
        print("=" * 70)
        print("Complete CAPTCHA")
        print("Click LOGIN")
        print("Enter OTP")
        print("Click VERIFY & PROCEED")
        print("=" * 70)

        try:

            self.page.get_by_role(
                "button",
                name="Submit"
            ).wait_for(
                timeout=300000
            )

        except TimeoutError:

            raise Exception("Login Timeout")

        print("Login Successful")

        return self.page