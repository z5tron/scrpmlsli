import re
import os
for root, dirs, files in os.walk("."):
    pics = [v for v in files if v.endswith('jpg')]
    if not pics:
        print(root)

