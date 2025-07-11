import xml.etree.ElementTree as ET
import os.path, time
import json
import os
import time
import datetime
import sys
import gzip
import argparse

# Third-party modules
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("\n✅ Built-in modules loaded.")

# Show where each third-party module is installed
print("\n📦 Module locations:")
print(f"pandas:     {pd.__file__}")
print(f"numpy:      {np.__file__}")
print(f"seaborn:    {sns.__file__}")
print(f"matplotlib: {matplotlib.__file__}")
print(f"pyplot:     {plt.__file__}")

# Optional: show the Python environment path
print(f"\n🐍 Python executable: {sys.executable}")

