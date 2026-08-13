import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

import os
import shutil
import sys
from pathlib import Path
from PIL import Image, ImageTk

from excel_validator import ExcelValidator
from browser_session import BrowserSession
from pmfby_login import PMFBYLogin
from pmfby_navigator import PMFBYNavigator
from pmfby_actions import PMFBYActions
from excel_reader import ExcelReader
from reporter import Reporter
from workflow_engine import WorkflowEngine

from workers.background_worker import BackgroundWorker
from datetime import datetime 
from not_eligible.validator import (
    NotEligibleExcelValidator
)
from not_eligible.excel_reader import (
    NotEligibleExcelReader
)

from not_eligible.workflow_engine import (
    NotEligibleWorkflowEngine
)

from change_account.excel_validator import (
    ChangeAccountExcelValidator
)

from change_account.excel_reader import (
    ChangeAccountExcelReader
)

from change_account.workflow_engine import (
    ChangeAccountWorkflowEngine
)


class MainWindow:

    def __init__(self):

        ##################################################
        # Window
        ##################################################

        self.root = tk.Tk()
        self.root.title("PMFBY Bulk Uploader")

        # Dynamic resizing with standard laptop dimensions
        self.root.geometry("1100x720")
        self.root.minsize(950, 600)
        self.root.configure(bg="#F3F4F6")

        ##################################################
        # Theme
        ##################################################

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        ##################################################
        # Variables
        ##################################################

        self.excel_file = tk.StringVar()
        self.mobile = tk.StringVar()
        self.password = tk.StringVar()

        self.pdf_file = tk.StringVar()

        self.operation = tk.StringVar(
            value="Create Crop Insurance Policy"
        )

        ##################################################
        # Runtime Objects
        ##################################################

        self.browser = None
        self.page = None
        self.navigator = None
        self.actions = None
        self.logged_in = False

        self.worker = BackgroundWorker()

        ##################################################
        # Build UI
        ##################################################

        self.create_header()
        self.create_footer()
        self.create_body()

        ##################################################
        # set initial state
        ##################################################

        self.set_ui_state("READY")
        self.upload_running = False

    def get_resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller .exe """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def configure_styles(self):

        # Global Colors
        header_red = "#8B0000"
        bg_color = "#F3F4F6"
        card_bg = "#FFFFFF"

        # General Style Configuration
        self.style.configure(".", background=bg_color, font=("Segoe UI", 9))

        # Header Styles
        self.style.configure("Header.TLabel", background=header_red, foreground="white", font=("Segoe UI", 16, "bold"))
        self.style.configure("SubHeader.TLabel", background=header_red, foreground="#FFD1D1", font=("Segoe UI", 9))
        self.style.configure("Status.TLabel", background=header_red, foreground="#00FF66", font=("Segoe UI", 10, "bold"))

        # Card / Frame Styles
        self.style.configure("Card.TLabelframe", background=card_bg, borderwidth=1, relief="solid")
        self.style.configure("Card.TLabelframe.Label", font=("Segoe UI", 10, "bold"), foreground=header_red, background=bg_color)

        # Typography
        self.style.configure("Title.TLabel", font=("Segoe UI", 9, "bold"), background=card_bg, foreground="#374151")
        self.style.configure("Value.TLabel", font=("Segoe UI", 9), background=card_bg, foreground="#111827")
        self.style.configure("Warning.TLabel", font=("Segoe UI", 9), background=card_bg, foreground="#DC2626")

        # Stat Labels
        self.style.configure("Success.TLabel", font=("Segoe UI", 10, "bold"), background=card_bg, foreground="#16A34A")
        self.style.configure("Failed.TLabel", font=("Segoe UI", 10, "bold"), background=card_bg, foreground="#DC2626")
        self.style.configure("Skipped.TLabel", font=("Segoe UI", 10, "bold"), background=card_bg, foreground="#D97706")

        # Buttons
        self.style.configure("TButton", font=("Segoe UI", 9), padding=(10, 4))
        self.style.configure("Primary.TButton", font=("Segoe UI", 9, "bold"))

    def create_header(self):

        header_bg = "#8B0000"
        frame = tk.Frame(self.root, bg=header_bg, height=70)
        frame.pack(fill="x", side="top")
        frame.pack_propagate(False)

        left = tk.Frame(frame, bg=header_bg)
        left.pack(side="left", fill="y", padx=15)

        # Load Union Logo safely for both Dev & Compiled PyInstaller Executable
        logo_path = self.get_resource_path("airrbea_logo.jpg")
        if not os.path.exists(logo_path):
            logo_path = self.get_resource_path("airrbea_logo.png")

        if os.path.exists(logo_path):
            try:
                pil_image = Image.open(logo_path)
                pil_image = pil_image.resize((50, 50), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(pil_image)

                logo_label = tk.Label(left, image=self.logo_img, bg=header_bg)
                logo_label.pack(side="left", padx=(0, 10), pady=10)
            except Exception as e:
                print(f"Could not load logo image: {e}")

        # Text container beside logo
        title_box = tk.Frame(left, bg=header_bg)
        title_box.pack(side="left", fill="y", pady=10)

        ttk.Label(title_box, text="PMFBY BULK UPLOADER", style="Header.TLabel").pack(anchor="w")
        ttk.Label(title_box, text="Andhra Pradesh Grameena Bank", style="SubHeader.TLabel").pack(anchor="w")

        # Status Tag Right side
        right = tk.Frame(frame, bg=header_bg)
        right.pack(side="right", fill="y", padx=20)

        self.status = ttk.Label(right, text="● READY", style="Status.TLabel")
        self.status.pack(expand=True)

    def create_body(self):

        self.body = tk.Frame(self.root, bg="#F3F4F6")
        self.body.pack(fill="both", expand=True, padx=12, pady=8)

        # Flexible Grid Configuration:
        # Row 2 (Live Log) expands dynamically to consume remaining screen height.
        self.body.grid_rowconfigure(0, weight=0)
        self.body.grid_rowconfigure(1, weight=0)
        self.body.grid_rowconfigure(2, weight=1)
        self.body.grid_columnconfigure(0, weight=1)

        self.create_top_cards_container()
        self.create_progress_card()
        self.create_log_card()

    def create_top_cards_container(self):

        top_container = tk.Frame(self.body, bg="#F3F4F6")
        top_container.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        top_container.grid_columnconfigure(0, weight=3)
        top_container.grid_columnconfigure(1, weight=1)

        # Connection Card
        conn_frame = ttk.LabelFrame(top_container, text=" Connection & Inputs ", style="Card.TLabelframe")
        conn_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        conn_frame.grid_columnconfigure(1, weight=1)

        # Row 0: Excel File
        ttk.Label(conn_frame, text="Excel File", style="Title.TLabel").grid(row=0, column=0, padx=10, pady=6, sticky="w")
        
        self.excel_entry = ttk.Entry(conn_frame, textvariable=self.excel_file)
        self.excel_entry.grid(row=0, column=1, padx=5, pady=6, sticky="ew")

        btn_box = tk.Frame(conn_frame, bg="white")
        btn_box.grid(row=0, column=2, padx=10, pady=6, sticky="e")

        self.browse_button = ttk.Button(btn_box, text="Browse", command=self.browse_excel)
        self.browse_button.pack(side="left", padx=2)

        self.template_button = ttk.Button(btn_box, text="Download Template", command=self.download_template)
        self.template_button.pack(side="left", padx=2)

        # Row 1: Mobile & Password
        creds_frame = tk.Frame(conn_frame, bg="white")
        creds_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=4)
        creds_frame.grid_columnconfigure(1, weight=1)
        creds_frame.grid_columnconfigure(3, weight=1)

        ttk.Label(creds_frame, text="Mobile Number", style="Title.TLabel").grid(row=0, column=0, padx=(0, 5), sticky="w")
        ttk.Entry(creds_frame, textvariable=self.mobile).grid(row=0, column=1, sticky="ew", padx=(0, 15))

        ttk.Label(creds_frame, text="Password", style="Title.TLabel").grid(row=0, column=2, padx=(0, 5), sticky="w")
        ttk.Entry(creds_frame, textvariable=self.password, show="*").grid(row=0, column=3, sticky="ew")

        # Row 2: Action Buttons
        action_bar = tk.Frame(conn_frame, bg="white")
        action_bar.grid(row=2, column=0, columnspan=3, pady=(6, 8))

        self.validate_button = ttk.Button(action_bar, text="Validate Excel", command=self.validate_excel)
        self.validate_button.pack(side="left", padx=5)

        self.login_button = ttk.Button(action_bar, text="Login to PMFBY", command=self.login, state="disabled")
        self.login_button.pack(side="left", padx=5)

        self.clear_button = ttk.Button(action_bar, text="Clear", command=self.clear_form)
        self.clear_button.pack(side="left", padx=5)

        # Upload Actions Card
        ##################################################
        # Execution Card
        ##################################################

        upload_frame = ttk.LabelFrame(
            top_container,
            text=" Execution ",
            style="Card.TLabelframe"
        )

        upload_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        ##################################################
        # Operation
        ##################################################

        ttk.Label(
            upload_frame,
            text="Operation",
            style="Title.TLabel"
        ).pack(
            anchor="w",
            padx=10,
            pady=(8, 2)
        )

        self.operation_combo = ttk.Combobox(

            upload_frame,

            textvariable=self.operation,

            values=[
                "Create Crop Insurance Policy",
                "Mark Account Not Eligible",
                "Change KCC Account Number"
            ],

            state="readonly"

        )

        self.operation_combo.pack(
            fill="x",
            padx=10,
            pady=(0, 6)
        )

        self.operation_combo.bind(
            "<<ComboboxSelected>>",
            self.operation_changed
        )

        ##################################################
        # PDF
        ##################################################

        self.pdf_frame = tk.Frame(
            upload_frame,
            bg="white"
        )

        self.pdf_frame.pack(
            fill="x",
            padx=10,
            pady=2
        )

        ttk.Label(
            self.pdf_frame,
            text="Unified PDF",
            style="Title.TLabel"
        ).pack(
            anchor="w"
        )

        pdf_row = tk.Frame(
            self.pdf_frame,
            bg="white"
        )

        pdf_row.pack(
            fill="x"
        )

        self.pdf_entry = ttk.Entry(
            pdf_row,
            textvariable=self.pdf_file
        )

        self.pdf_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.pdf_browse_button = ttk.Button(
            pdf_row,
            text="Browse",
            command=self.browse_pdf
        )

        self.pdf_browse_button.pack(
            side="left",
            padx=(4, 0)
        )

        ##################################################
        # Warning
        ##################################################

        ttk.Label(

            upload_frame,

            text="⚠️ Select Scheme and Branch in PMFBY portal after login.",

            style="Warning.TLabel",

            wraplength=220,

            justify="center"

        ).pack(
            anchor="center",
            padx=10,
            pady=(6, 4)
        )

        ##################################################
        # Start
        ##################################################

        self.upload_button = ttk.Button(

            upload_frame,

            text="Start Processing",

            command=self.start_processing,

            state="disabled",

            style="Primary.TButton"

        )

        self.upload_button.pack(
            fill="x",
            padx=15,
            pady=3
        )

        ##################################################
        # Cancel
        ##################################################

        self.cancel_button = ttk.Button(

            upload_frame,

            text="Cancel",

            command=self.cancel_upload,

            state="disabled"

        )

        self.cancel_button.pack(
            fill="x",
            padx=15,
            pady=(3, 8)
        )

        ##################################################
        # Initially hide PDF
        ##################################################

        self.pdf_frame.pack_forget()

    def create_progress_card(self):

        frame = ttk.LabelFrame(self.body, text=" Upload Progress ", style="Card.TLabelframe")
        frame.grid(row=1, column=0, sticky="ew", pady=(0, 6))

        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(3, weight=1)

        self.progress = ttk.Progressbar(frame, orient="horizontal", mode="determinate")
        self.progress.grid(row=0, column=0, columnspan=4, padx=12, pady=(8, 6), sticky="ew")

        ttk.Label(frame, text="Current Account:", style="Title.TLabel").grid(row=1, column=0, padx=(12, 4), pady=2, sticky="w")
        self.current_account = ttk.Label(frame, text="-", style="Value.TLabel")
        self.current_account.grid(row=1, column=1, sticky="w", padx=2)

        ttk.Label(frame, text="Success:", style="Title.TLabel").grid(row=1, column=2, padx=(20, 4), pady=2, sticky="w")
        self.success_count = tk.StringVar(value="0")
        ttk.Label(frame, textvariable=self.success_count, style="Success.TLabel").grid(row=1, column=3, sticky="w", padx=2)

        ttk.Label(frame, text="Current Khata:", style="Title.TLabel").grid(row=2, column=0, padx=(12, 4), pady=2, sticky="w")
        self.current_khata = ttk.Label(frame, text="-", style="Value.TLabel")
        self.current_khata.grid(row=2, column=1, sticky="w", padx=2)

        ttk.Label(frame, text="Failed:", style="Title.TLabel").grid(row=2, column=2, padx=(20, 4), pady=2, sticky="w")
        self.failed_count = tk.StringVar(value="0")
        ttk.Label(frame, textvariable=self.failed_count, style="Failed.TLabel").grid(row=2, column=3, sticky="w", padx=2)

        ttk.Label(frame, text="Current Survey:", style="Title.TLabel").grid(row=3, column=0, padx=(12, 4), pady=(2, 8), sticky="w")
        self.current_survey = ttk.Label(frame, text="-", style="Value.TLabel")
        self.current_survey.grid(row=3, column=1, sticky="w", padx=2, pady=(2, 8))

        ttk.Label(frame, text="Skipped:", style="Title.TLabel").grid(row=3, column=2, padx=(20, 4), pady=(2, 8), sticky="w")
        self.skipped_count = tk.StringVar(value="0")
        ttk.Label(frame, textvariable=self.skipped_count, style="Skipped.TLabel").grid(row=3, column=3, sticky="w", padx=2, pady=(2, 8))

    def create_log_card(self):

        frame = ttk.LabelFrame(self.body, text=" Live Log ", style="Card.TLabelframe")
        frame.grid(row=2, column=0, sticky="nsew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=6, padx=(0, 6))

        self.log = tk.Text(
            frame,
            wrap="word",
            font=("Consolas", 9),
            bg="#1E1E1E",
            fg="#D4D4D4",
            insertbackground="white",
            relief="flat",
            yscrollcommand=scrollbar.set
        )

        self.log.grid(row=0, column=0, sticky="nsew", padx=(6, 0), pady=6)
        scrollbar.config(command=self.log.yview)

    def create_footer(self):
        # Light Red Footer with pure black text
        bg_color = "#FEE2E2"
        text_color = "#000000"

        footer = tk.Frame(self.root, bg=bg_color, height=34)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        tk.Label(
            footer, text="Copyright © 2026", bg=bg_color, fg=text_color, font=("Segoe UI", 9)
        ).pack(side="left", padx=15)

        tk.Label(
            footer, text="Developed by APGBOA", bg=bg_color, fg=text_color, font=("Segoe UI", 9, "bold")
        ).pack(side="left", expand=True)

        tk.Label(
            footer, text="Version 1.1.0", bg=bg_color, fg=text_color, font=("Segoe UI", 9)
        ).pack(side="right", padx=15)

    def download_template(self):

        ##################################################
        # Ask destination folder
        ##################################################

        destination_folder = filedialog.askdirectory(

            title="Select folder to save PMFBY templates"

        )

        if not destination_folder:

            return

        ##################################################
        # Determine application base directory
        ##################################################

        if getattr(sys, "frozen", False):

            # PyInstaller application
            base_path = Path(
                sys.executable
            ).resolve().parent

            template_path = (
                base_path
                / "_internal"
                / "templates"
            )

        else:

            # Development
            base_path = Path(
                __file__
            ).resolve().parent.parent

            template_path = (
                base_path
                / "templates"
            )

        ##################################################
        # Template files
        ##################################################

        policy_template = (
            template_path
            / "PMFBY_Template.xlsx"
        )

        not_eligible_template = (
            template_path
            / "PMFBY_NotEligible_Template.xlsx"
        )

        change_account_template = (
            template_path
            / "PMFBY_Change_Accounts.xlsx"
        )

        ##################################################
        # Debug log - useful during development
        ##################################################

        self.write_log(
            f"Template directory: {template_path}"
        )

        self.write_log(
            f"Policy template: {policy_template}"
        )

        self.write_log(
            f"Not Eligible template: {not_eligible_template}"
        )
        self.write_log(
            f"Not Eligible template: {change_account_template}"
        )

        ##################################################
        # Check policy template
        ##################################################

        if not policy_template.is_file():

            messagebox.showerror(

                "Template Error",

                f"Policy template was not found.\n\n"
                f"Expected location:\n"
                f"{policy_template}"

            )

            return

        ##################################################
        # Check Not Eligible template
        ##################################################

        if not not_eligible_template.is_file():

            messagebox.showerror(

                "Template Error",

                f"Not Eligible template was not found.\n\n"
                f"Expected location:\n"
                f"{not_eligible_template}"

            )

            return
        ##################################################
        # Check Change Account template
        ###################################################
        if not change_account_template.is_file():

            messagebox.showerror(

                "Template Error",

                f"Change Account template was not found.\n\n"
                f"Expected location:\n"
                f"{change_account_template}"

            )

            return

        ##################################################
        # Copy templates
        ##################################################

        try:

            destination = Path(
                destination_folder
            )

            shutil.copy2(

                policy_template,

                destination
                / "PMFBY_Template.xlsx"

            )

            shutil.copy2(

                not_eligible_template,

                destination
                / "PMFBY_NotEligible_Template.xlsx"

            )

            shutil.copy2(

                change_account_template,

                Path(destination_folder)
                / "PMFBY_Change_Accounts.xlsx"

            )

            ##################################################
            # Success
            ##################################################

            self.write_log(
                "Both PMFBY templates copied successfully."
            )

            messagebox.showinfo(

                "Templates",

                "All PMFBY templates were downloaded successfully."

            )

        except Exception as ex:

            self.write_log(
                f"Template copy failed: {str(ex)}"
            )

            messagebox.showerror(

                "Template Error",

                f"Unable to download templates.\n\n"
                f"{str(ex)}"

            )
    def clear_form(self):

        self.excel_file.set("")
        self.mobile.set("")
        self.password.set("")

        self.pdf_file.set("")

        self.operation.set(
            "Create Crop Insurance Policy"
        )

        self.pdf_frame.pack_forget()

        self.log.delete("1.0", tk.END)
        self.status.config(text="● READY")

        self.login_button.config(state="disabled")
        self.upload_button.config(state="disabled")
        # Reset Progress Card UI
        self.reset_progress_card()

    def reset_progress_card(self):
        """Resets the progress bar, current targets, and stat counters."""
        self.progress["value"] = 0
        self.progress["maximum"] = 100

        self.current_account.config(text="-")
        self.current_khata.config(text="-")
        self.current_survey.config(text="-")

        self.success_count.set("0")
        self.failed_count.set("0")
        self.skipped_count.set("0")

    def browse_excel(self):

        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[
                ("Excel Files", "*.xlsx"),
                ("All Files", "*.*")
            ]
        )

        if filename:
            self.excel_file.set(filename)
            self.write_log(f"Excel selected : {filename}")
            self.set_status("Excel Selected")

    def validate_excel(self):

        ##################################################
        # Clear previous log
        ##################################################

        self.log.delete(
            "1.0",
            tk.END
        )

        ##################################################
        # Excel file
        ##################################################

        excel_file = self.excel_file.get().strip()

        if excel_file == "":

            self.set_status(
                "No Excel File Selected"
            )

            messagebox.showerror(
                "Validation Error",
                "Please select an Excel file."
            )

            return

        ##################################################
        # File exists
        ##################################################

        if not os.path.exists(excel_file):

            self.set_status(
                "File Not Found"
            )

            messagebox.showerror(
                "Validation Error",
                "Selected file does not exist."
            )

            return

        ##################################################
        # Extension
        ##################################################

        extension = os.path.splitext(
            excel_file
        )[1].lower()

        if extension != ".xlsx":

            self.set_status(
                "Invalid File"
            )

            messagebox.showerror(
                "Validation Error",
                "Only .xlsx files are supported."
            )

            return

        ##################################################
        # Validation
        ##################################################

        try:

            self.write_log(
                "Starting Excel validation..."
            )

            ##################################################
            # Select validator based on operation
            ##################################################

            operation = self.operation.get()

            ##################################################
            # Existing Policy workflow
            ##################################################

            if operation == "Create Crop Insurance Policy":

                validator = ExcelValidator()

                result = validator.validate(
                    excel_file
                )

                ##################################################
                # Existing validator result object
                ##################################################

                if result.success:

                    self.write_log(
                        "Excel validation completed successfully."
                    )

                    self.set_status(
                        "Validation Successful"
                    )

                    self.set_ui_state(
                        "VALIDATED"
                    )

                    messagebox.showinfo(
                        "Validation",
                        "Excel validated successfully."
                    )

                else:

                    self.set_status(
                        "Validation Failed"
                    )

                    self.set_ui_state(
                        "READY"
                    )

                    self.write_log(
                        f"{len(result.errors)} validation error(s) found."
                    )

                    self.write_log(
                        "-" * 70
                    )

                    for error in result.errors:

                        self.write_log(
                            f"Row {error.row} | "
                            f"{error.column} | "
                            f"{error.message}"
                        )

                    self.write_log(
                        "-" * 70
                    )

                    messagebox.showerror(

                        "Validation Failed",

                        f"{len(result.errors)} validation error(s) found.\n\n"
                        "Please correct the Excel file and validate again."

                    )

                return

            ##################################################
            # Not Eligible workflow
            ##################################################

            elif operation == "Mark Account Not Eligible":

                validator = NotEligibleExcelValidator()

                valid, errors = validator.validate(
                    excel_file
                )

                ##################################################
                # Success
                ##################################################

                if valid:

                    self.write_log(
                        "Not Eligible Excel validation completed successfully."
                    )

                    self.set_status(
                        "Validation Successful"
                    )

                    self.set_ui_state(
                        "VALIDATED"
                    )

                    messagebox.showinfo(

                        "Validation",

                        "Not Eligible Excel validated successfully."

                    )

                ##################################################
                # Failure
                ##################################################

                else:

                    self.set_status(
                        "Validation Failed"
                    )

                    self.set_ui_state(
                        "READY"
                    )

                    self.write_log(
                        f"{len(errors)} validation error(s) found."
                    )

                    self.write_log(
                        "-" * 70
                    )

                    for error in errors:

                        self.write_log(
                            error
                        )

                    self.write_log(
                        "-" * 70
                    )

                    messagebox.showerror(

                        "Validation Failed",

                        f"{len(errors)} validation error(s) found.\n\n"
                        "Please correct the Excel file and validate again."

                    )

                return
             ########################################################################
            # Change Account workflow   
            ########################################################################
            elif operation == "Change KCC Account Number":

                validator = ChangeAccountExcelValidator()

                valid, errors = validator.validate(

                    excel_file

                )

                ##################################################
                # Validation successful
                ##################################################

                if valid:

                    self.write_log(

                        "Change Account Excel validation "
                        "completed successfully."

                    )

                    self.set_status(

                        "Validation Successful"

                    )

                    self.set_ui_state(

                        "VALIDATED"

                    )

                    messagebox.showinfo(

                        "Validation",

                        "Change Account Excel validated successfully."

                    )

                ##################################################
                # Validation failed
                ##################################################

                else:

                    self.set_status(

                        "Validation Failed"

                    )

                    self.set_ui_state(

                        "READY"

                    )

                    self.write_log(

                        f"{len(errors)} validation error(s) found."

                    )

                    self.write_log(

                        "-" * 70

                    )

                    for error in errors:

                        self.write_log(

                            error

                        )

                    self.write_log(

                        "-" * 70

                    )

                    messagebox.showerror(

                        "Validation Failed",

                        f"{len(errors)} validation error(s) found.\n\n"
                        "Please correct the Excel file and validate again."

                    )

                return

            ##################################################
            # Unknown operation
            ##################################################

            else:

                self.set_status(
                    "Invalid Operation"
                )

                self.set_ui_state(
                    "READY"
                )

                messagebox.showerror(

                    "Validation Error",

                    "Unknown processing operation selected."

                )

        ##################################################
        # Unexpected validation error
        ##################################################

        except Exception as ex:

            self.set_status(
                "Validation Failed"
            )

            self.set_ui_state(
                "READY"
            )

            self.write_log(
                f"Validation Error : {str(ex)}"
            )

            messagebox.showerror(

                "Validation Error",

                str(ex)

            )

    def start_upload(self):

        if not self.logged_in:
            messagebox.showerror("Upload", "Please login first.")
            return

        self.set_ui_state("UPLOADING")
        self.upload_worker()

    def upload_worker(self):

        self.reporter = Reporter(logger=self.write_log)
        self.upload_running = True

        self.update_progress(
            current=0,
            total=0,
            success=0,
            failed=0,
            skipped=0
        )

        try:
            self.reporter.info("", "UPLOAD", "Reading Excel...")

            reader = ExcelReader()
            accounts = reader.read(self.excel_file.get())

            self.reporter.info("", "UPLOAD", f"{len(accounts)} account(s) loaded from Excel.")

            workflow = WorkflowEngine(
                navigator=self.navigator,
                actions=self.actions,
                reporter=self.reporter,
                worker=self.worker,
                progress_callback=self.update_progress,
            )

            workflow.process(accounts)

            self.update_progress(
                current=len(accounts),
                total=len(accounts),
                success=self.reporter.success_count,
                failed=self.reporter.failed_count,
                skipped=self.reporter.skipped_count
            )

            report_file = self.reporter.summary()
            self.reporter.info("", "REPORT", f"Execution report exported successfully:   {report_file}")
            self.set_status("Completed")

        except Exception as ex:
            self.reporter.error("", "UPLOAD", str(ex))
            self.set_status("Upload Failed")
            self.upload_running = False

        finally:
            self.set_ui_state("COMPLETED")
            self.upload_running = False

    def cancel_upload(self):
        self.worker.cancel()
        self.write_log("Cancellation requested...")

    def write_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log.insert("end", f"[{timestamp}] {message}\n")
        self.log.see("end")

    def set_ui_state(self, state):

        if state == "READY":
            self.validate_button.config(state="normal")
            self.login_button.config(state="disabled")
            self.upload_button.config(state="disabled")
            self.cancel_button.config(state="disabled")

        elif state == "VALIDATED":
            self.validate_button.config(state="normal")
            self.login_button.config(state="normal")
            self.upload_button.config(state="disabled")
            self.cancel_button.config(state="disabled")

        elif state == "LOGGED_IN":
            self.validate_button.config(state="disabled")
            self.login_button.config(state="disabled")
            self.upload_button.config(state="normal")
            self.cancel_button.config(state="disabled")

        elif state == "UPLOADING":
            self.validate_button.config(state="disabled")
            self.login_button.config(state="disabled")
            self.upload_button.config(state="disabled")
            self.cancel_button.config(state="normal")

        elif state == "COMPLETED":
            self.validate_button.config(state="normal")
            self.login_button.config(state="disabled")
            self.upload_button.config(state="disabled")
            self.cancel_button.config(state="disabled")

    def login(self):

        if self.logged_in:
            messagebox.showinfo("PMFBY", "Already logged in.")
            return

        if not self.mobile.get().strip():
            messagebox.showerror("Login", "Please enter Mobile Number.")
            return

        if not self.password.get().strip():
            messagebox.showerror("Login", "Please enter Password.")
            return

        self.login_worker()

    def login_worker(self):

        try:
            if hasattr(self, "browser") and self.browser:
                self.browser.close()
                self.browser = None

            self.write_log("Launching browser...")
            self.set_status("Launching Browser...")

            self.browser = BrowserSession()
            login = PMFBYLogin(self.browser)

            login.login(self.mobile.get().strip(), self.password.get().strip())

            self.navigator = PMFBYNavigator(self.browser)
            self.actions = PMFBYActions(self.browser)
            self.logged_in = True

            self.write_log("Login successful.")
            self.write_log("Please complete Scheme and Branch selection in the browser.")
            self.set_status("Logged In")
            self.set_ui_state("LOGGED_IN")

        except Exception as ex:
            self.logged_in = False
            self.write_log(f"Login failed : {str(ex)}")
            self.set_status("Login Failed")
            self.set_ui_state("VALIDATED")

    def set_status(self, text):
        self.status.config(text=f"● {text.upper()}")

    def update_progress(
        self,
        current=None,
        total=None,
        account="",
        khata="",
        survey="",
        success=None,
        failed=None,
        skipped=None
    ):
        self.root.after(
            0,
            lambda: self._update_progress_ui(
                current, total, account, khata, survey, success, failed, skipped
            )
        )

    def _update_progress_ui(
        self, current, total, account, khata, survey, success, failed, skipped
    ):
        if current is not None and total is not None:
            self.progress["maximum"] = total
            self.progress["value"] = current

        if account:
            self.current_account.config(text=account)

        if khata:
            self.current_khata.config(text=khata)

        if survey:
            self.current_survey.config(text=survey)

        if success is not None:
            self.success_count.set(str(success))

        if failed is not None:
            self.failed_count.set(str(failed))

        if skipped is not None:
            self.skipped_count.set(str(skipped))

        self.root.update_idletasks()

    def on_close(self):
        if self.upload_running:
            answer = messagebox.askyesno("Exit", "Upload is still running.\n\nStop upload and exit?")
            if not answer:
                return
            self.worker.cancel()

        try:
            if self.browser:
                self.browser.close()
        except Exception:
            pass

        self.root.destroy()

    def browse_pdf(self):

        filename = filedialog.askopenfilename(

            title="Select Unified PDF",

            filetypes=[
                ("PDF Files", "*.pdf")
            ]

        )

        if filename:

            self.pdf_file.set(filename)

            self.write_log(
                f"PDF selected : {filename}"
            )
    def operation_changed(self, event=None):

        operation = self.operation.get()

        ##################################################
        # Not Eligible
        ##################################################

        if operation == "Mark Account Not Eligible":

            self.pdf_frame.pack(
                fill="x",
                padx=10,
                pady=2,
                # before=self.operation_combo
            )

        ##################################################
        # Existing Policy flow
        ##################################################

        else:

            self.pdf_file.set("")

            self.pdf_frame.pack_forget()

    def start_processing(self):

        operation = self.operation.get()

        ##################################################
        # Existing policy workflow
        ##################################################

        if operation == "Create Crop Insurance Policy":

            self.start_upload()

            return

        ##################################################
        # Not Eligible
        ##################################################

        if operation == "Mark Account Not Eligible":

            self.start_not_eligible()

            return
        ##################################################
        # Change Account workflow
        ##################################################
        if operation == "Change KCC Account Number":

            self.start_change_account()

            return
    def start_change_account(self):

        if not self.logged_in:

            messagebox.showerror(
                "Not Eligible",
                "Please login first."
            )

            return
       
        ##################################################
        # Start
        ##################################################

        self.set_ui_state(
            "UPLOADING"
        )

        self.change_account_worker()
    def change_account_worker(self):

        self.reporter = Reporter(
            logger=self.write_log
        )

        self.upload_running = True

        self.update_progress(

            current=0,

            total=0,

            success=0,

            failed=0,

            skipped=0

        )

        try:

            ##################################################
            # Read Excel
            ##################################################

            self.reporter.info(

                "",

                "UPLOAD",

                "Reading Not Eligible Excel..."

            )

            reader = ChangeAccountExcelReader()

            accounts = reader.read(
                self.excel_file.get()
            )

            self.reporter.info(

                "",

                "UPLOAD",

                f"{len(accounts)} account(s) loaded."

            )

            ##################################################
            # Workflow
            ##################################################

            workflow = ChangeAccountWorkflowEngine(

                navigator=self.navigator,

                reporter=self.reporter,

                worker=self.worker,

                progress_callback=self.update_progress

            )

            workflow.process(
                accounts
            )

            ##################################################
            # Final progress
            ##################################################

            self.update_progress(

                current=len(accounts),

                total=len(accounts),

                success=self.reporter.success_count,

                failed=self.reporter.failed_count,

                skipped=self.reporter.skipped_count

            )

            ##################################################
            # Report
            ##################################################

            report_file = self.reporter.summary()

            self.reporter.info(

                "",

                "REPORT",

                f"Execution report exported successfully: {report_file}"

            )

            self.set_status(
                "Completed"
            )

        except Exception as ex:

            self.reporter.error(

                "",

                "UPLOAD",

                str(ex)

            )

            self.set_status(
                "Upload Failed"
            )

        finally:

            self.upload_running = False

            self.set_ui_state(
                "COMPLETED"
            )
    def start_not_eligible(self):

        if not self.logged_in:

            messagebox.showerror(
                "Not Eligible",
                "Please login first."
            )

            return

        ##################################################
        # PDF required
        ##################################################

        pdf_file = self.pdf_file.get().strip()

        if not pdf_file:

            messagebox.showerror(
                "Not Eligible",
                "Please select the unified PDF file."
            )

            return

        if not os.path.exists(pdf_file):

            messagebox.showerror(
                "Not Eligible",
                "Selected PDF file does not exist."
            )

            return

        ##################################################
        # PDF extension
        ##################################################

        if Path(pdf_file).suffix.lower() != ".pdf":

            messagebox.showerror(
                "Not Eligible",
                "Only PDF files are supported."
            )

            return

        
        ##################################################
        # Start
        ##################################################

        self.set_ui_state(
            "UPLOADING"
        )

        self.not_eligible_worker()
    def not_eligible_worker(self):

        self.reporter = Reporter(
            logger=self.write_log
        )

        self.upload_running = True

        self.update_progress(

            current=0,

            total=0,

            success=0,

            failed=0,

            skipped=0

        )

        try:

            ##################################################
            # Read Excel
            ##################################################

            self.reporter.info(

                "",

                "UPLOAD",

                "Reading Not Eligible Excel..."

            )

            reader = NotEligibleExcelReader()

            accounts = reader.read(
                self.excel_file.get()
            )

            self.reporter.info(

                "",

                "UPLOAD",

                f"{len(accounts)} account(s) loaded."

            )

            ##################################################
            # Workflow
            ##################################################

            workflow = NotEligibleWorkflowEngine(

                navigator=self.navigator,

                reporter=self.reporter,

                worker=self.worker,

                pdf_file=self.pdf_file.get(),

                progress_callback=self.update_progress

            )

            workflow.process(
                accounts
            )

            ##################################################
            # Final progress
            ##################################################

            self.update_progress(

                current=len(accounts),

                total=len(accounts),

                success=self.reporter.success_count,

                failed=self.reporter.failed_count,

                skipped=self.reporter.skipped_count

            )

            ##################################################
            # Report
            ##################################################

            report_file = self.reporter.summary()

            self.reporter.info(

                "",

                "REPORT",

                f"Execution report exported successfully: {report_file}"

            )

            self.set_status(
                "Completed"
            )

        except Exception as ex:

            self.reporter.error(

                "",

                "UPLOAD",

                str(ex)

            )

            self.set_status(
                "Upload Failed"
            )

        finally:

            self.upload_running = False

            self.set_ui_state(
                "COMPLETED"
            )
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()