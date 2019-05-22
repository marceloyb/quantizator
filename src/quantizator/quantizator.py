import numpy as np
import cv2 as cv


def nmult(n):
    if n <= 1:
        return [1, 1, 1]

    c = n
    nums = []

    for i in range(2, n + 1):
        while c % i == 0:
            nums.append(i)
            c /= i

    if len(nums) == 1:
        nums = [nums[0], 1, 1]
    if len(nums) == 2:
        nums = [nums[0], nums[1], 1]
    if len(nums) > 3:
        while len(nums) > 3:
            i1 = np.argmin(nums)
            n1 = nums[i1]
            nums.pop(i1)
            i2 = np.argmin(nums)
            nums[i2] *= n1

    return nums


def quantize(img, n=2):
    nums = nmult(n)
    print('Starting quantization using %d colors with RGB(%d, %d, %d) ...' % (n, nums[0], nums[1], nums[2]))
    m = np.amax(img) + 1
    r = np.uint8(img[..., 0] * (1 / (m / float(nums[0]))))
    g = np.uint8(img[..., 1] * (1 / (m / float(nums[1]))))
    b = np.uint8(img[..., 2] * (1 / (m / float(nums[2]))))

    rgb = np.zeros(img.shape, 'uint8')

    rn = nums[0] - 1. if nums[0] - 1. != 0 else 0.01
    gn = nums[1] - 1. if nums[1] - 1. != 0 else 0.01
    bn = nums[2] - 1. if nums[2] - 1. != 0 else 0.01

    rgb[..., 0] = np.uint8((r / rn) * 255)
    rgb[..., 1] = np.uint8((g / gn) * 255)
    rgb[..., 2] = np.uint8((b / bn) * 255)
    print('Quantization finished.')
    return rgb


def main():
    path = 'lena.bmp'
    print('Running quantization for \"' + path + "\"")
    img = cv.imread(path)
    img_qt = quantize(img, 256)
    print('Plot images ...')
    cv.imshow('Lena', img)
    cv.imshow('Lena Quantized', img_qt)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
