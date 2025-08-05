from .default import *
from .contrib import *

computers_config = {
    "local-playwright": LocalPlaywrightBrowser,
    "docker": DockerComputer,
    "browserbase": BrowserbaseBrowser,
    # "scrapybara-browser": ScrapybaraBrowser,  # Commented out - missing dependency
    # "scrapybara-ubuntu": ScrapybaraUbuntu,    # Commented out - missing dependency
}
