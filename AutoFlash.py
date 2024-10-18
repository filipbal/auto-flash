import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QComboBox, QCheckBox
from pywinauto import Application
import time

# Define name and version
NAME_AUTOFLASH = 'AutoFlash'
VERSION_AUTOFLASH = '0.3.4'

class AutomateFlashService(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.instance_label = QLabel('Enter first Flash Service instance number: <1;24>')
        self.instance_input = QLineEdit()

        self.model_type_label = QLabel('Select model type:')
        self.model_type_select = QComboBox()

        self.model_variant_label = QLabel('Select model variant:')
        self.model_variant_select = QComboBox()

        self.serial_number_label = QLabel('Enter first serial number:')
        self.serial_number_input = QLineEdit()

        self.qty_label = QLabel('Enter number of same devices to configure: (up to 24)')
        self.qty_input = QLineEdit()

        # Create options
        self.types = ["", "TOY18FIX600", "TOY18DAD400", "TOY18DAD600", "TOY18DAD800", "BABY18DAD400","BABY18DAD600", "BABY18DAD800"]
        self.variants = {
            "": [""],
            "TOY18FIX600": ["1EE0  (MO=TOY600, D2=HAM, EX)", "2EE0  (MO=TOY600, D2=HAM, EX)"],
            "TOY18DAD400": ["1BE0  (MO=TOY600, D2=HAM)", "2BE0  (MO=TOY600, D2=HAM)", "4BE0  (MO=TOY600, D2=HAM)", "SBE0  (MO=TOY600, D2=HAM)", "1EE0  (MO=TOY600, D2=HAM, EX)", "2EE0  (MO=TOY600, D2=HAM, EX)", "4EE0  (MO=TOY600, D2=HAM, EX)", "SEE0  (MO=TOY600, D2=HAM, EX)", "2BI0  (MO=TOY600, D2=HAM, OEM=INSTRUMENT SOLUTION)"],
            "TOY18DAD600": ["1BE0  (MO=TOY600, D2=HAM)", "2BE0  (MO=TOY600, D2=HAM)", "4BE0  (MO=TOY600, D2=HAM)", "SBE0  (MO=TOY600, D2=HAM)", "1EE0  (MO=TOY600, D2=HAM, EX)", "2EE0  (MO=TOY600, D2=HAM, EX)", "4EE0  (MO=TOY600, D2=HAM, EX)", "SEE0  (MO=TOY600, D2=HAM, EX)"],
            "TOY18DAD800": ["1BE0  (MO=TOY800, D2=HAM, TG)", "2BE0  (MO=TOY800, D2=HAM, TG)", "4BE0  (MO=TOY800, D2=HAM, TG)", "SBE0  (MO=TOY800, D2=HAM, TG)", "1EE0  (MO=TOY800, D2=HAM, TG, EX)", "2EE0  (MO=TOY800, D2=HAM, TG, EX)", "4EE0  (MO=TOY800, D2=HAM, TG, EX)", "SEE0  (MO=TOY800, D2=HAM, TG, EX)"],
            "BABY18DAD400": ["1BE0  (MO=TOY600, D2=S2D2)", "2BE0  (MO=TOY600, D2=S2D2)", "4BE0  (MO=TOY600, D2=S2D2)", "SBE0  (MO=TOY600, D2=S2D2)"],
            "BABY18DAD600": ["1BE0  (MO=TOY600, D2=S2D2)", "2BE0  (MO=TOY600, D2=S2D2)", "4BE0  (MO=TOY600, D2=S2D2)", "SBE0  (MO=TOY600, D2=S2D2)"],
            "BABY18DAD800": ["1BE0  (MO=TOY800, D2=S2D2, TG)", "2BE0  (MO=TOY800, D2=S2D2, TG)", "4BE0  (MO=TOY800, D2=S2D2, TG)", "SBE0  (MO=TOY800, D2=S2D2, TG"]
        }

        # Add options to widgets
        self.model_type_select.addItems(self.types)
        self.model_variant_select.addItems(self.variants)

        # Create checkboxes for required operations
        self.required_label = QLabel('Select required operations')
        self.default_checkbox = QCheckBox('Defaults')
        self.default_checkbox.setChecked(True)
        self.noise_checkbox = QCheckBox('Open Noise && Drift dialog')

        # Create button
        self.go_button = QPushButton('GO!')

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.instance_label)
        layout.addWidget(self.instance_input)
        layout.addWidget(self.model_type_label)
        layout.addWidget(self.model_type_select)
        layout.addWidget(self.model_variant_label)
        layout.addWidget(self.model_variant_select)
        layout.addWidget(self.serial_number_label)
        layout.addWidget(self.serial_number_input)
        layout.addWidget(self.qty_label)
        layout.addWidget(self.qty_input)
        layout.addWidget(self.required_label)
        layout.addWidget(self.default_checkbox)
        layout.addWidget(self.noise_checkbox)
        layout.addWidget(self.go_button)

        self.setLayout(layout)

        # Connect button click event and select change event and to a function
        self.go_button.clicked.connect(self.on_click)
        self.model_type_select.currentTextChanged.connect(self.update_variant_options)

        # Set window properties
        self.setWindowTitle(NAME_AUTOFLASH + ' v' + VERSION_AUTOFLASH)
        self.setGeometry(100, 100, 400, 200)

    # Update list of variants based on selected type
    def update_variant_options(self):
        selected_type = self.model_type_select.currentText()
        self.model_variant_select.clear()
        self.model_variant_select.addItems(self.variants[selected_type])

    # Run main function after clicking GO button
    def on_click(self):
        # Get values entered by the user
        FIRST_INSTANCE = int(self.instance_input.text())
        type = self.model_type_select.currentText()
        variant = self.model_variant_select.currentText()
        FIRST_NUMBER = int(self.serial_number_input.text())
        QUANTITY = int(self.qty_input.text())

        # Loop for all same devices
        for i in range(QUANTITY):
            instance = FIRST_INSTANCE + i
            number = FIRST_NUMBER + i

            # Print status
            print(f'Starting Flash Service with instance: {instance}')

            # Specify the correct title of the "Flash Service" application window
            if instance == 1:
                app_title = f"ECOM Flash Service.*"
            else:
                app_title = f"-{instance}- ECOM Flash Service.*"

            # Connect to the application by its title
            app = Application(backend="uia").connect(title_re=app_title)

            # Access the main window of the application
            main_window = app.window(title_re=app_title)

            # Bring the main window into focus (activate it)
            main_window.set_focus()

            # Check for checked 'Defaults' to run Default Operations
            if self.default_checkbox.isChecked():
                
                # Print status
                print('Entering Default Operations')
                # Click 'Default Operations' if possible
                main_window.child_window(auto_id="2201", control_type="Button").click_input() if main_window.child_window(auto_id="2201", control_type="Button").exists() else None
                # Wait a second
                time.sleep(1)

                # Print status
                print('Setting AMY model...')
                # Click 'Set AMY model'
                main_window.child_window(auto_id="1054", control_type="Button").click_input()
                # Wait a second
                time.sleep(1)

                # Access the 'Set AMY model' window
                set_model_window = app.top_window()

                # Access the "Type" dropdown menu
                type_selection_menu = set_model_window.child_window(auto_id="5200", control_type="ComboBox")
                time.sleep(1)

                # Select model type
                type_selection_menu.click_input()
                time.sleep(1)
                type_selection_menu.child_window(title=type).click_input()
                time.sleep(1)

                # Access the "Variant" dropdown menu
                variant_selection_menu = set_model_window.child_window(auto_id="5201", control_type="ComboBox")
                time.sleep(1)
                
                # Select model variant
                variant_selection_menu.click_input()
                time.sleep(1)
                variant_selection_menu.child_window(title=variant).click_input()
                time.sleep(1)


                # Confirmation loop that breaks if no error
                while True:

                    # Click "OK" to confirm model
                    set_model_window.child_window(title="OK", control_type="Button").click_input()
                    # Wait 10 seconds
                    time.sleep(10)

                    # If error writing model appears, click OK and try again
                    error_writing_model = main_window.child_window(title="Error")
                    if error_writing_model.exists():
                        print('Error writing AMY model!')
                        time.sleep(1)
                        error_writing_model.child_window(title="OK", control_type="Button").click_input()
                        print('Trying again...')
                        time.sleep(1)
                    else:
                        print('Model selection successful!')
                        break

                # If message appears for directory creation, click OK and continue
                message_directory_created = main_window.child_window(title="Message")

                if message_directory_created.exists():
                    print('Directory created.')
                    message_directory_created.child_window(title="OK", control_type="Button").click_input()
                    time.sleep(1)
                else:
                    time.sleep(1)

                # Print status
                print('Loading default constants...')

                # Click 'Load default constants'
                main_window.child_window(auto_id="1032", control_type="Button").click_input()
                # Wait a second
                time.sleep(1)

                # Click OK to confirm defaults
                main_window.child_window(title="OK", control_type="Button").click_input()
                # Wait 10 seconds
                time.sleep(10)

                # Print status
                print('Assigning serial number...')

                # Click 'Assign serial number'
                main_window.child_window(auto_id="1031", control_type="Button").click_input()
                # Wait a second
                time.sleep(1)

                # Simulate typing SN
                main_window.child_window(auto_id="1602", control_type="Edit").type_keys(number)
                time.sleep(1)

                # Click OK
                main_window.child_window(title="OK", control_type="Button").click_input()
                time.sleep(1)

                # If warning or message appears, confirm and continue
                warning_directory = main_window.child_window(title="Warning")
                message_directory_created = main_window.child_window(title="Message")

                if warning_directory.exists():
                    print('Warning: Directory exists!')
                    main_window.child_window(title="Ano", control_type="Button").click_input()
                    time.sleep(1)
                elif message_directory_created.exists():
                    print('Directory created.')
                    message_directory_created.child_window(title="OK", control_type="Button").click_input()
                    time.sleep(1)
                else:
                    time.sleep(1)
                
                # Wait 10 seconds
                time.sleep(10)

                # Print status
                print('Setting CCD gain...')

                # Click 'Set CCD gain'
                main_window.child_window(auto_id="1036", control_type="Button").click_input()
                time.sleep(1)

                # Click OK to confirm 1x Gain (default)
                main_window.child_window(title="OK", control_type="Button").click_input()
                time.sleep(1)

                # If Warning appears for EX detector, confirm by clicking "Ano"
                warning_ex = main_window.child_window(title="Warning")

                if warning_ex.exists():
                    print('Warning: EX-detector')
                    main_window.child_window(title="Ano", control_type="Button").click_input()
                    time.sleep(1)
                else:
                    time.sleep(1)

                # Wait 5 seconds
                time.sleep(5)

                # Print status
                print('Setting main fuse...')

                # Click 'Set main fuse'
                main_window.child_window(auto_id="1037", control_type="Button").click_input()
                time.sleep(1)

                # Click OK to confirm 24 VDC (default)
                main_window.child_window(title="OK", control_type="Button").click_input()
                
                # Wait 5 seconds
                time.sleep(5)

                # Print status
                print('OK!')


            # Open Noise & Drift dialog if checked by user
            if self.noise_checkbox.isChecked():
                print("Record noise and drift...") 
                
                # Unlock FIX detector
                if type == "TOY18FIX600":
                    main_window.child_window(auto_id="1050", control_type="Button").click_input()
                    time.sleep(1)
                    warning_lock = main_window.child_window(title="Warning")
                    if warning_lock.exists():
                        print('Warning: Unlock the unit')
                        main_window.child_window(title="OK", control_type="Button").click_input()
                        time.sleep(1)

                # Navigate to NaD
                main_window.child_window(auto_id="2", control_type="Button").click_input() if main_window.child_window(auto_id="2", control_type="Button").exists() else None
                main_window.child_window(auto_id="2205").click_input()
                main_window.child_window(auto_id="1401").click_input()
                time.sleep(1)

                # Check if "SWITCH LAMP ON" Button is present, i.e., if LAMP is OFF
                lamp_off = main_window.child_window(control_type="Button", title="Switch lamp ON")

                if lamp_off.exists():
                    print("Lamp OFF!")
                    
                    # If the button is found, click OK to ignite the lamp
                    main_window.child_window(control_type="Button", title="OK").click_input()
                    print("Lamp IGNITION...")
                    # Wait for ignition
                    time.sleep(10)
                else:
                    print("Lamp is already ON. No action required.")
                    time.sleep(1)

def print_version():
    print(f"{NAME_AUTOFLASH} v{VERSION_AUTOFLASH}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--version':
        print_version()
        sys.exit(0)
    
    app = QApplication(sys.argv)
    window = AutomateFlashService()
    window.show()
    sys.exit(app.exec_())


