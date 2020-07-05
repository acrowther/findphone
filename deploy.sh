functionname=${PWD##*/}
gcloud functions deploy $functionname --runtime=python37 --trigger-topic=$functionname --entry-point=process --service-account=bigquery@tinbiwebsite.iam.gserviceaccount.com
