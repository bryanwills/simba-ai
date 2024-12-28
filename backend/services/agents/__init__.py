# agents/__init__.py
import os
import glob

# Automatically import all Python files in the agents directory
modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if os.path.isfile(f) and not f.endswith('__init__.py')]
# __all__ = ["RetrievalAgent", "GraderAgent"]
