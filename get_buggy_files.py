import json
from pathlib import Path

def build_files_content_json(
    structure_json_path,
    root_dir,
    output_json_path
):
    structure_json_path = Path(structure_json_path)
    root_dir = Path(root_dir)
    output_json_path = Path(output_json_path)

    # Load structure JSON
    with structure_json_path.open("r", encoding="utf-8") as f:
        structure = json.load(f)

    files_content = {}

    for service_name, service_data in structure.items():
        for subfolder, subfolder_data in service_data.items():
            for filename in subfolder_data.get("files", []):

                # only .py files
                if not filename.endswith(".py"):
                    continue

                # ✅ key written to JSON (NO service)
                logical_key = f"{subfolder}/{filename}"

                # ✅ real filesystem path (WITH service)
                real_path = root_dir / service_name / subfolder / filename

                try:
                    files_content[logical_key] = real_path.read_text(
                        encoding="utf-8"
                    )
                except FileNotFoundError:
                    files_content[logical_key] = None

    # Save final JSON
    with output_json_path.open("w", encoding="utf-8") as f:
        json.dump(files_content, f, indent=2)

    print(f"Saved JSON to {output_json_path}")

build_files_content_json(
    structure_json_path="folder_structure.json",
    root_dir=".",
    output_json_path="files_content.json"
)

# print(files_dict["tracking/tracking_update_location.py"])
