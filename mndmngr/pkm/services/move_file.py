# get the file and new location from command line args
import os, sys, dotenv

dotenv.load_dotenv()

args = sys.argv
file_path_input = args[1]
new_path_input = args[2]

print("Moving file...")

file_path_abs = os.path.abspath(file_path_input)
new_path_abs = os.path.abspath(new_path_input)

user_root = os.environ["USER_ROOT"]

if not file_path_abs.startswith(user_root):
    print("Source file not found in project dir. Exiting...")
    sys.exit(1)

if not new_path_abs.startswith(user_root):
    print("Dest file not found in project dir. Exiting...")
    sys.exit(1)

file_path_rel = file_path_abs[len(user_root) :]
file_name = file_path_rel.split("/")[-1]
new_path_rel = new_path_abs[len(user_root) :] + "/" + file_name
full_new_path_abs = new_path_abs + "/" + file_name

try:
    os.rename(file_path_abs, full_new_path_abs)
except:
    print("Could not move file, exiting...")
    sys.exit(1)

print("Updating references...")

for root, dirs, files in os.walk((user_root)):
    for file in files:
        if file.endswith(".md"):
            with open(os.path.join(root, file), "r+") as f:
                lines = f.readlines()
                f.seek(0)
                for line in lines:
                    if file_path_rel in line:
                        line = line.replace(file_path_rel, new_path_rel)
                    f.write(line)
                f.truncate()
