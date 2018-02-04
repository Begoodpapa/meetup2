from  unittest import defaultTestLoader, TestLoader
from  unittest import TestSuite, TextTestRunner, TestCase
import os

import re
import sys
import time
import cStringIO
#import support
import optparse
import cProfile

BASEDIR = os.path.dirname(os.path.abspath(__file__))

def get_sublibs(keyword_library_name, lib, mod):
    kwl = []
    for handler in lib.handlers.values():
#        print handler.longname
        if handler.name == "Get Keyword Names" or not handler.longname.startswith(keyword_library_name):
#            print "Ignoring '%s' in module '%s'" % (handler.name, handler.longname)
            continue
        kwl.append(handler._method)
    return kwl

def get_files(basedir):
    sys.path.insert(0, basedir)
    files = [ ]
    filelist = [ name for name in os.listdir(basedir) if name != ".svn" ]
    for name in filelist:
        absname = os.path.abspath(os.path.join(basedir, name))
        if os.path.isdir(absname):
            files += get_files(absname)
        if os.path.isfile(absname) and name.startswith("test_") and name.endswith(".py"):
            files += [ absname ]
    return files

class IlTestLoader(TestLoader):

    def __init__(self, exclude_long_runners):
        self.exclude_long_runners = exclude_long_runners

    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass
        """
#        print 'getTestCaseNames %s\n' % str(testCaseClass)
        def isTestMethod(attrname, testCaseClass=testCaseClass, prefix=self.testMethodPrefix):
            isTestMethod = attrname.startswith(prefix)
            if not isTestMethod:
                return False
            test_method = getattr(testCaseClass, attrname)
            isTestMethod = callable(getattr(testCaseClass, attrname))
            if not isTestMethod:
                return False
            if self.exclude_long_runners:
                try:
                    method_doc = test_method.__doc__
                    if 'long runner' in method_doc:
                        return False
                except KeyboardInterrupt:
                    raise
                except:
                    return True
            else:
                return True

        testFnNames = filter(isTestMethod, dir(testCaseClass))
        for baseclass in testCaseClass.__bases__:
            for testFnName in self.getTestCaseNames(baseclass):
                if testFnName not in testFnNames:  # handle overridden methods
                    testFnNames.append(testFnName)
        if self.sortTestMethodsUsing:
            testFnNames.sort(self.sortTestMethodsUsing)
#        print testFnNames
        return testFnNames

def get_tests(basedir, filelist,exclude_long_runner_flag):
    if len(filelist) == 0:
        files = get_files(basedir)
    else:
        files = []
        for name in filelist:
            absname = os.path.abspath(os.path.join(basedir, name))
            if os.path.isdir(absname):
                files += get_files(absname)
            elif os.path.isfile(absname):
                if os.path.split(absname)[1].startswith("test_") and os.path.split(absname)[1].endswith(".py"):
                    sys.path.insert(0, os.path.split(absname)[0])
                    files += [ absname ]
                else:
                    print "File '%s' does not match the nameing rules (test_*.py) -- parameter ignored" % (name)
            else:
                print "File/Directory '%s' does not exist -- parameter ignored" % (name)
    modules = []
    loading_problem = 0
    for file in files:
        module_name = os.path.splitext(os.path.split(file)[1])[0]
        module = __import__(module_name,globals())
        if module not in modules:
            modules.append(module)
        else:
            sys.stderr.write("Trying to import module %s twice, some tests will not be executed\n"%module_name)
            sys.stderr.write("ERROR: unit test fails because of duplicate import\n")
            loading_problem = 1
    testLoader = IlTestLoader(exclude_long_runner_flag)
    tests = [ testLoader.loadTestsFromModule(mod) for mod in modules ]
#    print tests
    return tests, loading_problem


def run_tests(tests, verbose=False):
    suite = TestSuite(tests)
    verbosity = verbose and 2 or 0
    result = TextTestRunner(verbosity=verbosity).run(suite)
    rc = len(result.failures) + len(result.errors)
    if rc > 200:
        rc = 200
    return rc

def unittest_exit(rc):
    print "\nunit tests completed with return code %s" % rc
    time.sleep(1)
    sys.exit(rc)


def print_untested_keywords(keyword_library_name, f, entries, kwl):
    # create dictionaries for ease of checking
    kw_dict = {}
    for kw in kwl:
        kw_dict[kw.func_code] = kw
    entry_dict = {}
    for entry in entries:
        entry_dict[entry.code] = entry

    untested_kws = {}
    number_untested_kws = 0
    for kw in kwl:
        try:
            # check if keyword function has been called
            x = entry_dict[kw.func_code]
        except KeyError:
            path = kw.func_code.co_filename

            # compute library and file name
            if not 'src' in path:
                # some files are reported with relative path, others with absolute path
                path = os.path.join('src',path)
                path = os.path.normpath(path)
            path_list = list(os.path.split(path))
#            sys.stderr.write("\n%s\n"%str(path_list))
            source_file = os.path.splitext(path_list[1])[0]
            python_library_name = ''
            path_list = os.path.split(path_list[0])
            while 'src' in path_list[0]:
                if python_library_name:
                    python_library_name = path_list[1] + '.' + python_library_name
                else:
                    python_library_name = path_list[1]
                path_list = os.path.split(path_list[0])

            number_untested_kws += 1
            kw_output = kw.__name__
            if not kw.__doc__:
                kw_output += ' (NO DOC STRING)'
            else:
                if 'deprecated' in kw.__doc__.lower():
                    kw_output += ' (DEPRECATED)'
            try:
                untested_kws[python_library_name].append((source_file, kw_output))
            except KeyError:
                untested_kws[python_library_name] = [(source_file, kw_output)]

#    print untested_kws
    sorted_keys = untested_kws.keys()
    sorted_keys.sort()
    f.write("\n================================================================================\n" )
    f.write("%s untested KWs out of total %s KWs in %s\n" % (number_untested_kws, len(kwl), keyword_library_name))
    f.write("================================================================================\n\n" )
    print "%s untested KWs out of total %s KWs in %s\n" % (number_untested_kws, len(kwl), keyword_library_name)
    for key in sorted_keys:
        module_kwl = untested_kws[key]
        module_kwl.sort()
#        print "%s keywords in %s" % (len(module_kwl), key)
        f.write("%s keywords in %s\n" % (len(module_kwl), key))
        old_file =""
        for file, kw in module_kwl:
            if old_file != file:
                old_file = file
#                print "\t", file
                f.write("\t%s\n"% file)
#            print "\t\t", kw
            f.write("\t\t%s\n"% kw)
#            print "\t%s\t%s"%(file, kw)
        f.write("\n" )
#    print "%s untested KWs out of total %s KWs" % (number_untested_kws, len(kwl))

if __name__ == '__main__':
    usage = """usage: python %prog [options] [<directories or files to examine>]"""
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,\
                      help="enables more output by TextTestRunner")
    parser.add_option("--stdout","-s", action="store_true", dest="stdout_flag", default=False, \
                      help="enables standard output (normally suppressed)")
    parser.add_option("--profile","-p", action="store_true", dest="profile_flag", default=False, \
                      help="runs the profiler and creates a statistic about keywords that are not called during unit test")
    parser.add_option("--exclude","-x", action="store_true", dest="exclude_long_runner_flag", default=False, \
                      help="exclude long running test cases from the test run")
    options, arguments = parser.parse_args()

    stdout_orig = sys.stdout
    if not options.stdout_flag:
        print "stdout suppressed, enable via --stdout or -s\n"
        sys.stdout = cStringIO.StringIO()
        sys.__stdout__ = sys.stdout

    # import Robot only after disabling stdout
    from robot.running import TestLibrary
    sys.path.insert(0, os.path.join(BASEDIR, '..', 'src'))

    tests, loading_problem = get_tests(BASEDIR, arguments, options.exclude_long_runner_flag)

    if not options.profile_flag:
        # run tests without profiler and exit
        rc = run_tests(tests, options.verbose)
        rc = rc or loading_problem
        unittest_exit(rc)

    profile = cProfile.Profile()
    # run tests with profiler
    rc = profile.runcall(run_tests,tests,options.verbose)
    rc = rc or loading_problem

    # re-enable stdout
    sys.stdout = stdout_orig
    sys.__stdout__ = sys.stdout

    entries = profile.getstats()
#    print type(entries[0]), dir(entries[0])
#    print type(entries[0].code), dir(entries[0].code)


    librarynames = [ "comm", "domain_cm", "domain_sig", "domain_tt", "domain_dc"]

    f = open(os.path.join(BASEDIR,'kw_profile.txt'),'w')

    for keyword_library_name in librarynames:
        library = TestLibrary(keyword_library_name)
        mod = __import__(keyword_library_name, globals())
        kwl = get_sublibs(keyword_library_name, library, mod)
        print_untested_keywords(keyword_library_name, f, entries, kwl)

    f.close()
    unittest_exit(rc)

from comm.communication import connections
from comm.communication.connections import  mock
import comm

class ExtendedExceptionTest(TestCase):

    def failIfNotRaises(self, excClass, excStr, callableObj, *args, **kwargs):
        """similar to assertRaises in unittest.TestCase base class.
        There is one additional parameter excStr.
        This string is checked for equality against the string that is included in the exception """
        try:
            callableObj(*args, **kwargs)
        except excClass:
            type, value, traceback = sys.exc_info()
            self.assertEquals(str(value),excStr)
            return
        else:
            if hasattr(excClass,'__name__'): excName = excClass.__name__
            else: excName = str(excClass)
            raise self.failureException, "%s not raised" % excName


class BaseTestCase(ExtendedExceptionTest):
    """ This class serves two purposes:

