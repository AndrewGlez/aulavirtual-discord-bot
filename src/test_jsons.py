import json

def compare_data():
    from save_tasks import fetch_task

    # Fetch new data
    new_data = fetch_task()

    # Current local data
    with open('task.json', 'r+') as f:
        current_data = json.load(f)
        # Compare
        new_ids = {item['id'] for item in new_data[0]['data']['events']}
        current_ids = {item['id'] for item in current_data[0]['data']['events']}
        if new_ids != current_ids:
            f.seek(0)
            f.truncate()
            f.write(json.dumps(new_data, indent=2))
            return True
        return False
    
compare_data()