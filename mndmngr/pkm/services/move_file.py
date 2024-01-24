# get the file and new location from command line args
import os, sys, dotenv

dotenv.load_dotenv()

args = sys.argv
file_path_rel = args[1]
new_path_rel = args[2]

print("Moving file...")

file_name = file_path_rel.split("/")[-1]
file_path_full = os.environ["PROJECT_ROOT"] + file_path_rel

if new_path_rel[-1] == "/":
    new_path_rel = new_path_rel[:-1]
new_path_full = os.environ["PROJECT_ROOT"] + new_path_rel + "/" + file_name

try:
    os.rename(file_path_full, new_path_full)
except:
    print("Could not move file, exiting...")
    sys.exit(1)

print("Updating references...")

for root, dirs, files in os.walk((os.environ["PROJECT_ROOT"] + "/example")):
    for file in files:
        with open(os.path.join(root, file), "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if file_path_rel in line:
                    line = line.replace(file_path_rel, new_path_rel)
                f.write(line)
            f.truncate()
