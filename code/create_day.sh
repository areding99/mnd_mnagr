# set -x # for debug mode

# ~ doesn't resolve to $HOME in ""
log_path="$HOME/Desktop/task_management/demo_files/logs"
top_level_dir="task_management"

# when child process dies, will return to pwd at time of running script automatically
cd $log_path

year_dir=`date +%Y`

if [ ! -d $year_dir ]; then 
  mkdir $year_dir
fi

cd $year_dir

# use `` to embed a call to a command
today=`date +%Y-%m-%d`
today_log="$today.md"


if [ -f $today_log ]; then
  echo "you've already created a daily log for today"
  exit 1
fi

touch $today_log

cat << EOF >> $today_log
---
title: $today
path: `pwd`
created: `date +%Y-%m-%d` `date +%H:%M`
id: `uuidgen`
---
EOF

