import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from filters.channels import CHANNELS


class Channel_link:

    def make_links(self):
        links = ""
        for row in CHANNELS:
            links += f"👉 @{row}\n"
        self.links = links