import sys, os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox, QComboBox, QSlider, QLabel
import csv


class audioFile:
    def __init__(self):
        self.sample_rate = ["8k", "11k", "16k", "22k", "32k", "37k", "44k"]
        self.volume_boost = range(0, 100, 1)
        self.filter = ["None", "Low-pass", "Highpass", "Band-pass", "All-pass"]
        self.bit_depth = ["4 bit", "8-bit", "11-bit", "12-bit", "16-bit", "18-bit", "20-bit", "24-bit", "28-bit",
                          "32-bit"]
        self.compression = ["None", "Lossy", "Lossless"]
        self.audio_type = "Song"
        self.filename = "string name"
        self.output_folder = ""

        # generate a string that is formatted for asm include
        self.asm_str = "#incasmlabel(" + self.filename + ", \"" + self.filename + "." + self.audio_type + ".inc\", 2)"
        # example string:  incasmlabel(swish, "audio/wip/assets/sfx/swish/swish.song.inc", 2)

#This code defines a new class called App which is a subclass of the QMainWindow class from the PyQt5.QtWidgets module. The __init__ method is the constructor for the class and is automatically called when an instance of the class is created.
class App(QtWidgets.QMainWindow):
    def __init__(self):
#This line calls the __init__ method of the parent QMainWindow class to ensure that all necessary initializations are done.
        super().__init__()
#These lines set various properties of the main window, such as its title, size, and minimum size.
        self.setWindowTitle("HuTrack Conversion UI")
        self.setGeometry(800, 500, 800, 500)
        self.setMinimumSize(800, 200)
#This line defines a list table_headers which will be used as the headers for the table widget.
        self.table_headers = ['Remove', 'File', 'Output folder', 'Rate', 'Volume Adjust', 'Volume', 'Filter', 'Bits', 'Compression', 'ASM Include Snippit', 'Option', 'Value']
#This line defines an empty list table_data which will be used to store the data that will be displayed in the table widget.
        self.table_data = []
#This line creates an instance of the QTableWidget class and assigns it to the table attribute of the App class. The self argument is passed to indicate that the table widget is a child of the main window.
        self.table = QtWidgets.QTableWidget(self)
#These lines set the number of columns in the table widget and set the labels for the horizontal headers.
        self.table.setColumnCount(len(self.table_headers))
        self.table.setHorizontalHeaderLabels(self.table_headers)
#This line sets the selection behavior of the table widget so that entire rows are selected when the user clicks on a cell.
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
#This line sets the resize mode for the horizontal headers so that they are resized to fit the contents.
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
#These lines set the default alignment for the horizontal headers to be left-aligned and make the vertical headers invisible.
        self.table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        self.table.verticalHeader().setVisible(False)
#TThe line self.table.cellClicked.connect(self.cell_clicked) connects the cellClicked signal from the table widget to the cell_clicked method. The cellClicked signal is emitted when a cell in the table is clicked. This means that when a cell in the table is clicked, the cell_clicked method will be called.
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.cellClicked.connect(self.cell_clicked)
#These lines create a QPushButton instance with the label "Browse for .dmf or .wav files", connect the button's clicked signal to the browse_files method, and move the button to the position (10, 10) within the main window.
        self.browse_button = QtWidgets.QPushButton("Browse for .dmf or .wav files", self)
        self.browse_button.clicked.connect(self.browse_files)
        self.browse_button.move(10, 10)
#These lines create another QPushButton instance with the label "Browse for output folder", connect the button's clicked signal to the output_folder method, and move the button to the position (10, 50) within the main window.
        self.output_folder_browse = QtWidgets.QPushButton("Browse for output folder", self)
        self.output_folder_browse.clicked.connect(self.output_folder)
        self.output_folder_browse.move(10, 50)
#These lines create a QPushButton instance with the label "Convert", connect the button's clicked signal to the convert method, and move the button to the position (500, 50) within the main window.
        self.convert_button = QtWidgets.QPushButton("Convert", self)
        self.convert_button.clicked.connect(self.convert)
        self.convert_button.move(500, 50)
#These lines create a QPushButton instance with the label "Export to CSV", connect the button's clicked signal to the export_to_csv method, and move the button to the position (300, 50) within the main window.
        self.export_csv_button = QtWidgets.QPushButton("Export to CSV", self)
        self.export_csv_button.clicked.connect(self.export_to_csv)
        self.export_csv_button.move(300, 50)
#These lines create a QPushButton instance with the label "Clear", connect the button's clicked signal to the clear method, and move the button to the position (650, 50) within the main window.
        self.clear_button = QtWidgets.QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear)
        self.clear_button.move(650, 50)
#This line creates an instance of the status bar and assigns it to the status_bar attribute of the App class.
        self.status_bar = self.statusBar()
#These lines create a QHBoxLayout instance and add the browse_button and output_folder_browse buttons to the layout.
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.browse_button)
        button_layout.addWidget(self.output_folder_browse)
#These lines create a QVBoxLayout instance, add the button_layout to the QVBoxLayout, set the contents margins of the QVBoxLayout to 0, and set the spacing between widgets in the layout to 0.
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(button_layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
#This line sets the size policy of the table widget to be expanding in both the horizontal and vertical directions.
        self.table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
#These lines add the table widget, convert_button, export_csv_button, and clear_button to the QVBoxLayout.
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.convert_button)
        self.layout.addWidget(self.export_csv_button)
        self.layout.addWidget(self.clear_button)
