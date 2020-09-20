#!/usr/bin/env python

import os

for root, dirs, files in os.walk("."):
   for name in files:
      filepath = os.path.join(root, name)
      if name in ("out_DDB.nc", "out_OUT.nc", "out_EIG.nc", "out_WFK.nc"):
          print(filepath)
