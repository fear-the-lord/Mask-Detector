# Import the necessary dependencies
import os 

# Function to rename multiple files 
def main(): 
	# Loop over all the files in the source directory
	for count, filename in enumerate(os.listdir("dataset/without_mask")): 
		# Provide the name with which the files are to be renamed
		dst = "img" + str(count) + ".jpg"
		# Provide the source path
		src = 'dataset/without_mask/' + filename 
		# Provide the destination path
		dst = 'dataset/without_mask/' + dst
		
		# rename() function will rename all the files
		print("Renaming: ", src, "->", dst) 
		os.rename(src, dst) 
	print("[INFO] Images Renamed Successfully...")

# Driver Code 
if __name__ == '__main__': 
	# Calling main() function 
	main() 