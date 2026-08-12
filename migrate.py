import json
import uuid
from pathlib import Path
from datetime import datetime, timezone
from setup import setup

def format_timestamp(ts):
    """Convert timestamp to ISO format YYYY-MM-DDTHH:MM:SSZ"""
    if ts == 0:
        dt = datetime.now(timezone.utc)
    else:
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def convert_save_py_to_json(input_py, output_json, save_name, activities_config):
    print(f"Loading from: {input_py}")
    
    with open(input_py, "r", encoding="utf-8") as f:
        code = f.read()

    namespace = {}
    exec(code, namespace)

    timestamp = namespace.get("timestamp", 0)
    old_activities = namespace.get("activities", [])
    
    print(f"Found {len(old_activities)} activities")

    # Get unique activity names
    used_activity_names = set()
    for activity in old_activities:
        if len(activity) > 0:
            used_activity_names.add(activity[0])

    # Build activityTemplates
    activity_templates = []
    for activity_name in used_activity_names:
        rgb = activities_config.get(activity_name, [128, 128, 128])
        if isinstance(rgb, list) and len(rgb) == 3:
            hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        else:
            hex_color = "#808080"
        
        activity_templates.append({
            "name": activity_name,
            "id": str(uuid.uuid4()),
            "color": hex_color
        })

    # Build activities list with optional note
    activities_list = []
    notes_count = 0
    for activity in old_activities:
        name = activity[0]
        ts_begin = activity[1]
        begin_time = format_timestamp(ts_begin)
        
        new_activity = {
            "name": name,
            "begin": begin_time,
            "id": str(uuid.uuid4())
        }
        
        if len(activity) > 3 and activity[3] and activity[3].strip():
            new_activity["note"] = activity[3]
            notes_count += 1
        
        activities_list.append(new_activity)

    # End time from save timestamp
    end_time = format_timestamp(timestamp)
    updated_at = format_timestamp(timestamp) if timestamp != 0 else format_timestamp(0)

    # Use folder name as save name if auto
    if save_name == "auto":
        input_path = Path(input_py)
        save_name = input_path.parent.name
        print(f"Using folder name as save name: {save_name}")

    output_data = {
        "name": save_name,
        "activities": activities_list,
        "activityTemplates": activity_templates,
        "end": end_time,
        "updatedAt": updated_at,
        "id": str(uuid.uuid4())
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Converted to {output_json}")
    print(f"Created {len(activity_templates)} templates for used activities")
    print(f"Activities with notes: {notes_count}/{len(activities_list)}")
    print(f"End time: {end_time}")

# Load config and args
ARGS, ACTIVITIES = setup("migrate")

if ARGS["OUTPUT_JSON"] == "auto":
    ARGS["OUTPUT_JSON"] = f"{uuid.uuid4()}.json"

convert_save_py_to_json(
    ARGS["INPUT_SAVE"],
    ARGS["OUTPUT_JSON"],
    ARGS["SAVE_NAME"],
    ACTIVITIES
)
