# Usefull informations I used to implement this tool comes from
# https://blender.stackexchange.com/a/39747/71342
from zipfile import ZipFile
import os
from os.path import basename

filenames = (
  '__init__.py',
  'build_hierarchy.py',
)

with ZipFile('camera_hierarchy.zip', 'w') as zipObj:
  for filename in filenames:
    filepath = os.path.join('add_camera_hierarchy', filename)
    zipObj.write(filename, filepath)

# close the Zip File
zipObj.close()
