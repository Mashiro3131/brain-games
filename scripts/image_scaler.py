""" Image scaler for the game buttons """




original_dimensions_1 = (175, 210) 
original_dimensions_2 = (234, 91) 

# Calculate new dimensions (50% increase) 
new_dimensions_1 = tuple([int(dim * 1.35) for dim in original_dimensions_1]) 
new_dimensions_2 = tuple([int(dim * 1.35) for dim in original_dimensions_2]) 


print("size=" + str(new_dimensions_1)+")")
print("size=" + str(new_dimensions_2)+")")
