functionname=${PWD##*/}
venvname=$functionname'env'
cd ../
virtualenv $venvname
source $venvname/bin/activate
cd $functionname
pip install -r requirements.txt
#python test.py
bq mk -t us.phone name:STRING,phone:STRING
