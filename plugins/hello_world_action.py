import pcbnew
import os

class HelloWorldAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Test Plugin"
        self.category = "Test"
        self.description = "This plugin opens a window that says Hello World"
        self.show_toolbar_button = True # Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'hello_world_light.png') # Optional

    def Run(self):
        # The entry function of the plugin that is executed on user action
        print("Hello World")