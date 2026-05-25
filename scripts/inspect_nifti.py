import nibabel as nib


image_path = "example_data/MyBrain.nii.gz"

image = nib.load(image_path)

print("Shape:")
print(image.shape)

print("\nHeader:")
print(image.header)
