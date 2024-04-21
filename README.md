# team24

python -m venv myenv
C:\Users\milia\AppData\Local\Programs\Python\Python39\python.exe -m venv myenv
.\myenv\Scripts\Activate

deactivate

gcloud builds submit --tag gcr.io/wild-step/wild_step_app --project=wild-step
gcloud run deploy --image gcr.io/wild-step/wild_step_app --platform managed --project=wild-step --allow-unauthenticated


