from PySide2 import QtCore, QtWidgets, QtWebEngineWidgets
import sys,os
from string import Template
from jinja2 import Environment, FileSystemLoader
from ccpem_core import gui_ext

class MolecularBrowserNoServer(QtWebEngineWidgets.QWebEngineView):
    '''
    Class for molecular browser, does not require server.  Can not display 
    binary files (i.e. .mrc).
    '''
    def __init__(self, parent=None):
        super(MolecularBrowserNoServer, self).__init__(parent)
        self.setup_uglymol()
        self.set_html_template()

    def setup_uglymol(self):
        self.uglymol_path = os.path.join(os.path.dirname(gui_ext.__file__),'uglymol')
        self.template_html_dir = os.path.join(self.uglymol_path,'templates')

    def set_html_template(self):
        ENV = Environment(loader=FileSystemLoader(self.template_html_dir))
        base_html = os.path.join(self.template_html_dir,'devtest.html')
        self.jinja_template = ENV.get_template('devtest.html')

    def load_files(self,list_models):
        list_set_paths = []
        for mod in list_models:
            if os.path.isfile(mod):
                list_set_paths.append('"file://{}"'.format(mod))
        models_string = ','.join(list_set_paths)
        set_html = self.jinja_template.render(uglymol_loc=self.uglymol_path, models=models_string)
        self.setHtml(set_html,baseUrl = QtCore.QUrl().fromLocalFile(self.uglymol_path))
        



if __name__ == '__main__':
    #job data
    job_data_dir = "/Users/agnel/git/uglymol/data"
    #list of models to display
    list_models = [os.path.join(job_data_dir,'1mru.pdb')
                ,os.path.join(job_data_dir,'1mru.map')]

    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QWidget()
    win.setWindowTitle('QWebView Map Test')
    # Add layout
    layout = QtWidgets.QVBoxLayout()
    win.setLayout(layout)
#read base html
    uglyview = MolecularBrowserNoServer()
    uglyview.load_files(list_models)

    layout.addWidget(uglyview)

    win.show()
    app.exec_()


