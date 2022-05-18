import pcbnew
import os

class HelloWorldAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "A complex action plugin"
        self.category = "A descriptive category name"
        self.description = "A description of the plugin"
        self.show_toolbar_button = True # Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'hello_world_light.png') # Optional

    def Run(self):
        # The entry function of the plugin that is executed on user action
        print("Hello World")