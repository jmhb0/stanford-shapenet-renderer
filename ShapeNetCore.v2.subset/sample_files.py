import subprocess
import argparse
import pandas as pd
import os 
import ipdb
import numpy as np
blender_path = "/Applications/Blender.app/Contents/MacOS/Blender"

this_fname = os.path.abspath(__file__)
this_dir = os.path.dirname(this_fname)

# Create an argparse object to get the class name
parser = argparse.ArgumentParser()
parser.add_argument("--shapenet_class", type=str, default='car', help="Shapenet class")
parser.add_argument("--num", type=int, default=100, help="Number of samples")
parser.add_argument("--seed", type=int, default=0)

args = parser.parse_args()

# lookup the code for this class
categories = open(os.path.join(this_dir, "all_categories.txt")).read().split("\n")
codes = [c[:8] for c in categories]
classes= [c[9:].strip() for c in categories]
class_lookup = pd.Series(codes, index=classes)
code = class_lookup.loc[args.shapenet_class]

# load the uid list and filter for the chosen class
uids = pd.read_csv(os.path.join(this_dir, "all.csv"))
uids = uids[uids['synsetId']==int(code)] 
print(f"Found {len(uids)} objects with class {args.shapenet_class}")

# exclude some of them 
uids_exclude = open(os.path.join(this_dir, "exclude_uids.txt")).read()
uids_exclude = uids_exclude.split("\n")
uids_exclude = [u.strip() for u in uids_exclude]
uids = uids[~uids['modelId'].isin(uids_exclude)]

# do the sampling 
uids_sample = uids.sample(n=args.num, random_state=args.seed)['modelId']


# copy the model ids for the samples
dir_class = os.path.join(this_dir, "samples", f"samples_{args.shapenet_class}")
os.makedirs(dir_class, exist_ok=True)
for uid in uids_sample:
    source_file = os.path.join("jmhb@scdt.stanford.edu:/pasteur/data/ShapeNet/ShapeNetCore.v2", code ,uid)
    destination_file = dir_class

    # copy the files
    if not os.path.exists(os.path.join(destination_file, uid)):
        subprocess.run(['scp', '-r', source_file, destination_file])

    # do the rendering
    fname_3d_model = os.path.join(destination_file, uid,'models', 'model_normalized.obj')
    output_folder = os.path.join(destination_file, uid, "renders")
    if not os.path.exists(output_folder):
        command = f"{blender_path} --background --python render_blender.py -- --output_folder {output_folder} {fname_3d_model} --scale=0.8 --resolution=512"
        print(command)
        command = command.split(" ")
        print(command)
        result = subprocess.run(command,)


ipdb.set_trace()
pass
