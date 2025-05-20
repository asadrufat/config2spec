import subprocess
import os
import argparse

def run_c2s(input_dir: str, backend_path: str = None, batfish_path: str = None, failure_model: int = 0):
    """
    Runs config2spec with the specified input directory and failure model.
    
    Parameters:
    - input_dir: Path to the directory containing network configuration files.
    - backend_path: Path to the backend jar file (optional).
    - batfish_path: Path to batfish (optional).
    - failure_model: Integer representing the failure model (default is 0).
    """
    # Construct the command
    if not backend_path:
        backend_path = os.path.join(
            "batfish_interface",
            "batfish-73946b2f1bdea5f1146e4db4f2586e071da752df",
            "projects",
            "backend",
            "target",
            "backend-bundle-0.36.0.jar"
        )
    
    if not batfish_path:
        batfish_path = "~/tmp"

    # Convert failure_model to string if it's not already
    if not isinstance(failure_model, str):
        failure_model = str(failure_model)
    
    command = [
        "python", "run_c2s.py",
        input_dir,
        backend_path,
        batfish_path,
        "-mf", failure_model
    ]

    print(f"[INFO] Running: {' '.join(command)}")

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        # Print stdout for visibility
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed with exit code {e.returncode}")
        print(f"[ERROR] Error message: {e.stderr}")
        print("[ERROR] Could not complete Config2Spec execution")
    
    # Filter out waypoint policies and output in a new csv file
    simplified_csv = os.path.join(input_dir, "policies_simplified.csv")
    output_dir = os.path.join(input_dir, "cleaned_policies.csv")
    with open(simplified_csv, "r") as f:
        lines = f.readlines()
    with open(output_dir, "w") as f:
        for line in lines:
            if "waypoint" not in line.lower():
                f.write(line)
    print(f"[INFO] Filtered policies saved to {output_dir}")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run Config2Spec and filter waypoint policies')
    
    # Required argument
    parser.add_argument('--input_dir', '-i', required=True, 
                        help='Path to the directory containing network configuration files')
    
    # Optional arguments with defaults
    parser.add_argument('--backend_path', '-b', 
                        help='Path to the backend jar file')
    parser.add_argument('--batfish_path', '-p', 
                        help='Path to batfish')
    parser.add_argument('--failure_model', '-f', type=int, default=0,
                        help='Integer representing the failure model (default: 0)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the main function
    run_c2s(
        input_dir=args.input_dir,
        backend_path=args.backend_path,
        batfish_path=args.batfish_path,
        failure_model=args.failure_model
    )