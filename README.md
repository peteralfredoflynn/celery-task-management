# celery-task-management


# How to query K8s ap

```
kubectl proxy
```
In separate terminal
```
curl http://127.0.0.1:8001/apis/batch/v1
```
This is the response. you can see the preferred version for batch is v1.
```json
{
"kind": "APIGroup",
"apiVersion": "v1",
"name": "batch",
"versions": [
{
"groupVersion": "batch/v1",
"version": "v1"
},
{
"groupVersion": "batch/v1beta1",
"version": "v1beta1"
}
],
"preferredVersion": {
"groupVersion": "batch/v1",
"version": "v1"
}
}
```


### Helpers
```
docker build -t task_mgt:v3 .
```


```
docker tag task_mgt:v3 gcr.io/peter-sandbox-237917/task_mgt:v3
```

```
docker push gcr.io/peter-sandbox-237917/task_mgt:v3
```
