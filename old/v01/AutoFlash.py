import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QComboBox
from pywinauto import Application
import pywinauto.keyboard as keyboard
import time


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

        self.qty_label = QLabel('Enter number of same devices to configure: (up to 6)')
        self.qty_input = QLineEdit()

        # Create options
        self.types = ["TOY18DAD400", "TOY18DAD600", "TOY18DAD800"]
        self.variants = {
            "TOY18DAD400": ["1EE0  (MO=TOY600, D2=HAM, EX)", "2EE0  (MO=TOY600, D2=HAM, EX)", "4EE0  (MO=TOY600, D2=HAM, EX)", "SEE0  (MO=TOY600, D2=HAM, EX)"],
            "TOY18DAD600": ["1EE0  (MO=TOY600, D2=HAM, EX)", "2EE0  (MO=TOY600, D2=HAM, EX)", "4EE0  (MO=TOY600, D2=HAM, EX)", "SEE0  (MO=TOY600, D2=HAM, EX)"],
            "TOY18DAD800": ["1EE0  (MO=TOY800, D2=HAM, TG, EX)", "2EE0  (MO=TOY800, D2=HAM, TG, EX)", "4EE0  (MO=TOY800, D2=HAM, TG, EX)", "SEE0  (MO=TOY800, D2=HAM, TG, EX)"]
        }

        # Add options to widgets
        self.model_type_select.addItems(self.types)
        self.model_variant_select.addItems(self.variants)

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
        layout.addWidget(self.go_button)

        self.setLayout(layout)

        # Connect button click event and select change event and to a function
        self.go_button.clicked.connect(self.on_click)
        self.model_type_select.currentTextChanged.connect(self.update_variant_options)

        # Set window properties
        self.setWindowTitle('Automate Flash Service v0.1')
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
                app_title = f"ECOM Flash Service v5.41 (zvoljml)"
            else:
                app_title = f"-{instance}- ECOM Flash Service v5.41 (zvoljml)"

            # Connect to the application by its title
            app = Application(backend="uia").connect(title=app_title)

            # Access the main window of the application
            main_window = app.window(title=app_title)

            # Bring the main window into focus (activate it)
            main_window.set_focus()

            # Print status
            print('Setting AMY model...')

            # Send "A" key to enter Default operations
            main_window.type_keys("a")
            time.sleep(1)

            # Simulate pressing key "0" to Set AMY model
            keyboard.send_keys("0")
            time.sleep(1)

            # Access the Set model window
            set_model_window = app.top_window()

            # Access the "Model selection" dropdown menu
            type_selection_menu = set_model_window.child_window(title="Model selection", control_type="ComboBox", found_index=0)

            # Click on the dropdown menu to open it
            type_selection_menu.click_input()
            time.sleep(1)

            # Select model type
            type_selection_menu.select(type)
            time.sleep(1)

            # Access the second dropdown menu (index 1)
            variant_selection_menu = set_model_window.child_window(title="Model selection", control_type="ComboBox", found_index=1)

            # Click on the second dropdown menu to open it
            variant_selection_menu.click_input()
            time.sleep(1)

            # Click model variant
            variant_selection_menu.child_window(title=variant, control_type="ListItem").click_input()
            time.sleep(1)

            # Send Enter to confirm model
            keyboard.send_keys("{ENTER}")
            # Wait 10 seconds
            time.sleep(10)

            # Print status
            print('Loading default constants...')

            # Simulate pressing key "1" to Load defaults
            keyboard.send_keys("1")
            time.sleep(1)

            # Send Enter to confirm defaults
            keyboard.send_keys("{ENTER}")
            # Wait 10 seconds
            time.sleep(10)

            # Print status
            print('Assigning serial number...')

            # Simulate pressing key "2" to Assign SN
            keyboard.send_keys("2")
            time.sleep(1)

            # Simulate typing SN
            app.top_window().child_window(control_type="Edit", found_index=1).type_keys(number)
            time.sleep(1)

            # Send Enter to confirm SN
            keyboard.send_keys("{ENTER}")
            time.sleep(1)

            # Send Enter to confirm warning
            keyboard.send_keys("{ENTER}")
            # Wait 10 seconds
            time.sleep(10)

            # Print status
            print('Setting CCD gain...')

            # Simulate pressing key "5" to Set CCD gain
            keyboard.send_keys("5")
            time.sleep(1)

            # Send Enter to confirm 1x Gain (default)
            keyboard.send_keys("{ENTER}")
            # Wait 5 seconds
            time.sleep(5)

            # Print status
            print('Setting main fuse...')

            # Simulate pressing key "8" to Set main fuse
            keyboard.send_keys("8")
            time.sleep(1)

            # Send Enter to confirm 24 VDC (default)
            keyboard.send_keys("{ENTER}")
            # Wait 5 seconds
            time.sleep(5)

            # Print status
            print('OK!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutomateFlashService()
    window.show()
    sys.exit(app.exec_())


