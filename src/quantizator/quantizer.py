from abc import abstractmethod

import copy

import numpy as np

import quantizator.util as util


class Quantizer:
    """
    Classe abstrata que representa um algorítmo de quantização de cores de uma imagem.
    A imagem a ser quantizada é mesma passada como parâmetro no construtor de um objeto que herda esta classe.
    """

    def __init__(self, img):
        self.img = img

    @abstractmethod
    def quantize(self, n):
        pass


class SimpleQuantizer(Quantizer):
    """
    Implementação do Quantizer utilizando um algorítmo de quantização simples.
    """

    def quantize(self, n):
        nums = util.nmult(n)
        print('Iniciando quantização uniforme com %d cores divididas em RGB(%d, %d, %d) ...' % (
        n, nums[0], nums[1], nums[2]))

        m = np.amax(self.img) + 1
        rgb = np.zeros(self.img.shape, 'uint8')
        for i in range(3):
            aux = np.uint8(self.img[..., i] * float(nums[i] / m))
            rgb[..., i] = np.uint8(127 if nums[i] == 1 else (aux / (nums[i] - 1.)) * 255)

        return rgb


class UniformQuantizer(Quantizer):
    """
    Implementação da Quantização Uniforme
    """

    def quantize(self, n):

        aux = copy.deepcopy(n)
        rgbarray = util.nmult(n)

        # gera o código das cores. quantidade de códigos = ncolors
        a = np.linspace(0, 255, num=rgbarray[0], dtype=int)
        b = np.linspace(0, 255, num=rgbarray[1], dtype=int)
        c = np.linspace(0, 255, num=rgbarray[2], dtype=int)

        palheta = np.array(np.meshgrid(a, b, c)).T.reshape(-1, 3)
        return util.aprox(self.img, palheta).astype('uint8')


class MedianCutQuantizer(Quantizer):
    """
    Implementação do Quantizer utilizando um algorítmo de quantização que usa mediancut.
    """

    def quantize(self, n):
        bucket = []
        palheta = []
        dispersao = []
        # pega rgb de todos pixels e coloca em um array ordenado
        # esse array é jogado em um bucket

        colors = np.concatenate(self.img[:, :], axis=0)
        colors = np.unique(colors, axis=0)

        # descobre qual cor tem a maior dispersão e ordena
        for i in range(3):
            dispersao.append(np.amax(colors[:, i]) - np.amin(colors[:, i]))
        dispersao_key = dispersao.index(max(dispersao))
        colors = sorted(colors, key=lambda x: x[dispersao_key])

        bucket.append(colors)

        # divide o bucket original em n buckets em que n = numero de cores
        while len(bucket) < n:
            tamanho = len(bucket)
            new_bucket = []
            for i in range(tamanho):
                bk = np.array(bucket[i], 'uint8')
                meio = util.argmedian(bk, dispersao_key)
                a = bk[:meio]
                b = bk[meio:]
                new_bucket.append(a)
                new_bucket.append(b)
            bucket = new_bucket

        # Palheta pelo pixel do meio
        # identifica a cor mediana para cada um dos buckets de cor
        for i in range(len(bucket)):
            bk = np.array(bucket[i], 'uint8')
            meio = util.argmedian(bk, dispersao_key)
            palheta.append(bk[meio])

        return util.aprox(self.img, palheta)
