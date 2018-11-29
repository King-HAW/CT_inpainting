import SimpleITK as sitk
import os
import numpy as np
import cv2
import matplotlib
import matplotlib.pyplot as plt


path = '/home/jiayu/Data/Liver_CT_Dongming/liver_image/test/'
test_data_path = '/home/jiayu/Data/Liver_CT_Dongming/Prob.nii'
test_data_mask_path = '/home/jiayu/Data/Liver_CT_Dongming/Prob_seg.nii.gz'
data_name = '10_CT.nii.gz'

# Get Img from data for training
for i in range(12):
    data_name = str(i+1) + '_CT.nii.gz'
    img_data = sitk.ReadImage(path + data_name)
    img = sitk.GetArrayFromImage(img_data)
    print(img.shape)

    for j in range(img.shape[0]):
        slice = np.rot90(img[j, :, :], k=2)
        slice1 = ((slice - np.min(slice)) / (np.max(slice) - np.min(slice))) * 255
        slice2 = np.expand_dims(slice1, axis=2)
        slice_rgb = np.concatenate((slice2, slice2, slice2), axis=-1)
        cv2.imwrite(path + 'Image/{}_CT_{}.png'.format(i+1, j+1), slice_rgb, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])


print('Done!')

# Get Img from data for test
test_data = sitk.ReadImage(test_data_path)
test_mask = sitk.ReadImage(test_data_mask_path)
img = sitk.GetArrayFromImage(test_data)
mask = sitk.GetArrayFromImage(test_mask)

img_shape = img.shape
print(img_shape)
mask_shape = mask.shape
print(mask_shape)

[slice_index] = np.where(np.sum(mask, axis=tuple([1, 2])) != 0)
# a = np.sum(mask, axis=tuple([1, 2]))
print(slice_index)

count = 1

for i in slice_index:
    mask_tmp = mask[i, :, :]
    img_tmp = img[i, :, :]
    # mask1 = mask[0]
    # print(mask_tmp.shape)
    print('slice_{}: {}'.format(i, np.sum(mask_tmp)))
    # mask_tmp = np.rot90(mask_tmp, k=2)
    # img_tmp = np.rot90(img_tmp, k=2)
    mask_tmp = mask_tmp[::-1]
    mask_tmp = mask_tmp * 1.
    img_tmp = img_tmp[::-1]
    img_tmp = ((img_tmp - np.min(img_tmp)) / (np.max(img_tmp) - np.min(img_tmp))) * 255
    # plt.figure()
    # plt.imshow(mask_tmp, cmap='gray')
    # plt.show()
    # pass
    mask_tmp1 = np.expand_dims(mask_tmp, axis=2)
    mask_rgb = np.concatenate((mask_tmp1, mask_tmp1, mask_tmp1), axis=-1)
    # cv2.imwrite(path + 'ct/mask/test_CT_{}.png'.format(i), mask_rgb, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    matplotlib.image.imsave(path + 'ct/mask/test_CT_{}.png'.format(count), mask_rgb)

    img_tmp1 = np.expand_dims(img_tmp, axis=2)
    img_rgb = np.concatenate((img_tmp1, img_tmp1, img_tmp1), axis=-1)
    cv2.imwrite(path + 'ct/img/test_CT_{}.png'.format(count), img_rgb, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    count += 1
