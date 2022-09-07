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
    fig, axes = plot_single_empty_graph()
    # Получение экземпляра класса холста с размещенным рисунком
    canvas = MyMplCanavas(fig)
    # Добавление виджета холста с рисунком в размещение
    layout.addWidget(canvas)
    # Добавление навигационной панели с привязкой к созданному холсту с рисунком Matplotlib
    toolbar = NavigationToolbar2QT(canvas, layout.parent())
    layout.addWidget(toolbar)
    return canvas, toolbar

def plot_single_empty_graph():
    '''
    Функция для подготовки рисунка с пустыми осями и предварительного их оформления, без задания данных
    '''
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 7), dpi=85, facecolor='white', frameon=True, edgecolor='black', linewidth=1)
    fig.subplots_adjust(wspace=0.4, hspace=0.6, left=0.15, right=0.85, top=0.9, bottom=0.1)
    axes.grid(True, c='lightgrey', alpha=0.5)
    axes.set_title('Заголовок диаграммы рассеяния', fontsize=10)
    axes.set_xlabel('X', fontsize=8)
    axes.set_ylabel('Y', fontsize=8)
    return fig, axes

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableView
from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QLabel, QSpinBox


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from las import CurveSet

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


class MainWindow(QMainWindow):
    
    current_set = None
        
    def __init__(self):
        super().__init__()
        
        def plot_curve():
               x_index = None
               y_index = None
               for i in range(len(self.current_set.curves_list)):
                   if self.current_set.curves_list[i] == 'GZ5':
                       x_index = i
                   if self.current_set.curves_list[i] == 'DEPT':
                       y_index = i
                                     
               fig, ax = plt.subplots(1,1)
               x = self.current_set.curves_data[x_index]
               y = self.current_set.curves_data[y_index]
               ax.plot(x, y)
               plt.show()
               
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
        
        self.lButtonsPanel.add_button(plot_curve, 'plot chosen')

        # Preparation foundation for matplotlib widget
        self.mplWidget = QWidget()
        self.companovka_for_mpl = QVBoxLayout(self.mplWidget)
        self.CentrLayout.addWidget(self.mplWidget)
        canvas, toolbar = prepare_abstract_canvas_and_toolbar(layout=self.companovka_for_mpl)
        
        las_path = './las_test/115_БКЗ.las'
        self.current_set = CurveSet(las_path)
        
        self.expl_field.add_text(str(self.current_set.curves_list))
        self.lButtonsPanel.add_combobox(self.current_set.curves_list, 'methods combo')
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())