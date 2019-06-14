import quantizator.quantizer as quant
import cv2 as cv
import argparse

from quantizator import util


def define_args():
    parser = argparse.ArgumentParser(description='Aplica um algorítmo de quantização a uma dada imagem.')
    parser.add_argument('-i', dest='input', type=str, default='./input.png',
                        help='O caminho até a imagem que será quantizada.')
    parser.add_argument('-o', dest='output', type=str,
                        help='O caminho onde a imagem quantizada será escrita.')
    parser.add_argument('-a', dest='algorithm', type=str, default='uniform',
                        help='O algorítmo a ser utilizado para a quantização.')
    parser.add_argument('-n', dest='number', type=int, default='256',
                        help='O número de cores a ser feito a quantização.')
    return parser.parse_args()


def show(*img_defs):
    for img_def in img_defs:
        cv.imshow(img_def[0], img_def[1])


def wait():
    cv.waitKey(0)
    cv.destroyAllWindows()


def main():
    args = define_args()

    print('Aplicando quantização em \"%s\" usando o algorítmo %s.' % (args.input, args.algorithm))

    img = cv.imread(args.input)

    # Escolhe o algorítmo que será utilizado na quantização
    qnt = None
    if args.algorithm == 'simple':
        qnt = quant.SimpleQuantizer(img)
    elif args.algorithm == 'uniform':
        qnt = quant.UniformQuantizer(img)
    elif args.algorithm == 'mediancut':
        qnt = quant.MedianCutQuantizer(img)
    else:
        raise RuntimeError('O método de quantização %s não é um método válido.' % args.algorithm)

    # Aplica quantização
    qnt_img = qnt.quantize(args.number)

    # Grava a imagem em um arquivo de saída se necessário
    if args.output is not None:
        cv.imwrite(args.output, qnt_img)

    cpsrn = util.psnr(img, qnt_img)
    print('Color Peak Signal to Noise-Ratio: %f' % cpsrn)

    show(('Input', img), ('Output', qnt_img))
    wait()


if __name__ == "__main__":
    main()
