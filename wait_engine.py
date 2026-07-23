from playwright.sync_api import expect, TimeoutError
import time


class WaitEngine:

    DEFAULT_TIMEOUT = 5000
    SHORT_TIMEOUT = 5000
    LONG_TIMEOUT = 60000

    def __init__(self, page):

        self.page = page

    ###################################################

    def visible(self, locator, timeout=None):

        locator.wait_for(
            state="visible",
            timeout=timeout or self.DEFAULT_TIMEOUT
        )

    ###################################################

    def hidden(self, locator, timeout=None):

        locator.wait_for(
            state="hidden",
            timeout=timeout or self.DEFAULT_TIMEOUT
        )

    ###################################################

    def enabled(self, locator, timeout=None):

        expect(locator).to_be_enabled(
            timeout=timeout or self.DEFAULT_TIMEOUT
        )

    ###################################################

    def click(self, locator):

        self.visible(locator)

        self.enabled(locator)

        locator.click()

    ###################################################

    def fill(self, locator, value):

        self.visible(locator)

        locator.fill("" if value is None else str(value))

    ###################################################

    def select(self, locator, value):

        self.visible(locator)

        self.enabled(locator)

        locator.select_option(value)

    ###################################################

    def check(self, locator):

        self.visible(locator)

        if not locator.is_checked():

            locator.check()

    ###################################################

    def dropdown_loaded(self, locator):

        self.visible(locator)

        self.enabled(locator)

        for _ in range(100):

            try:

                if locator.locator("option").count() > 1:
                    return

            except Exception:
                pass

            self.page.wait_for_timeout(100)

        raise Exception("Dropdown not populated.")

    ###################################################

    def ajax_complete(self):

        self.page.wait_for_load_state(
            "networkidle"
        )

    ###################################################

    def page_loaded(self, locator):

        self.visible(locator)

        self.ajax_complete()

    ###################################################

    def url_contains(self, text):

        self.page.wait_for_url(
            f"**{text}**"
        )

    ###################################################

    def text_visible(self, text):

        self.page.get_by_text(
            text
        ).wait_for()

    ###################################################

    def exists(self, locator):

        try:

            locator.wait_for(
                state="attached",
                timeout=self.SHORT_TIMEOUT
            )
            return True

        except TimeoutError:

            return False

    ###################################################

    def spinner_disappeared(self):

        try:

            self.page.locator(
                ".spinner"
            ).wait_for(
                state="hidden",
                timeout=self.SHORT_TIMEOUT
            )

        except Exception:

            pass
    ###################################################

    def verification_completed(self):

        self.page.get_by_text(
            "Verify",
            exact=True
        ).wait_for(
            state="hidden"
        )

    ###################################################

    def wait_for_any(
        self,
        locators,
        timeout=None
    ):

        timeout = timeout or self.DEFAULT_TIMEOUT

        end = time.time() + timeout / 1000

        while time.time() < end:

            for key, locator in locators.items():

                try:

                    if locator.is_visible():

                        return key

                except Exception:

                    pass

            self.page.wait_for_timeout(200)

        return None

    def dropdown_loaded(self, locator):

        self.visible(locator)

        for _ in range(300):      # ~30 seconds

            try:

                options = locator.locator("option")

                if options.count() > 1:

                    first = options.nth(1).text_content()

                    if first and first.strip():

                        return

            except Exception:

                pass

            self.page.wait_for_timeout(100)

        raise Exception(
            "Dropdown not populated."
        )