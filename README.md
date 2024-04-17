# team24

gcloud builds submit --tag gcr.io/life-on-land-419810/wild-step --project=life-on-land-419810

gcloud run deploy --image gcr.io/life-on-land-419810/wild-step --platform managed --project=life-on-land-419810 --allow-unauthenticated


gcloud builds submit --tag gcr.io/wild-step/wild_step_app --project=wild-step
gcloud run deploy --image gcr.io/wild-step/wild_step_app --platform managed --project=wild-step --allow-unauthenticated


