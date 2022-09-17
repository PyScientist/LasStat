import sys
import time


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT


class MyMplCanavas(FigureCanvasQTAgg):
    '''
    Класс холста Qt для помещения рисунка Matplotlib!
    '''
    def __init__(self, fig):
        super().__init__(fig)
        self.setMinimumSize(200,200)


def prepare_abstract_canvas_and_toolbar(layout = None):
    """
    Функция для инициализации рисунка Matplotlib и его размещения в виджете Qt, добавления панели навигаии
    """
    # Подготовка рисунка и осей
    elem_dict = {}
    elem_dict['fig'], elem_dict['ax'] = plot_single_empty_graph()
    # Получение экземпляра класса холста с размещенным рисунком
    elem_dict['can'] = MyMplCanavas(elem_dict['fig'])
    # Добавление виджета холста с рисунком в размещение
    layout.addWidget(elem_dict['can'])
    # Добавление навигационной панели с привязкой к созданному холсту с рисунком Matplotlib
    toolbar = NavigationToolbar2QT(elem_dict['can'], layout.parent())
    layout.addWidget(toolbar)
   
    return elem_dict

def plot_single_empty_graph():
    """
    Функция для подготовки рисунка с пустыми осями и предварительного их оформления, без задания данных
    """
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 30), dpi=85, facecolor='white', frameon=True, edgecolor='black', linewidth=1)
    fig.subplots_adjust(wspace=0.4, hspace=0.6, left=0.15, right=0.85, top=0.9, bottom=0.1)
    axes.grid(True, c='lightgrey', alpha=0.5)
    axes.set_title('Title', fontsize=10)
    axes.set_xlabel('X', fontsize=20)
    axes.set_ylabel('Y', fontsize=20)
    return fig, axes

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableView
from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QLabel, QSpinBox


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from las import CurveSet, PropertiesDict

from matplotlib import pyplot as plt

class ExplanationField:
    """ExplanationField class"""

    def __init__(self, host):
        self.host = host
        # Create widget and vertical layout for
        # explanation information
        self.expl_widget = QWidget()
        self.container = QVBoxLayout()
        self.expl_widget.setLayout(self.container)
        self.textField = QTextEdit()
        self.container.addWidget(self.textField)

    def set_text(self, text):
        """Inserting text to text field"""
        self.textField.setText(text)

    def add_text(self, text):
        """Adding text to text field"""
        self.textField.append(text)

    def clear_text(self):
        """Clear text in explanation field"""
        self.textField.clear()


class LButton:
    """Button for lower panel"""

    def __init__(self, action, text):
        # Create font object and set and customize it
        font = QtGui.QFont()
        font.setPixelSize(50)
        # Create button and set font to it
        self.button = QPushButton(text)
        self.button.setFont(font)
        self.button.clicked.connect(action)


class LSpin:
    def __init__(self, default_value, name):
        self.spinbox = QSpinBox()
        self.spinbox.setRange(0, 1000)
        self.spinbox.setValue(default_value)
        self.spinbox.setObjectName(name)


class MethodCombobox:
    def __init__(self, values, name):
        self.combobox_methods = QComboBox()
        self.combobox_methods.addItems(values)
        self.combobox_methods.setObjectName(name)


class LowerButtonsPanel:
    """Lower panel class"""

    def __init__(self, host):
        self.host = host
        # Create widget and horizontal layout for
        # lower panel for buttons which operate views
        self.buttons_widget = QWidget()
        self.container = QHBoxLayout()
        self.buttons_widget.setLayout(self.container)

    def add_combobox(self, values, name):
        """"Add combobox with values"""
        self.container.addWidget(MethodCombobox(values, name).combobox_methods)

    def add_button(self, action, text):
        """Add button to panel with action and text"""
        self.container.addWidget(LButton(action=action, text=text).button)

    def read_combobox_methods(self, name):
        """Got current text from methods combobox"""
        combobox = self.buttons_widget.findChild(QComboBox, name)
        return combobox.currentText()

class  CurveObject:
            def __init__(self, mainwindow):
                # Recive axes and figure objects
                self.axes, self.fig = mainwindow.MplCanavas['ax'], mainwindow.MplCanavas['fig']
                # Read mnemonic of curve to plot from combobox
                self.mnem = mainwindow.lButtonsPanel.read_combobox_methods('methods combo')
                x_index, y_index= None, None
                for i, curve in enumerate(mainwindow.current_set.curves_list):
                   if curve == self.mnem:
                       x_index = i
                   if curve == 'DEPT':
                       y_index = i
                # Obtain data and units of curve by indexes
                self.x_arr = mainwindow.current_set.curves_data[x_index]
                self.x_unit = mainwindow.current_set.units_list[x_index]
                self.x_color = mainwindow.current_set.curve_props_list[x_index]['color']
                self.y_arr = mainwindow.current_set.curves_data[y_index]
                self.y_unit = mainwindow.current_set.units_list[y_index]
                self.plot_data()  #plotting data
                                
            def  plot_data(self):
                """Prepare plot and make some adjustment"""
                self.axes.plot(self.x_arr, self.y_arr*(-1), color=self.x_color)
                self.axes.set_title('Plot cuves from las', fontsize=20)
                self.axes.set_xlabel(F'{self.mnem}, {self.x_unit} ', fontsize=20)
                self.axes.set_ylabel(F'Depth, {self.y_unit}', fontsize=20)
                # Redraw matplotlib canvas
                self.fig.canvas.draw()
            
            
class MainWindow(QMainWindow):
          
    def __init__(self):
        super().__init__()
        self.current_set = None
        self.curvesObj = None
        
        def plot_curve():
               """Plot selected curve"""
               self.curvesObj = CurveObject(self)
               
        def clear_ax():
                 """Clear axes from all information"""
                 self.MplCanavas['ax'].clear()
                 self.MplCanavas['fig'].canvas.draw()
               
               
        # Create widget and vertical layout.
        # Set layout to widget
        # Set widget as central widget of main window
        self.CentrWidg = QWidget()
        self.CentrLayout = QVBoxLayout()
        self.CentrWidg.setLayout(self.CentrLayout)
        self.setCentralWidget(self.CentrWidg)
        
        # Create explanation field and add it to central widget layout
        self.expl_field = ExplanationField(self)
        self.CentrLayout.addWidget(self.expl_field.expl_widget)
        
        # Create lower buttons panel (initially empty) and add it to central widget layout
        self.lButtonsPanel = LowerButtonsPanel(self)
        self.CentrLayout.addWidget(self.lButtonsPanel.buttons_widget)
        # Add button to plot single curve to the graph
        self.lButtonsPanel.add_button(plot_curve, 'plot chosen')
        self.lButtonsPanel.add_button(clear_ax, 'clear')
        # Preparation foundation for matplotlib widget
        self.mplWidget = QWidget()
        self.comp_for_mpl = QVBoxLayout(self.mplWidget)
        self.CentrLayout.addWidget(self.mplWidget)
        # Insert matplotlib drawing canvas to matplotlib layuot
        self.MplCanavas = prepare_abstract_canvas_and_toolbar(layout=self.comp_for_mpl)
                
        las_path = './las_test/115_БКЗ.las'
        properties_dict = PropertiesDict()
        self.current_set = CurveSet(las_path, properties_dict)
        
        self.expl_field.add_text('ready')
        self.lButtonsPanel.add_combobox(self.current_set.curves_list, 'methods combo')
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())