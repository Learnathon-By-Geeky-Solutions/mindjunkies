1. Test django

```
python manage.py test
```

2. Build container

```
docker build -f Dockerfile \
  -t registry.digitalocean.com/mindjunkies/django-mindjunkies-web:latest 
  -t registry.digitalocean.com/mindjunkies/django-mindjunkies-web:v1 \
  .
```

3. Push Container with 2 tags: latest and random

```
docker push registry.digitalocean.com/mindjunkies/django-mindjunkies-web --all-tags
```

4. Update secrets (if needed)

```
kubectl delete secret django-mindjunkies-prod-env
kubectl create secret generic django-mindjunkies-prod-env --from-env-file=.env.prod

```

5. Update Deployment `k8s/apps/django-mindjunkies-web.yaml`:

Add in a rollout strategy:


`imagePullPolicy: Always`

Change 
```
image: registry.digitalocean.com/mindjunkies/django-mindjunkies-web:latest
```
to

```
image: registry.digitalocean.com/mindjunkies/django-mindjunkies-web:v1 
```
Notice that we need `v1` to change over time.


```
kubectl apply -f k8s/apps/django-mindjunkies-web.yaml
```

6. Roll Update:
```
kubectl rollout status deployment/django-mindjunkis-web-deployment
```
7. Migrate database

Get a single pod (either method works)

```
export SINGLE_POD_NAME=$(kubectl get pod -l app=django-mindjunkies-web-deployment -o jsonpath="{.items[0].metadata.name}")
```
or 
```
export SINGLE_POD_NAME=$(kubectl get pod -l=app=django-mindjunkies-web-deployment -o NAME | tail -n 1)
```

Then run `migrate.sh` 

```
kubectl exec -it $SINGLE_POD_NAME -- bash /app/migrate.sh
```