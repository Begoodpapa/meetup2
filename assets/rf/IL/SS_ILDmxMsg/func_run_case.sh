EXTs='html htm tsv'

function run_case()
{
  if [ -z $1 ]; then return 1; fi
  CASE_NAME=$1

  if [ -f $CASE_NAME ]; then 
    pybot -P ../../TALIB/src -L TRACE $CASE_NAME 
    return 0
  fi

  run=0
  for ext in $EXTs; do
    if [ -f $CASE_NAME.$ext ]; then 
      pybot -P ../../TALIB/src -L TRACE $CASE_NAME.$ext
      run=1
    fi
  done
  if [ $run -eq 0 ]; then return 1; fi
  return 0
}
