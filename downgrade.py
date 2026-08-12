import json
from pathlib import Path
from datetime import datetime
from setup import setup

def parse_timestamp(iso_time):
    """Convert ISO format timestamp to Unix timestamp"""
    if iso_time:
        dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
        return int(dt.timestamp())
    return 0

def convert_json_to_save_py(input_json, output_py, save_name):
    print(f"Loading from: {input_json}")
    
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract basic info
    json_save_name = data.get("name", save_name)
    end_time = data.get("end")
    updated_at = data.get("updatedAt")
    
    # Convert timestamp
    timestamp = parse_timestamp(end_time)
    
    activities = data.get('activities', [])
    print(f"Processing {len(activities)} activities")

    # Get activity names and build reverse mapping from templates
    activity_names = set()
    for activity in activities:
        activity_names.add(activity.get('name', 'Unknown'))
    
    # Create activity list in old format
    old_activities = []
    notes_count = 0
    
    for activity in activities:
        name = activity.get('name', 'Unknown')
        begin_time = activity.get('begin')
        ts_begin = parse_timestamp(begin_time)
        
        # Build activity entry
        activity_entry = [name, ts_begin]
        
        # Add note if present
        if 'note' in activity and activity['note']:
            activity_entry.append('')  # End time placeholder (empty for now)
            activity_entry.append(activity['note'])
            notes_count += 1
        else:
            activity_entry.append('')  # End time placeholder
        
        old_activities.append(activity_entry)

    # Generate Python code with proper formatting
    py_code = f"""# Auto-generated downgrade from JSON
# Save name: {json_save_name}
# Generated at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Total activities: {len(old_activities)}

timestamp = {timestamp}
activities = {old_activities}
"""

    with open(output_py, "w", encoding="utf-8") as f:
        f.write(py_code)

    print(f"Converted to {output_py}")
    print(f"Processed {len(old_activities)} activities")
    print(f"Activities with notes: {notes_count}/{len(old_activities)}")
    print(f"Save name: {json_save_name}")
    print(f"Timestamp: {timestamp}")

# Load config and args
ARGS, ACTIVITIES = setup("downgrade")

# Set default input JSON if not provided
if ARGS["INPUT_JSON"] == "save.json":
    if Path("save.json").exists():
        print("Using default save.json")
    else:
        print("Warning: save.json not found, using test_save.json instead")
        ARGS["INPUT_JSON"] = "test_save.json"

# Check if INPUT_JSON was provided via command line
import sys
if len(sys.argv) == 1:  # No arguments provided
    ARGS["INPUT_JSON"] = "save.json"

# Check if INPUT_JSON exists
if not Path(ARGS["INPUT_JSON"]).exists():
    print(f"Error: Input file '{ARGS['INPUT_JSON']}' not found")
    exit(1)

if ARGS["OUTPUT_PY"] == "auto":
    input_path = Path(ARGS["INPUT_JSON"])
    ARGS["OUTPUT_PY"] = f"{input_path.stem}_downgrade.py"

convert_json_to_save_py(
    ARGS["INPUT_JSON"],
    ARGS["OUTPUT_PY"],
    ARGS["SAVE_NAME"]
)
