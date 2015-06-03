import sublime, sublime_plugin
import os, tempfile, webbrowser
from . import templates
from . import compile

class SynesthesiaNewCommand(sublime_plugin.WindowCommand):
	def run(self):
		v = self.window.new_file()
		v.settings().set('default_dir', compile.SYNESTHESIA_OUTPUT_PATH)
		v.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')

		v.run_command("insert_snippet", {"contents": templates.new_file})

class SynesthesiaSampleCommand(sublime_plugin.WindowCommand):
	def run(self):
		v = self.window.new_file()
		v.settings().set('default_dir', compile.SYNESTHESIA_OUTPUT_PATH)
		v.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')

		v.run_command("insert_snippet", {"contents": templates.sample_file})
