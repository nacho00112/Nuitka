
from nuitka import Options
from nuitka.Tracing import options_logger
import shutil

def checkTermuxSpecificCommands():
    # onefile checks
    if Options.isOnefileMode():
        # termux-elf-cleaner
        if not shutil.which("termux-elf-cleaner"):
            options_logger.warning("Running in Termux with onefile mode but termux-elf-cleaner was not found in PATH. " \
                    "you won't be able to apply it later since the binary will be contained within the onefile.")