1) It allows to overwrite the mml connection so that keyword methods that use mml communication can be unit tested.
The subclass has to define a setUp method like

    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(units_output.io_normal_1,"ZIHI::WDU,00;")
        self.add_mml_response(units_output.io_normal_2,"ZIHI::WDU,00;")
        self.add_mml_response(units_output.io_other)

It is essential that the BaseTestCase.setUp(self) is called in the setUp of the derived class.
In the above example the "mml connection" will return units_output.io_normal_1 for the first
ZIHI::WDU,00; command and units_output.io_normal_2 for all subsequent ZIHI::WDU,00; commands.
For all other commands it will return units_output.io_other
These return values are string objects containing the mml output.

If the derived class uses a tearDown(self) method it must also call BaseTestCase.tearDown(self)

2) It offers another assert method "failIfNotRaises" that allows to check the exception string that was raised by a test method.
"""
    def setUp(self):
        """ overwrite the mml connection and clear dictionary of command responses"""
        # clear the dictionary of command responses
        self.mml_responses = {}
        mock.start_mock()

        # reset ste
        current = connections.get_current_connection_obj()
        current.ste_mode = None
        current.ste_unit = None
        current.ste_count = 0

        # note , add default this command response
#        self.add_mml_response("""# echo $?
#        0
#        ""","echo $?")

    def add_mml_response(self, command_response, command_input = ""):
        """ add an mml response to the dictionary of responses
        If command_input is specied the response will be used for the specific command
        If command_input is omitted the response will be used for all commands not specified in this dictionary
        If several reponses are configured for the same command_input they will be used one after the other.
        The last response of a command_input will be used for all subsequent calls with command_input
        """
        if not self.mml_responses.has_key(command_input):
            self.mml_responses[command_input]=[]
        self.mml_responses[command_input].append(command_response)

    def mml_responses_completed(self):
        mock.set_mml_responses(self.mml_responses)

    def tearDown(self):
        """ restore the original mml connection """
        mock.finish_mock()


class LowLevelTestcase(ExtendedExceptionTest):

    def setUp(self):
        """ overwrite the mml connection and clear dictionary of command responses"""
        # clear the dictionary of command responses
        self.replay = common.Replay()
        self.replay.start_unittest()
        # reset ste
        current = connections.get_current_connection_obj()
        current.ste_mode = None
        current.ste_unit = None
        current.ste_count = 0

    def add_response(self, response):
        self.replay.add_response(response)

    def tearDown(self):
        """ restore the original mml connection """
        self.replay.end_unittest()


