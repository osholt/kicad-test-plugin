from .hello_world_action import HelloWorldAction # Note the relative import!
HelloWorldAction().register() # Instantiate and register to Pcbnew

# -*- coding: utf-8 -*-
try:
    # Note the relative import!
    from .hello_world_action import HelloWorldAction
    # Instantiate and register to Pcbnew
    HelloWorldAction().register()
# if failed, log the error and let the user know
except Exception as e:
    # log the error
    import os
    plugin_dir = os.path.dirname(os.path.realpath(__file__))
    log_file = os.path.join(plugin_dir, 'hello_world_error.log')
    with open(log_file, 'w') as f:
        f.write(repr(e))
    # register dummy plugin, to let the user know of the problems
    import pcbnew
    import wx

    class HelloWorld(pcbnew.ActionPlugin):
        """
        Notify user of error when initializing the plugin
        """
        def defaults(self):
            self.name = "HellowWorld"
            self.category = "HelloWorld"
            self.description = "Prints Hello World"

        def Run(self):
            caption = self.name
            message = "There was an error while loading plugin \n" \
                      "Please take a look in the plugin folder for hellow_world_error.log\n" \
                      "You can raise an issue on GitHub page.\n" \
                      "Please attach the .log file"
            wx.MessageBox(message, caption, wx.OK | wx.ICON_ERROR)

    HelloWorld().register()