import os
import random
import string
import subprocess
from datetime import datetime, timedelta

# Function to generate random text
def generate_random_text(size):
    """Generate random text of the given size in bytes."""
    chars = string.ascii_letters + string.digits + string.punctuation + " \n"
    return ''.join(random.choices(chars, k=size))

# Function to generate filenames
def generate_filename():
    """Generate a filename with the pattern a_b_c.uasset."""
    a_options = [
        "Skeletal", "Mesh", "Spectator", "WBP", "PS", "GS", "SKM", "TAttribute", 
        "UActorComponent", "AActor", "SCompoundWid", "IAnalyticsProvider", 
        "CStaticClassProvider", "EColorBits", "Texture", "Sound", "Audio", "Animation"
    ]
    b_options = [
        "Character", "Asset", "Accessory", "Hand", "Body", "Leg", "Thigh", 
        "Enemy", "Player", "UI", "Main", "Sub", "forbidden", "validityChecks"
    ]
    c = random.randint(1, 10000)
    a = random.choice(a_options)
    b = random.choice(b_options)
    return f"{a}_{b}_{c}.uasset"

# Function to create random files
def create_random_files(num_files, min_size, max_size, folder='Content'):
    """Create random files with specific filename patterns in the Content folder."""
    os.makedirs(folder, exist_ok=True)  # Ensure the Content subfolder exists
    for _ in range(num_files):
        file_size = random.randint(min_size, max_size)
        file_name = generate_filename()
        file_path = os.path.join(folder, file_name)
        
        with open(file_path, 'w') as f:
            f.write(generate_random_text(file_size))
        
        print(f"Created {file_name} in {folder} with size {file_size} bytes.")

# Function to generate a random commit message
def generate_commit_message():
    """Generate a random commit message with the pattern a b c."""
    a_options = ["Add", "Update", "Fix", "Create", "Edit", "Duplicate", "Export", "Optimization"]
    b_options = ["Building", "Hall", "Tree", "Props", "Lighting", "Ground", "Environment", 
                 "Texture", "UI", "Graphic", "Menu", "Button", "Artboard"]
    c_options = ["FBX", "Mesh", "Object", "Asset", "3D", "Animation"]
    a = random.choice(a_options)
    b = random.choice(b_options)
    c = random.choice(c_options)
    return f"{a} {b} {c}"

# Function to generate a random time for a specific date
def generate_commit_time(date):
    """Generate a random time on the given date between 16:45:03 and 16:59:37."""
    random_time = datetime.combine(date, datetime.min.time()) + timedelta(
        hours=16, minutes=random.randint(45, 59), seconds=random.randint(3, 37)
    )
    return random_time.strftime("%Y-%m-%dT%H:%M:%S")

# Function to run Git commands
def run_git_command(command, env=None):
    """Run a Git command using subprocess."""
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, env=env)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")

# Main logic to commit for each day in the range
if __name__ == "__main__":
    start_date = datetime(2024, 4, 1)
    end_date = datetime(2024, 11, 30)
    current_date = start_date

    while current_date <= end_date:
        print(f"\n--- Processing Date: {current_date.strftime('%Y-%m-%d')} ---\n")

        # Create random files in the Content folder
        num_files = random.randint(3, 7)  # Number of files
        min_size = 20 * 1024  # 20 KB
        max_size = 50 * 1024  # 50 KB
        create_random_files(num_files, min_size, max_size, folder='Content')

        # Generate commit message and time
        commit_message = generate_commit_message()
        commit_time = generate_commit_time(current_date)

        # Set environment variables for commit date
        env = os.environ.copy()
        env['GIT_COMMITTER_DATE'] = commit_time
        env['GIT_AUTHOR_DATE'] = commit_time

        # Run Git commands
        print("Adding files to Git...")
        run_git_command(["git", "add", "."], env=env)

        print(f"Committing files with message: '{commit_message}' and date: {commit_time}")
        run_git_command(["git", "commit", "-m", commit_message], env=env)

        # Move to the next day
        current_date += timedelta(days=1)
