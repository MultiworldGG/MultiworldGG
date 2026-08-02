from OverworldShuffle import __version__ as OWVersion
import os

with(open(os.path.join("resources","app","meta","manifests","app_version.txt"),"w+")) as f:
  f.write(OWVersion)
