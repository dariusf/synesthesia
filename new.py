import sublime, sublime_plugin
import os, tempfile, webbrowser
from . import templates

class SynesthesiaNewCommand(sublime_plugin.WindowCommand):
	def run(self):
		v = self.window.new_file()
		v.settings().set('default_dir', os.path.join(sublime.packages_path(), 'synesthesia'))
		v.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')

		v.run_command("insert_snippet", {"contents": templates.new_file})

class SynesthesiaSampleCommand(sublime_plugin.WindowCommand):
	def run(self):
		v = self.window.new_file()
		v.settings().set('default_dir', os.path.join(sublime.packages_path(), 'synesthesia'))
		v.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')

		v.run_command("insert_snippet", {"contents": templates.sample_file})
