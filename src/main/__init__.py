import os
import pathlib as pl
curr_file = pl.Path(os.path.realpath(__file__))

img_dir = str(curr_file.parents[2]) + f"{os.sep}img{os.sep}"