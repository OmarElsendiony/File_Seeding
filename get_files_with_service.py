import json
from pathlib import Path

def add_service_to_keys(
    structure_json_path,
    flat_json_path,
    output_json_path
):
    structure_json_path = Path(structure_json_path)
    flat_json_path = Path(flat_json_path)
    output_json_path = Path(output_json_path)

    # Load structure (service → folders → files)
    with structure_json_path.open("r", encoding="utf-8") as f:
        structure = json.load(f)

    # Load flat map (tracking/file.py → content)
    with flat_json_path.open("r", encoding="utf-8") as f:
        flat = json.load(f)

    result = {}

    for service_name, service_data in structure.items():
        for folder, folder_data in service_data.items():
            for filename in folder_data.get("files", []):
                old_key = f"{folder}/{filename}"
                new_key = f"{service_name}/{old_key}"

                if old_key in flat:
                    result[new_key] = flat[old_key]

    with output_json_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Saved JSON with service-prefixed keys to {output_json_path}")

add_service_to_keys(
    structure_json_path="folder_structure.json",
    flat_json_path="files_fixes_info.json",
    output_json_path="files_fixes_info_with_service.json"
)
