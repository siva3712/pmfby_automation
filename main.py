# import getpass

# from browser_session import BrowserSession
# from pmfby_login import PMFBYLogin


# def main():

#     mobile = input("Mobile : ")

#     password = getpass.getpass("Password : ")

#     browser = BrowserSession(
#         headless=False
#     )

#     login = PMFBYLogin(
#         browser
#     )

#     page = login.login(
#         mobile,
#         password
#     )

#     print()

#     print("Browser session is reusable now.")

#     print(page.url)

#     input("Press ENTER to exit...")

#     browser.close()


# if __name__ == "__main__":

#     main()

from ui.main_window import MainWindow

if __name__ == "__main__":

    MainWindow().run()