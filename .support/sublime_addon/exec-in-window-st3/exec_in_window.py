import sublime, sublime_plugin
import os, sys
import subprocess
import functools
import time
import os
import tempfile
import codecs
execplugin = __import__("Default.exec")
execcmd = execplugin.exec

class ExecInWindowAppendCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        data = kwargs.get( 'data', None )
        if data:
            self.view.insert( edit, self.view.size(), data )

class ExecInWindowClearViewCommand(sublime_plugin.TextCommand):
    def run(self, edit, user_input=None, *args):
        self.view.erase(edit, sublime.Region(0, self.view.size()))

class ExecInWindowCommand(execcmd.sublime_plugin.WindowCommand, execcmd.ProcessListener):
    def run(self, cmd = [], file_regex = "", line_regex = "", working_dir = "",
            encoding = "utf-8", env = {}, quiet = False, kill = False,
            # Catches "path" and "shell"
            **kwargs):

        if kill:
            if self.proc:
                self.proc.kill()
                self.proc = None
                self.append_data(None, "[Cancelled]")
            return

        self.post_command=env.get('post_command',None)

        # Create temporary file if doesn't exists
        #
        if self.window.active_view().file_name():
            self.file = self.window.active_view().file_name()
        else:
            self.file          = self.create_temp_file()
            cmd[cmd.index('')] = self.file

        # Default the to the current files directory if no working directory was given
        if (working_dir == "" and self.window.active_view() and self.file):
            working_dir = os.path.dirname(self.file)

        self.output_view = self.window.open_file(working_dir+"/BUILD_RESULT")
        self.output_view.set_scratch(True)
        self.output_view.set_read_only(False)

        self.output_view.settings().set("result_file_regex", file_regex)
        self.output_view.settings().set("result_line_regex", line_regex)
        self.output_view.settings().set("result_base_dir", working_dir)

        self.encoding = encoding
        self.quiet = quiet
        self.proc = None
        self.clear_view()
        # execcmd.sublime.set_timeout(functools.partial(self.clear_view), 0)
        if not self.quiet:
            print( "Running " + " ".join(cmd) )
            execcmd.sublime.status_message("Building")

        merged_env = env.copy()
        if self.window.active_view():
            user_env = self.window.active_view().settings().get('build_env')
            if user_env:
                merged_env.update(user_env)

        encodingEnv = {
            "PYTHONIOENCODING": "utf-8", 
            "LANG": "en_US.UTF-8"
        }
        
        merged_env.update( encodingEnv )

        # Change to the working dir, rather than spawning the process with it,
        # so that emitted working dir relative path names make sense
        if working_dir != "":
            os.chdir(working_dir)

        err_type = OSError
        if os.name == "nt":
            err_type = WindowsError

        try:
            # Forward kwargs to AsyncProcess
            self.proc = execcmd.AsyncProcess(cmd, False, merged_env, self, **kwargs)
        except err_type as e:
            self.append_data(None, str(e) + "\n")
            self.append_data(None, "[cmd:  " + str(cmd) + "]\n")
            self.append_data(None, "[dir:  " + str(os.getcwd()) + "]\n")
            if "PATH" in merged_env:
                self.append_data(None, "[path: " + str(merged_env["PATH"]) + "]\n")
            else:
                self.append_data(None, "[path: " + str(os.environ["PATH"]) + "]\n")
            if not self.quiet:
                self.append_data(None, "[Finished]")

    def is_enabled(self, kill = False):
        if kill:
            return hasattr(self, 'proc') and self.proc and self.proc.poll()
        else:
            return True

    def clear_view(self):
        self.output_view.run_command('exec_in_window_clear_view',{})

    def create_temp_file(self):
        view = self.window.active_view()
        region = execcmd.sublime.Region(0, view.size())
        content = view.substr(region)

        filename = '%s.tmp' % view.id()
        path = os.path.join(tempfile.gettempdir(), filename)
        file = open(path, 'w')
        # file.write(str(content.encode('utf-8')))
        file.write( content )
        file.close()
        return path

    def append_data(self, proc, data):
        if proc != self.proc:
            # a second call to exec has been made before the first one
            # finished, ignore it instead of intermingling the output.
            if proc:
                proc.kill()
            return
        try:
            if isinstance( data, str ):
                data = data.encode( self.encoding )
            string = data.decode(self.encoding)
        except Exception as e:
            string = "[Decode error - output not " + self.encoding + "]\n"
            proc = None

        # Normalize newlines, Sublime Text always uses a single \n separator
        # in memory.
        # string = string.replace('\r\n', '\n').replace('\r', '')
        string = string.replace('\r', '')

        selection_was_at_end = (len(self.output_view.sel()) == 1
            and self.output_view.sel()[0]
                == execcmd.sublime.Region(self.output_view.size()))

        self.output_view.run_command('exec_in_window_append',{ 'data': string })        
        if selection_was_at_end:
            self.output_view.show(self.output_view.size())

    def finish(self, proc):
        if not self.quiet:
            elapsed = time.time() - proc.start_time
            exit_code = proc.exit_code()
            if exit_code == 0 or exit_code == None:
                self.append_data(proc, ("\n[Execution Finished in %.1fs]\n") % (elapsed))
                if self.post_command:                
                    self.append_data(proc, ("\n[Post Command:%s]\n") % (self.post_command))
                    sublime.active_window().run_command(self.post_command)
            else:
                self.append_data(proc, ("\n[Finished in %.1fs with exit code %d]\n") % (elapsed, exit_code))

        if proc != self.proc:
            return

        errs = self.output_view.find_all_results()

        if len(errs) == 0:
            execcmd.sublime.status_message("Build finished")            
        else:
            execcmd.sublime.status_message(("Build finished with %d errors") % len(errs))


    def on_data(self, proc, data):
        execcmd.sublime.set_timeout(functools.partial(self.append_data, proc, data), 0)

    def on_finished(self, proc):
        execcmd.sublime.set_timeout(functools.partial(self.finish, proc), 0)
