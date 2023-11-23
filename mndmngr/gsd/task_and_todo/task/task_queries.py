import os

if __name__ == "__main__":
  import dotenv, sys
  dotenv.load_dotenv()
  sys.path.append(os.environ['PROJECT_ROOT'])

def query_raw_task_by_id(id: str) -> list[str] | None:
  cwd = os.getcwd()

  os.chdir(os.environ['TASKS_PATH'])

  for section in os.listdir():
    os.chdir(section)
    print(section)
    for task_file in os.listdir():
      with open (task_file, 'r') as f_io:
        for line in f_io.readlines():
          # stop scanning after seeing first instance of 'id:' in metadata
          if 'id:' in line:
            if id in line:
              os.chdir(cwd)
              f_io.seek(0)
              return f_io.readlines()
            continue
    os.chdir("..")

  os.chdir(cwd)
  return None

print(query_raw_task_by_id("3e127e25-02c0-4803-a48f-4530b49ce9d7"))

def query_raw_tasks_in_section(section: str) -> list[list[str]]:
  cwd = os.getcwd()

  os.chdir(os.environ['TASKS_PATH'])
  os.chdir(section)

  tasks: list[list[str]] = []

  for t_file in os.listdir():
    with open (t_file, 'r') as f_io:
      tasks.append(f_io.readlines())

  os.chdir(cwd)

  return tasks

