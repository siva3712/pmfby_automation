from excel_reader import ExcelReader

reader = ExcelReader()

accounts = reader.read("sample-data.xlsx")

for account in accounts:

    print(account.account_no)

    for khata in account.khatas:

        print("  ", khata.khata_no)

        for crop in khata.crops:

            print("      ", crop.crop_name)

            print("      ", crop.survey_numbers)