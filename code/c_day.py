import os, datetime, uuid

# # directory your task management files reside in
# parent_dir="/Desktop"
# relative_path="/task_management/demo_files/logs"
# # ~ doesn't resolve to $HOME in ""
# log_path="$HOME$parent_dir$relative_path"


# # when child process dies, will return to pwd at time of running script automatically
# cd $log_path

# year_dir=`date +%Y`

# if [ ! -d $year_dir ]; then 
#   mkdir $year_dir
# fi

# cd $year_dir

# # use `` to embed a call to a command
# today=`date +%Y-%m-%d`
# today_log="$today.md"


# # if [ -f $today_log ]; then
# #   echo "you've already created a daily log for today"
# #   exit 1
# # fi

# touch $today_log

# cat << EOF >> $today_log
# ---
# title: $today
# path: ${relative_path#/}/$year_dir/$today_log
# created: `date +%Y-%m-%d` `date +%H:%M`
# id: `uuidgen`
# ---
# EOF

parent_dir="/Desktop/task_management"
relative_path="/demo_files/logs"

log_path=os.path.expanduser('~')+parent_dir+relative_path

os.chdir(log_path)

year_dir = str(datetime.datetime.now().year)

if (not os.path.isdir(year_dir)):
  os.mkdir(year_dir)

os.chdir(year_dir)

today = str(datetime.datetime.now().date())
print(today)

today_log_name = today+".md"

if (os.path.isfile(today_log_name)):
  print("you've already created a daily log for today")
  exit(1)

today_log = open(today_log_name, 'w')

today_log.write("---\n")
today_log.write("title: "+today+"\n")
today_log.write("path: "+relative_path[1:]+"/"+year_dir+"/"+today_log_name+"\n")
today_log.write("created: "+str(datetime.datetime.now().date())+" "+str(datetime.datetime.now().time())+"\n")
today_log.write("id: "+str(uuid.uuid4())+"\n")
today_log.write("---\n")

today_log.close()

