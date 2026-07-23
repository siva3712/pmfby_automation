import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import os
import shutil

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


class MainWindow:

    def __init__(self):

        ##################################################
        # Window
        ##################################################

        self.root = tk.Tk()

        self.root.title(
            "PMFBY Bulk Uploader"
        )

        self.root.geometry("1100x760")

        self.root.minsize(
            1100,
            760
        )

        self.root.configure(
            bg="#eef2f7"
        )

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

    
    def configure_styles(self):

        self.style.configure(

            "Header.TLabel",

            background="#0B5CAD",

            foreground="white",

            font=("Segoe UI", 18, "bold")

        )

        self.style.configure(

            "SubHeader.TLabel",

            background="#0B5CAD",

            foreground="white",

            font=("Segoe UI", 10)

        )

        self.style.configure(

            "Card.TLabelframe",

            background="white"

        )

        self.style.configure(

            "Card.TLabelframe.Label",

            font=("Segoe UI", 10, "bold")

        )

        self.style.configure(

            "Title.TLabel",

            font=("Segoe UI", 10, "bold"),

            background="white"

        )

        self.style.configure(

            "Green.TButton",

            font=("Segoe UI", 10, "bold")

        )

        self.style.configure(

            "Blue.TButton",

            font=("Segoe UI", 10, "bold")

        )

        self.style.configure(

            "Orange.TButton",

            font=("Segoe UI", 10, "bold")

        )

        self.style.configure(

            "Status.TLabel",

            font=("Segoe UI", 10, "bold"),

            background="#eef2f7"

        )
    def create_header(self):

        frame = tk.Frame(
            self.root,
            bg="#0B5CAD",
            height=75
        )
        frame.pack(fill="x")
        frame.pack_propagate(False)

        ####################################################
        # Left Frame
        ####################################################

        left = tk.Frame(frame, bg="#0B5CAD")
        left.pack(side="left", fill="y", padx=20)

        ttk.Label(
            left,
            text="PMFBY BULK UPLOADER",
            style="Header.TLabel"
        ).pack(anchor="w", pady=(10, 0))

        ttk.Label(
            left,
            text="Andhra Pradesh Grameena Bank",
            style="SubHeader.TLabel"
        ).pack(anchor="w")

        ####################################################
        # Right Frame
        ####################################################

        right = tk.Frame(frame, bg="#0B5CAD")
        right.pack(side="right", fill="y", padx=20)

        self.status = ttk.Label(
            right,
            text="🟢 READY",
            style="SubHeader.TLabel"
        )

        self.status.pack(expand=True)

    def create_body(self):

        self.body = tk.Frame(

            self.root,

            bg="#eef2f7"

        )

        self.body.pack(

            fill="both",

            expand=True,

            padx=15,

            pady=10

        )
        self.create_connection_card()

        self.create_upload_card()

        self.create_progress_card()

        self.create_log_card()
    def create_connection_card(self):

        frame = ttk.LabelFrame(
            self.body,
            text=" Connection ",
            style="Card.TLabelframe"
        )

        frame.pack(
            fill="x",
            pady=(0, 10)
        )

        ####################################################
        # Excel File
        ####################################################

        ttk.Label(
            frame,
            text="Excel File",
            style="Title.TLabel"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=15,
            sticky="w"
        )

        self.excel_entry = ttk.Entry(
            frame,
            textvariable=self.excel_file,
            width=70
        )

        self.excel_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=15,
            sticky="ew"
        )

        self.browse_button = ttk.Button(
            frame,
            text="Browse",
            command=self.browse_excel
        )

        self.browse_button.grid(
            row=0,
            column=2,
            padx=5
        )

        self.template_button = ttk.Button(
            frame,
            text="Download Template",
            command=self.download_template
        )

        self.template_button.grid(
            row=0,
            column=3,
            padx=5
        )

        ####################################################
        # Mobile
        ####################################################

        ttk.Label(
            frame,
            text="Mobile Number",
            style="Title.TLabel"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        ttk.Entry(
            frame,
            textvariable=self.mobile,
            width=30
        ).grid(
            row=1,
            column=1,
            sticky="w",
            padx=5
        )

        ####################################################
        # Password
        ####################################################

        ttk.Label(
            frame,
            text="Password",
            style="Title.TLabel"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        ttk.Entry(
            frame,
            textvariable=self.password,
            show="*",
            width=30
        ).grid(
            row=2,
            column=1,
            sticky="w",
            padx=5
        )

        ####################################################
        # Buttons
        ####################################################

        button_frame = tk.Frame(
            frame,
            bg="white"
        )

        button_frame.grid(
            row=3,
            column=0,
            columnspan=4,
            pady=15
        )

        self.validate_button = ttk.Button(
            button_frame,
            text="Validate Excel",
            command=self.validate_excel
        )

        self.validate_button.pack(
            side="left",
            padx=5
        )

        self.login_button = ttk.Button(
            button_frame,
            text="Login to PMFBY",
            command=self.login,
            state="disabled"
        )

        self.login_button.pack(
            side="left",
            padx=5
        )

        self.clear_button = ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_form
        )

        self.clear_button.pack(
            side="left",
            padx=5
        )

        frame.columnconfigure(
            1,
            weight=1
        )

    def create_upload_card(self):

        frame = ttk.LabelFrame(
            self.body,
            text=" Upload ",
            style="Card.TLabelframe"
        )

        frame.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Label(
            frame,
            text="After successful login,\nselect Scheme and Branch in the PMFBY portal.",
            foreground="red"
        ).pack(
            anchor="w",
            padx=10,
            pady=10
        )

        self.upload_button = ttk.Button(
            frame,
            text="Start Upload",
            command=self.start_upload,
            state="disabled"
        )

        self.upload_button.pack(
            pady=10
        )

        self.cancel_button = ttk.Button(
            frame,
            text="Cancel Upload",
            command=self.cancel_upload,
            state="disabled"
        )

        self.cancel_button.pack(
            pady=(0, 10)
        )




    def download_template(self):

        source = "templates/PMFBY_Template.xlsx"

        destination = filedialog.asksaveasfilename(

            title="Save Template",

            initialfile="PMFBY_Template.xlsx",

            defaultextension=".xlsx",

            filetypes=[

                ("Excel Workbook", "*.xlsx")

            ]

        )

        if not destination:
            return

        shutil.copy2(
            source,
            destination
        )

        messagebox.showinfo(

            "Template",

            "Template downloaded successfully."

        )
    
    def clear_form(self):

        self.excel_file.set("")

        self.mobile.set("")

        self.password.set("")

        self.log.delete(
            "1.0",
            tk.END
        )

        self.status.config(
            text="● READY"
        )

        self.login_button.config(
            state="disabled"
        )

        self.upload_button.config(
            state="disabled"
        )

    def create_progress_card(self):

        frame = ttk.LabelFrame(
            self.body,
            text=" Upload Progress ",
            style="Card.TLabelframe"
        )

        frame.pack(
            fill="x",
            pady=(0, 10)
        )

        ####################################################
        # Progress Bar
        ####################################################

        self.progress = ttk.Progressbar(
            frame,
            orient="horizontal",
            mode="determinate",
            length=850
        )

        self.progress.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=15,
            pady=(15, 10),
            sticky="ew"
        )

        ####################################################
        # Current Account
        ####################################################

        ttk.Label(
            frame,
            text="Current Account",
            style="Title.TLabel"
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.current_account = ttk.Label(
            frame,
            text="-"
        )

        self.current_account.grid(
            row=1,
            column=1,
            sticky="w"
        )

        ####################################################
        # Current Khata
        ####################################################

        ttk.Label(
            frame,
            text="Current Khata",
            style="Title.TLabel"
        ).grid(
            row=2,
            column=0,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.current_khata = ttk.Label(
            frame,
            text="-"
        )

        self.current_khata.grid(
            row=2,
            column=1,
            sticky="w"
        )

        ####################################################
        # Current Survey
        ####################################################

        ttk.Label(
            frame,
            text="Current Survey",
            style="Title.TLabel"
        ).grid(
            row=3,
            column=0,
            padx=15,
            pady=(5, 15),
            sticky="w"
        )

        self.current_survey = ttk.Label(
            frame,
            text="-"
        )

        self.current_survey.grid(
            row=3,
            column=1,
            sticky="w"
        )

        ####################################################
        # Statistics
        ####################################################

        self.success_count = tk.StringVar(value="0")

        self.failed_count = tk.StringVar(value="0")

        self.skipped_count = tk.StringVar(value="0")

        ttk.Label(
            frame,
            text="Success",
            style="Title.TLabel"
        ).grid(
            row=1,
            column=2,
            padx=(40, 5),
            sticky="w"
        )

        ttk.Label(
            frame,
            textvariable=self.success_count,
            foreground="green"
        ).grid(
            row=1,
            column=3,
            sticky="w"
        )

        ttk.Label(
            frame,
            text="Failed",
            style="Title.TLabel"
        ).grid(
            row=2,
            column=2,
            padx=(40, 5),
            sticky="w"
        )

        ttk.Label(
            frame,
            textvariable=self.failed_count,
            foreground="red"
        ).grid(
            row=2,
            column=3,
            sticky="w"
        )

        ttk.Label(
            frame,
            text="Skipped",
            style="Title.TLabel"
        ).grid(
            row=3,
            column=2,
            padx=(40, 5),
            sticky="w"
        )

        ttk.Label(
            frame,
            textvariable=self.skipped_count,
            foreground="orange"
        ).grid(
            row=3,
            column=3,
            sticky="w"
        )

        frame.columnconfigure(
            1,
            weight=1
        )
    
    def create_log_card(self):

        frame = ttk.LabelFrame(
            self.body,
            text=" Live Log ",
            style="Card.TLabelframe"
        )

        frame.pack(
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.log = tk.Text(

            frame,

            wrap="word",

            font=("Consolas", 10),

            bg="#1E1E1E",

            fg="#DDDDDD",

            insertbackground="white",

            yscrollcommand=scrollbar.set

        )

        self.log.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )

        scrollbar.config(
            command=self.log.yview
        )
    def create_footer(self):
        # A clean, light mint green background
        bg_color = "#e8f5e9"
        text_color = "#2c3e50"
        
        # Increased height slightly to 50 so elements fit beautifully vertically
        footer = tk.Frame(
            self.root,
            bg=bg_color,
            height=50
        )
        footer.pack(
            fill="x",
            side="bottom"
        )
        footer.pack_propagate(False)

        # 1. EYE-CATCHING CENTER LABEL
        # Pack this first with expand=True to anchor it right in the middle
        tk.Label(
            footer,
            text="Developed by APGBOA",
            bg=bg_color,
            fg="#2e7d32",  # A deeper green for better contrast and pop
            font=("Segoe UI", 12, "bold")  # Added bold to make it eye-catching
        ).pack(
            side="top",
            expand=True,
            pady=(5, 0)
        )

        # 2. COPYRIGHT LABEL (Bottom Left)
        tk.Label(
            footer,
            text="Copyright © 2026",
            bg=bg_color,
            fg=text_color,
            font=("Segoe UI", 9)
        ).pack(
            side="left",
            padx=15,
            pady=(0, 5)
        )

        # 3. VERSION LABEL (Bottom Right)
        tk.Label(
            footer,
            text="Version 1.0.0",
            bg=bg_color,
            fg=text_color,
            font=("Segoe UI", 9)
        ).pack(
            side="right",
            padx=15,
            pady=(0, 5)
        )


    

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

            self.write_log(
                f"Excel selected : {filename}"
            )

            self.set_status(
                "Excel Selected"
            )
    
   


    def validate_excel(self):

        ####################################################
        # Clear Previous Log
        ####################################################

        self.log.delete("1.0", tk.END)

        ####################################################
        # Excel Selected?
        ####################################################

        excel_file = self.excel_file.get().strip()

        if excel_file == "":

            self.set_status("No Excel File Selected")

            messagebox.showerror(
                "Validation Error",
                "Please select an Excel file."
            )

            return

        ####################################################
        # File Exists?
        ####################################################

        if not os.path.exists(excel_file):

            self.set_status("File Not Found")

            messagebox.showerror(
                "Validation Error",
                "Selected file does not exist."
            )

            return

        ####################################################
        # Extension Check
        ####################################################

        extension = os.path.splitext(excel_file)[1].lower()

        if extension != ".xlsx":

            self.set_status("Invalid File")

            messagebox.showerror(
                "Validation Error",
                "Only .xlsx files are supported."
            )

            return

        ####################################################
        # Validate
        ####################################################

        try:

            self.write_log("Starting Excel validation...")

            validator = ExcelValidator()

            result = validator.validate(excel_file)

            if result.success:

                self.write_log("Excel validation completed successfully.")

              
                self.set_status("Validation Successful")

                self.set_ui_state("VALIDATED")

                messagebox.showinfo(
                    "Validation",
                    "Excel validated successfully."
                )

            else:

                self.set_status("Validation Failed")

                self.set_ui_state("READY")

                self.write_log(
                    f"{len(result.errors)} validation error(s) found."
                )

                self.write_log("-" * 70)

                for error in result.errors:

                    self.write_log(

                        f"Row {error.row} | "
                        f"{error.column} | "
                        f"{error.message}"

                    )

                self.write_log("-" * 70)

                messagebox.showerror(

                    "Validation Failed",

                    f"{len(result.errors)} validation error(s) found.\n\n"
                    "Please correct the Excel file and validate again."

                )

        except Exception as ex:

            self.set_status("Validation Failed")

            self.set_ui_state("READY")

            self.write_log(f"Validation Error : {str(ex)}")

            messagebox.showerror(
                "Validation Error",
                str(ex)
            )
    
    def start_upload(self):

        if not self.logged_in:

            messagebox.showerror(
                "Upload",
                "Please login first."
            )

            return

        # if self.worker.is_running():

        #     return

        self.set_ui_state(
            "UPLOADING"
        )

        # self.worker.start(
        #     self.upload_worker
        # )
        # Run directly on the main thread
        self.upload_worker()
    
    def upload_worker(self):

        ##################################################
        # Create Reporter first
        ##################################################

        self.reporter = Reporter(
            logger=self.write_log
        )

        try:

            ##################################################
            # Read Excel
            ##################################################

            self.reporter.info(
                "",
                "UPLOAD",
                "Reading Excel..."
            )

            reader = ExcelReader()

            accounts = reader.read(
                self.excel_file.get()
            )

            self.reporter.info(
                "",
                "UPLOAD",
                f"{len(accounts)} account(s) loaded from Excel."
            )

            ##################################################
            # Workflow
            ##################################################

            workflow = WorkflowEngine(

                navigator=self.navigator,

                actions=self.actions,

                reporter=self.reporter,

                worker=self.worker,

                progress_callback=self.update_progress,

            )

            workflow.process(
                accounts
            )

            ##################################################
            # Export Report
            ##################################################

            report_file = self.reporter.summary()

            self.reporter.info(

                "",

                "REPORT",

                f"Execution report exported successfully:   {report_file}"

            )


            self.set_status(
                "Completed"
            )

        ##################################################

        except Exception as ex:

            self.reporter.error(

                "",

                "UPLOAD",

                str(ex)

            )

            self.set_status(
                "Upload Failed"
            )

        ##################################################

        finally:

            self.set_ui_state(
                "COMPLETED"
            )
    def cancel_upload(self):

        # if self.worker.is_running():

        #     self.worker.cancel()

        #     self.write_log(
        #         "Cancellation requested..."
        #     )

        #     self.set_status(
        #         "Stopping..."
        #     )
        self.worker.cancel()
        self.write_log(
            "Cancellation requested..."
        )

    def write_log(self, message):

        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )

        # self.root.after(

        #     0,

        #     lambda: (
        #         self.log.insert(
        #             "end",
        #             f"[{timestamp}] {message}\n"
        #         ),
        #         self.log.see("end")
        #     )

        # )

        self.log.insert(
            "end",
            f"[{timestamp}] {message}\n"
        )

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

        # if self.worker.is_running():
        #     return
        if self.logged_in:

            messagebox.showinfo(
                "PMFBY",
                "Already logged in."
            )
            return

        if not self.mobile.get().strip():

            messagebox.showerror(
                "Login",
                "Please enter Mobile Number."
            )

            return

        if not self.password.get().strip():

            messagebox.showerror(
                "Login",
                "Please enter Password."
            )

            return

        # self.worker.start(
        #     self.login_worker
        # )
        # Run directly on the main thread
        self.login_worker()
    def login_worker(self):

        try:

            self.write_log(
                "Launching browser..."
            )

            self.set_status(
                "Launching Browser..."
            )

            self.browser = BrowserSession()

            login = PMFBYLogin(
                self.browser
            )

            login.login(

                self.mobile.get().strip(),

                self.password.get().strip()

            )

            self.navigator = PMFBYNavigator(
                self.browser
            )

            self.actions = PMFBYActions(
                self.browser
            )

            self.logged_in = True

            self.write_log(
                "Login successful."
            )

            self.write_log(
                "Please complete Scheme and Branch selection in the browser."
            )

            self.set_status(
                "Logged In"
            )

            # self.root.after(
            #     0,
            #     lambda: self.set_ui_state(
            #         "LOGGED_IN"
            #     )
            # )

            self.set_ui_state(
                "LOGGED_IN"
            )

        except Exception as ex:

            self.logged_in = False

            self.write_log(
                f"Login failed : {str(ex)}"
            )

            self.set_status(
                "Login Failed"
            )

            # self.root.after(
            #     0,
            #     lambda: self.set_ui_state(
            #         "VALIDATED"
            #     )
            # )
            self.set_ui_state(
                "VALIDATED"
            )
    def set_status(self, text):

        # self.root.after(

        #     0,

        #     lambda: self.status.config(
        #         text=f"● {text.upper()}"
        #     )

        # )
        self.status.config(
            text=f"● {text.upper()}"
        )
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

                current,

                total,

                account,

                khata,

                survey,

                success,

                failed,

                skipped

            )

        )
    
    def _update_progress_ui(
    self,
    current,
    total,
    account,
    khata,
    survey,
    success,
    failed,
    skipped
    ):

        ##################################################
        # Progress Bar
        ##################################################

        if current is not None and total is not None:

            self.progress["maximum"] = total

            self.progress["value"] = current

        ##################################################
        # Current Account
        ##################################################

        if account:

            self.current_account.config(
                text=account
            )

        ##################################################
        # Current Khata
        ##################################################

        if khata:

            self.current_khata.config(
                text=khata
            )

        ##################################################
        # Current Survey
        ##################################################

        if survey:

            self.current_survey.config(
                text=survey
            )

        ##################################################
        # Statistics
        ##################################################

        if success is not None:

            self.success_count.set(
                str(success)
            )

        if failed is not None:

            self.failed_count.set(
                str(failed)
            )

        if skipped is not None:

            self.skipped_count.set(
                str(skipped)
            )
    def run(self):

        self.root.mainloop()