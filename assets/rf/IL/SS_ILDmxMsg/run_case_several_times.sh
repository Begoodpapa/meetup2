if [ $# -lt 1 ]
then
   echo "Usage: $0 CASE_NAME [TIMES]"
   exit 1
fi

CASE_NAME=$1
RUN_TIMES=${2:-1}
LOG_PATH=logs

source func_run_case.sh

echo "*************  Total Run $RUN_TIMES times  **************"
rm -rf $LOG_PATH
mkdir $LOG_PATH

for ((  i = 1 ;  i <= $RUN_TIMES;  i++  ))
do
  echo "************** Dmxmsg functional Test No. $i ************* "
  date
  run_case $CASE_NAME 
  if [ $? -ne 0 ]; then 
    echo -e "\n\tError occured while running case $CASE_NAME !\n" 1>&2
  else
    cp ./log.html ./$LOG_PATH/${CASE_NAME}_$i.html
  fi
done
