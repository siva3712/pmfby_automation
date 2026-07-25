from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
import os
import sys


class Reporter:

    ########################################################

    def __init__(self, logger=None):

        self.logger = logger

        self.logs = []

        self.records = []

        self.success_count = 0
        self.failed_count = 0
        self.skipped_count = 0

        ##################################################
        # Application Folder
        ##################################################

        if getattr(sys, "frozen", False):

            self.base_path = Path(sys.executable).parent

        else:

            self.base_path = Path(__file__).resolve().parent

        ##################################################

        self.report_path = self.base_path / "reports"

        self.report_path.mkdir(exist_ok=True)

    ########################################################
    # Generic Logger
    ########################################################

    def log(
        self,
        account_no="",
        step="",
        status="INFO",
        message="",
        khata_no="",
        crop="",
        survey_no=""
    ):

        record = {

            "time": datetime.now(),

            "account": account_no,

            "khata": khata_no,

            "crop": crop,

            "survey": survey_no,

            "step": step,

            "status": status,

            "message": message

        }

        self.logs.append(record)

        line = (
            f"[{status}] "
            f"{account_no} | "
            f"{step} | "
            f"{message}"
        )

        print(line)

        if self.logger:

            self.logger(line)

    ########################################################
    # Convenience Methods
    ########################################################

    def info(
        self,
        account_no="",
        step="",
        message=""
    ):

        self.log(
            account_no,
            step,
            "INFO",
            message
        )

    ########################################################

    def warning(
        self,
        account_no="",
        step="",
        message=""
    ):

        self.log(
            account_no,
            step,
            "WARNING",
            message
        )

    ########################################################

    def error(
        self,
        account_no="",
        step="",
        message=""
    ):

        self.log(
            account_no,
            step,
            "ERROR",
            message
        )

    ########################################################
    # Final Account Status
    ########################################################

    def account_success(
        self,
        account_no,
        message="Policy Created Successfully."
    ):

        self.success_count += 1

        self.log(
            account_no,
            "ACCOUNT",
            "SUCCESS",
            message
        )

    ########################################################

    def account_failed(
        self,
        account_no,
        message
    ):

        self.failed_count += 1

        self.log(
            account_no,
            "ACCOUNT",
            "FAILED",
            message
        )

    ########################################################

    def account_skipped(
        self,
        account_no,
        message
    ):

        self.skipped_count += 1

        self.log(
            account_no,
            "ACCOUNT",
            "SKIPPED",
            message
        )

    ########################################################

    def export(self):

        workbook = Workbook()

        sheet = workbook.active

        sheet.title = "PMFBY Upload Report"

        sheet.append([

            "Time",

            "Account",

            "Stage",

            "Crop",

            "Khata",

            "Survey",

            "Farmer",

            "Father / Husband",

            "Individual Area (Ha)",

            "Total Area (Ha)",

            "Status",

            "Message"

        ])

        for record in self.records:

            sheet.append([

                record["time"].strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                record["account"],

                record["stage"],

                record["crop"],

                record["khata"],

                record["survey"],

                record["farmer"],

                record["father"],

                record["individual_area"],

                record["total_area"],

                record["status"],

                record["message"]

            ])

        filename = self.report_path / datetime.now().strftime(
            "PMFBY_Report_%Y%m%d_%H%M%S.xlsx"
        )

        workbook.save(filename)


        self.log(

                "",

                "REPORT",

                "INFO",

                f"Report saved to {filename}"

        )

        return filename

    ########################################################

    def summary(self):

        print()

        print("=" * 60)

        print("UPLOAD SUMMARY")

        print("=" * 60)

        print(f"Success : {self.success_count}")

        print(f"Failed  : {self.failed_count}")

        print(f"Skipped : {self.skipped_count}")

        print("=" * 60)

        return self.export()

    def record_result(
        self,
        account,
        stage,
        crop="",
        khata="",
        survey="",
        farmer="",
        father="",
        individual_area="",
        total_area="",
        status="",
        message=""
    ):

        self.records.append({

            "time": datetime.now(),

            "account": account,

            "stage": stage,

            "crop": crop,

            "khata": khata,

            "survey": survey,

            "farmer": farmer,

            "father": father,

            "individual_area": individual_area,

            "total_area": total_area,

            "status": status,

            "message": message

        })