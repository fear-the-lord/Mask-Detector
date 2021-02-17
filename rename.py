# Pythono3 code to rename multiple 
# files in a directory or folder 

# importing os module 
import os 

# Function to rename multiple files 
def main(): 

	for count, filename in enumerate(os.listdir("dataset/without_mask")): 
		dst = "img" + str(count) + ".jpg"
		src = 'dataset/without_mask/' + filename 
		dst = 'dataset/without_mask/' + dst
		
		# rename() function will 
		# rename all the files
		print("Renaming: ", src, "->", dst) 
		os.rename(src, dst) 

# Driver Code 
if __name__ == '__main__': 
	
	# Calling main() function 
	main() 
