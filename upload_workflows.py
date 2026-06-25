import tomllib, json, urllib.request, urllib.error
for f in ['workflows/dashboard-kpi-tracker.toml', 'workflows/disinfo-pipeline.toml', 'workflows/feedback-ingestion.toml']:
    try:
        with open(f, 'rb') as file:
            data = tomllib.load(file)
        req = urllib.request.Request('http://127.0.0.1:4545/api/workflows', data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer lf_key_527679d18a9ebd59e00a049e3596f801'})
        resp = urllib.request.urlopen(req)
        print(f'{f}: {resp.read().decode()}')
    except Exception as e:
        if isinstance(e, urllib.error.HTTPError):
            print(f'{f}: {e.code} {e.read().decode()}')
        else:
            print(f'{f}: Error: {e}')
