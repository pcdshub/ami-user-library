from qtpy import QtWidgets, QtCore
from typing import Any

import ami.graph_nodes as gn
import amitypes

from ami.flowchart.library.common import CtrlNode
from ami.flowchart.library.CalculatorWidget import sanitize_name
from ami.flowchart.library.PythonEditorWidget import PythonEditorWidget


class Filter(CtrlNode):
    """
    Calculate the centroid of a given array.
    Two methods are available:
    1. Image moments: calculate moments on the full image directly
    2. Moment on projection along the horizontal and vertical directions

    For all method a background is subtracted. The background by default is the average of 10x10
    pixels at the upper left and lower right corner. Make sure these area do not contain signal.

    TO DO: gaussian fit method

    """

    nodeName = "Filter_Test"

    def __init__(self, name):
        super().__init__(
            name,
            terminals={
                'input1': {'io': 'in', 'removable': True, 'ttype': Any, 'optional': False, 'group': None},
                'input2': {'io': 'in', 'removable': True, 'ttype': Any, 'optional': False, 'group': None},
                'output1': {'io': 'out', 'removable': True, 'ttype': Any, 'optional': False, 'group': None},
                'output2': {'io': 'out', 'removable': True, 'ttype': Any, 'optional': False, 'group': None},
            }
        )
    
    def display(self, topics, terms, addr, win, **kwargs):
        super().display(topics, terms, addr, win, **kwargs)
        pass

    def to_operation(self, **kwargs):
        proc = EventProcessor()
        text = self.values
        inputs = list(self.input_vars().values())
        outputs = list(self.output_vars())
        func = gen_filter_func()

        return gn.Map(name=self.name()+"_operation", **kwargs,
                      func=proc.on_event,
                      begin_run=proc.begin_run,
                      end_run=proc.end_run,
                      begin_step=proc.begin_step,
                      end_step=proc.end_step)



class FilterWidget(QtWidgets.QWidget):

    sigStateChanged = QtCore.Signal(object, object, object)

    def __init__(self, inputs, outputs):
        super().__init__()
        self.inputs = inputs
        self.outputs = outputs

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        
        # Input variables and widget
        self.variable_widget = QtWidgets.QWidget(parent=self)
        self.variable_layout = QtWidgets.QGridLayout()
        self.variables = []

        for _, term in self.inputs.items():
            self.variables.append(self.createButton(term, self.operatorClicked))

        row = 0
        col = 0
        for ii in range(0, len(self.inputs)):
            self.variable_layout.addWidget(self.variables[ii], row, col)
            if col < 3:
                col += 1
            else:
                col = 0
                row += 1

        self.variable_widget.setLayout(self.variable_layout)
        self.layout.addWidget(self.variable_widget)

        # Edit area
        self.lineEdit = QtWidgets.QLineEdit(parent=self)
        self.lineEdit.setPlaceholderText("Example: Input0 < 100")
        self.lineEdit.returnPressed.connect(self.print_filter_func)
        self.layout.addWidget(self.lineEdit)
        # self.layout.addWidget(QtWidgets.QPlainTextEdit(parent=self))
        # self.layout.addWidget(PythonEditorWidget(parent=self))
    

    def createButton(self, text, member, op=None):
        button = Button(parent=self, text=text)
        button.op = op
        button.clicked.connect(member)
        return button
    

    @QtCore.Slot()
    def operatorClicked(self):
        clickedButton = self.sender()
        if clickedButton.op:
            value = clickedButton.op
        else:
            value = clickedButton.text()

        widget = self.focusWidget()
        if isinstance(widget, QtWidgets.QLineEdit):
            widget.setText(widget.text() + value)
        elif isinstance(widget, QtWidgets.QPlainTextEdit):
            widget.setPlainText(widget.toPlainText() + value)
    
    @QtCore.Slot()
    def print_filter_func(self):
        func = gen_filter_func(self.lineEdit.text, self.inputs, self.outputs)
        print(func)


def gen_filter_func(text, inputs, outputs):
    filter_func = f"""
def func(*args, **kwargs):
\t({','.join(inputs)}) = args
\tif %s:
\t\treturn {','.join(outputs)}
"""
    filter_func += "\n\treturn %s" % (', '.join([str(None)]*len(outputs)))
    return filter_func


def sanitize_name(name, space=True):
    return name.translate(sanitizer_space if space else sanitizer)

sanitizer_space = str.maketrans(" .:|-", "_____")
sanitizer = str.maketrans(".:|-", "____")

class Button(QtWidgets.QToolButton):
    def __init__(self, parent=None, text=""):
        super().__init__(parent)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.setText(text)

    def sizeHint(self):
        size = super().sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size






if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    terms = {}
    
    terms[f'In.0'] = f'Input.0'

    widget = FilterWidget(terms, [])
    widget.show()
    sys.exit(app.exec_())



