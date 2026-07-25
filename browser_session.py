import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


class BrowserSession:

    def __init__(self, headless=False):

        ##################################################
        # Running from EXE
        ##################################################

        if getattr(sys, "frozen", False):

            browser_path = (
                Path(sys.executable).parent
                / "_internal"
                / "browsers"
            )

            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(browser_path)

        ##################################################

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(

            headless=headless,

            args=["--start-maximized"]

        )

        self.context = self.browser.new_context(

            viewport=None

        )

        self.page = self.context.new_page()

    ##################################################

    def get_page(self):

        return self.page

    ##################################################

    def close(self):

        self.context.close()

        self.browser.close()

        self.playwright.stop()