#These lines create a QWidget instance, set its layout to be the QVBoxLayout, and assign the widget to the widget attribute of the App class.
        self.widget = QtWidgets.QWidget(self)
        self.widget.setLayout(self.layout)
#This line sets the central widget of the main window to be the QWidget instance created earlier.
        self.setCentralWidget(self.widget)
# This function allows the user to browse and select multiple files from their computer
    def browse_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        settings = QSettings("Your Company", "Your Application")
        default_dir = settings.value("default_dir", "")

        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", default_dir,
                                                "All Files (*);;WAV Files (*.wav);;DMF Files (*.dmf)", options=options)
        if files:
                for file in files:
                # Check if file is already in the table
                        already_added = False
                        file_name = os.path.basename(file).split(".")[0]
                        for audio_file in self.table_data:
                                if file_name == audio_file.filename:
                                        already_added = True
                                        break
                        if not already_added:
                                audio_file = audioFile()
                                audio_file.filename = file_name
                                self.table_data.append(audio_file)

                self.table.setRowCount(len(self.table_data))
                self.update_table()

        # Save the directory of the selected file for next time
        settings.setValue("default_dir", os.path.dirname(files[0]))



    def output_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        folder = QFileDialog.getExistingDirectory(self, "QFileDialog.getExistingDirectory()", options=options)
        if folder:
            for audio_file in self.table_data:
                audio_file.output_folder = folder

            self.update_table()

    def convert(self):
        for audio_file in self.table_data:
            if audio_file.filename == "string name":
                self.status_bar.showMessage("Please select a file")
                return

            if audio_file.output_folder == "":
                self.status_bar.showMessage("Please select an output folder")
                return

            self.status_bar.showMessage("Converting " + audio_file.filename + "...")

            # Conversion logic here

            self.status_bar.showMessage("Finished converting " + audio_file.filename + ".")

    def clear(self):
        self.table_data.clear()
        self.table.setRowCount(0)
        self.status_bar.showMessage("Cleared table.")

    def update_table(self):#add subtract button Feb13 234pm pt
        for i, audio_file in enumerate(self.table_data):
            remove_button = QtWidgets.QPushButton("-")
            remove_button.clicked.connect(lambda row=i: self.remove_row(row))
            self.table.setCellWidget(i, 0, remove_button)

            self.table.setItem(i, 1, QTableWidgetItem(audio_file.filename))
            self.table.setItem(i, 2, QTableWidgetItem(audio_file.output_folder))

            combo_box = QComboBox()
            combo_box.addItems(audio_file.sample_rate)
            self.table.setCellWidget(i, 3, combo_box)

            slider = QSlider(QtCore.Qt.Horizontal)
            slider.setRange(-100, 100)
            slider.setValue(0)
            self.table.setCellWidget(i, 4, slider)

            label = QLabel(str(slider.value()))
            self.table.setCellWidget(i, 5, label)
            slider.valueChanged.connect(lambda value, label=label: label.setText(str(value)))

            combo_box = QComboBox()
            combo_box.addItems(audio_file.filter)
            self.table.setCellWidget(i, 6, combo_box)

            combo_box = QComboBox()
            combo_box.addItems(audio_file.bit_depth)
            self.table.setCellWidget(i, 7, combo_box)

            combo_box = QComboBox()
            combo_box.addItems(audio_file.compression)
            self.table.setCellWidget(i, 8, combo_box)

            self.table.setItem(i, 9, QTableWidgetItem(audio_file.asm_str))

    def remove_row(self, row):
        self.table.removeRow(row)
        self.table_data.pop(row)
#end update

    def cell_clicked(self, row, col):
        if col == 7:
            QMessageBox.information(self, "ASM Include Snippit", self.table.item(row, col).text())

    def convert(self):
        for audio_file in self.table_data:
            if audio_file.filename == "string name":
                self.status_bar.showMessage("Please select a file")
                return

            if audio_file.output_folder == "":
                self.status_bar.showMessage("Please select an output folder")
                return

            self.status_bar.showMessage("Converting " + audio_file.filename + "...")

            # Conversion logic here

            self.status_bar.showMessage("Finished converting " + audio_file.filename + ".")

            # Write data to a CSV file
            with open('output.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['File', 'Output folder', 'Rate', 'Volume Boost', 'Filter', 'Bits', 'Compression', 'ASM Include Snippit', 'Option', 'Value'])
                for audio_file in self.table_data:
                    writer.writerow([audio_file.filename, audio_file.output_folder, audio_file.sample_rate, audio_file.volume_boost, audio_file.filter, audio_file.bit_depth, audio_file.compression, audio_file.asm_str])


    def export_to_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                    "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.table_headers[1:]) # exclude the remove column from the headers
                for i in range(self.table.rowCount()):
                    row = []
                    for j in range(1, self.table.columnCount()): # exclude the remove column from the data
                        item = self.table.item(i, j)
                        if item is not None:
                            row.append(item.text())
                        else:
                            widget = self.table.cellWidget(i, j)
                            if isinstance(widget, QComboBox):
                                row.append(widget.currentText())
                            elif isinstance(widget, QSlider):
                                row.append(widget.value())
                            else:
                                row.append('')
                    writer.writerow(row)
            self.status_bar.showMessage("Exported to CSV successfully.")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
