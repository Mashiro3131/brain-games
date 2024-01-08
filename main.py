import os
import sys
import new_menu as menu
# Get the absolute path of the current script
current_path = os.path.dirname(os.path.abspath(__file__))

# Append the 'src' folder to the sys.path
src_path = os.path.join(current_path, 'src')
sys.path.append(src_path)

menu.launch_menu()