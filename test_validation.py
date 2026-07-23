from excel_validator import ExcelValidator

validator = ExcelValidator()

result = validator.validate(
    "sample-data.xlsx"
)

if result.success:

    print("Validation Successful")

else:

    print()

    print("Validation Failed")

    print()

    for error in result.errors:

        print(
            f"Row {error.row} | "
            f"{error.column} | "
            f"{error.message}"
        )