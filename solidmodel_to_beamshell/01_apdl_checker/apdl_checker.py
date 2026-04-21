import json
import re
import argparse
from pathlib import Path

class APDLChecker:
    def __init__(self, rules_path: str):
        """Initialize the checker with a path to rules.json."""
        self.rules_path = Path(rules_path)
        self.rules = self._load_rules()
        self.errors = []

    def _load_rules(self) -> dict:
        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading rules from {self.rules_path}: {e}")
            return {"commands": {}}

    def parse_line(self, line: str) -> list:
        """Parse a single APDL line, ignoring comments and splitting arguments."""
        # Remove comments starting with !
        line_no_comment = line.split('!')[0].strip()
        if not line_no_comment:
            return []
        
        # Split by comma and strip whitespace
        parts = [p.strip().upper() for p in line_no_comment.split(',')]
        return parts

    def check_file(self, filepath: str) -> list:
        """Check an APDL file and return a list of errors."""
        self.errors = []
        path = Path(filepath)
        
        if not path.exists():
            self.errors.append({"line": 0, "error": f"File not found: {filepath}"})
            return self.errors

        try:
            # Using utf-8 with replace to handle potential encoding issues on Windows
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                for line_num, line in enumerate(f, 1):
                    parts = self.parse_line(line)
                    if not parts:
                        continue
                    
                    command = parts[0]
                    self._validate_command(command, parts, line_num, line.strip())
        except Exception as e:
            self.errors.append({"line": 0, "error": f"Error reading file: {e}"})

        return self.errors

    def _validate_command(self, command: str, parts: list, line_num: int, raw_line: str):
        """Validate a single command against rules."""
        cmd_rules = self.rules.get("commands", {}).get(command)
        if not cmd_rules:
            # We don't check commands that are not in our rules (yet)
            return

        # Check minimum arguments
        min_args = cmd_rules.get("min_args", 1)
        if len(parts) < min_args:
            self.errors.append({
                "line": line_num,
                "command": command,
                "raw": raw_line,
                "error": f"Not enough arguments. Expected at least {min_args}, got {len(parts)}."
            })
            return

        # Check labels
        labels_info = cmd_rules.get("labels")
        if labels_info:
            label_idx = labels_info.get("index")
            valid_values = labels_info.get("valid_values", [])
            
            if label_idx < len(parts):
                label_val = parts[label_idx]
                if valid_values and label_val not in valid_values:
                    self.errors.append({
                        "line": line_num,
                        "command": command,
                        "raw": raw_line,
                        "error": f"Invalid label '{label_val}' at index {label_idx}. Valid options are: {', '.join(valid_values)}"
                    })

        # Check numeric fields
        numeric_indices = cmd_rules.get("numeric_indices", [])
        for idx in numeric_indices:
            if idx < len(parts) and parts[idx] != "":
                # Try to convert to float (or int)
                val = parts[idx]
                # In APDL, variables can be used. If it's not a number, we might need a variable tracker.
                # For PoC, we will only check if it looks like a variable or parameter vs a hardcoded non-number.
                # A simple heuristic: if it contains letters but isn't a known parameter, it might be an error.
                # But for now, we'll try to cast to float. If it fails, we assume it's a parameter (which we skip for now).
                try:
                    float(val)
                except ValueError:
                    # It's not a number. If it contains symbols like +/-/*/// or numbers, it might be an expression.
                    # We will log an info/warning if we implement variable tracking, but for now we pass.
                    pass

        # Command specific checks
        if command == "ET":
            valid_elements = cmd_rules.get("valid_elements", [])
            if len(parts) > 2:
                # Element name/number is usually index 2
                ename = parts[2]
                try:
                    ename_int = int(ename)
                    if valid_elements and ename_int not in valid_elements:
                         self.errors.append({
                            "line": line_num,
                            "command": command,
                            "raw": raw_line,
                            "error": f"Unsupported or invalid element type '{ename_int}'. Supported: {valid_elements}"
                        })
                except ValueError:
                     self.errors.append({
                            "line": line_num,
                            "command": command,
                            "raw": raw_line,
                            "error": f"Element type '{ename}' should be a number."
                        })

    def print_report(self):
        """Print a formatted report of errors."""
        if not self.errors:
            print("No errors found! ✨")
            return

        print(f"\n--- APDL Verification Report ({len(self.errors)} errors) ---")
        for err in self.errors:
            print(f"Line {err.get('line')}: {err.get('error')}")
            if 'raw' in err:
                print(f"  Code: {err.get('raw')}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="APDL Static Checker PoC")
    parser.add_argument("file", help="Path to the APDL file to check")
    parser.add_argument("--rules", default="rules.json", help="Path to the rules.json file")
    
    args = parser.parse_args()
    
    checker = APDLChecker(args.rules)
    checker.check_file(args.file)
    checker.print_report()
