import colorama
from colorama import Fore
colorama.init(autoreset=True)

""" Image scaler for the game buttons """

# it's a small fun script to scale the images for the game buttons or other images if you want to use it
# don't foget to play with padding and size to get the best result

original_dimensions_1 = (175, 210) 
original_dimensions_2 = (234, 91) 

# Calculate new dimensions (0.35 = 35% increase) 
new_dimensions_1 = tuple([int(dim * 1.35) for dim in original_dimensions_1]) 
new_dimensions_2 = tuple([int(dim * 1.35) for dim in original_dimensions_2]) 


print(f"{Fore.GREEN}size={new_dimensions_1}")
print(f"{Fore.GREEN}size={new_dimensions_2}")
