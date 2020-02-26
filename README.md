# celery-task-management

### Helpers
```
docker build -t task_mgt:v3 .
```


```
sed -i -e 's/VERSION/v3/g' app.yml
sed -i -e 's/VERSION/v3/g' .yml
```


```
docker tag task_mgt:v3 gcr.io/peter-sandbox-237917/task_mgt:v3
```

```
docker push gcr.io/peter-sandbox-237917/task_mgt:v3
```
