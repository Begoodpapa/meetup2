"""This test library provides the necessary functionality to interface between the Robot test automation frame work
and the IPA2800 platform software. It is organized in several sub-libraries which implement base keywords in python.
Each keyword typically has its own documentation, describing input parameters which may be mandatory (Man.) and return values.
The test library documentation.

Mail reflector for technical discussion: DG.NET-A8-TA-Dev@nokia.com
Product Owner Team for IL test automation project: Juha Puonti (CPO) (Esp), Qiu Jun (Hz)

When reporting bugs or requesting new features, please use the ILMml Issue Track System:
https://jira.inside.nokiasiemensnetworks.com/browse/ILTA

==========================================
"""
import os.path
import sys
from types import MethodType, FunctionType
from ILRobotAPI import get_version
ROBOT_VERSION = get_version()

try:
    mod = __import__("version", globals())
    __version__ = mod.version
except:
    __version__ = "0.0.0"

class illibgen_common_lib:

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._keywords = self._scan_keywords()
        
    def get_common_version(self):
        """Returns the version of the underlying IL Library

        #developer_used
        """
        return __version__

    def get_keyword_names(self):
        return self._keywords.keys() + self._get_my_keywords()

    def __getattr__(self, name):
        try:
            return self._keywords[name]
        except KeyError:
            raise AttributeError

    def _get_my_keywords(self):
        return [ attr for attr in dir(self)
                 if not attr.startswith('_') and type(getattr(self, attr)) is MethodType ]

    def _scan_keywords(self):
        keywords = []
        basedir = os.path.dirname(os.path.abspath(__file__))
        for path in os.listdir(basedir):
            path = os.path.join(basedir, path)
            if os.path.isdir(path):
                empty_dir=self._check_empty_dir(path)
                if empty_dir:
                     continue
                keywords += self._scan_keywords_from_dir(path)
            elif path.endswith('.py') :
                keywords += self._scan_keywords_from_file(path)
        return dict([ (kw.__name__, kw) for kw in keywords ])

    def _scan_keywords_from_file(self, path):
        mod_name = os.path.splitext(os.path.basename(path))[0]
        return self._scan_keywords_from_module(mod_name)

    def _scan_keywords_from_dir(self, path):
        mod_name = os.path.basename(path)
        return self._scan_keywords_from_module(mod_name)

    def _scan_keywords_from_module(self, name):
        mod = __import__(name, globals())
        kws = [ getattr(mod, attr) for attr in dir(mod)
                if not attr.startswith('_') ]
        return [ kw for kw in kws if type(kw) in [MethodType, FunctionType] ]

    def _check_empty_dir(self,path):
        empty=True
        files=os.listdir(path)
        for file in files:
            if str(file).endswith("py"):
                empty=False
        if empty:
            self._remove_pyc_in_directory(path)
        return empty

    def _remove_pyc_in_directory(self,directory):
        if str(directory).endswith('.svn'):return
        paths = os.listdir(directory)
        for path in paths:
            path = os.path.join(directory, path)
            if os.path.isdir(path):
                self._remove_pyc_in_directory(path)
            elif str(path).endswith(".pyc"):
                os.remove(path)
        paths = os.listdir(directory)
        if len(paths)==0:
            os.rmdir(directory)


if __name__ == "__main__":
    mylib = illibgen_common_lib()
    print mylib.get_keyword_names()
