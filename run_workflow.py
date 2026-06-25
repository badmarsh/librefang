import urllib.request, json

workflows = [
    ('dashboard-kpi-tracker', 'b0ff5245-e0a3-4348-bbfc-4ec6af66aa24'),
    ('disinfo-pipeline', '78705f90-a2c4-4bb2-ae98-6bc4d551eb98'),
    ('feedback-ingestion', '074016ec-dcb9-4bed-b78e-5fcf9022199f')
]

for name, wid in workflows:
    print(f'Running {name} ({wid})...')
    req = urllib.request.Request(
        f'http://127.0.0.1:4545/api/workflows/{wid}/run?wait=true', 
        data=b'{"input":"run"}', 
        headers={'Content-Type':'application/json', 'Authorization':'Bearer lf_key_527679d18a9ebd59e00a049e3596f801'}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        print(f"Success! Response: {resp.read().decode()}")
    except Exception as e:
        if hasattr(e, 'read'): 
            print(f"Error ({e.code}): {e.read().decode()}")
        else: 
            print(f"Error: {e}")
