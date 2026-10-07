import importlib
import pkgutil
import modules
from discord.ext import commands

def load_modules(bot: commands.Bot):
    for module_info in pkgutil.iter_modules(modules.__path__):
        if not module_info.ispkg:
            continue

        module = importlib.import_module(
            f"modules.{module_info.name}.module"
        )

        module.setup(bot)