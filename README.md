# Quantizator
Programa simples escrito em Python 3 para a aplicação de quantização de cores em imagens.

## Métodos
Este programa possúi três métodos implementados para a quantização de cores:
- Quantização uniforme com normalização;
- Quantização uniforme com espaço linear;
- Quantização median cut;

Cada uma destas implementações foi escrita separadamente em classes: _SimpleQuantizer, UniformQuantizer e MedianCutQuantizer_ reespectivamente.
<br><br>
Para o uso destes métodos, basta istânciar a respectiva classe, passando para o contrutor a imagem a ser quantizada, e em seguida utilizar o método _quantize_, passando como parâmetro o número de cores que a imagem passará a ter.

## Execução
Antes de se executar o programa, é necessário instalar as seguintes dependências:
- _numpy_
- _opencv-python_

Com as dependências instaladas, realize os seguintes passos:
1. Navegue até a pasta _"quantizator/src"_;
2. Abra o terminal de comandos e execute: "_python3 -m quantizator.app -i IE -o IS -a ME -n ND_", onde:
   - IE: caminho da imagem a ser quantizada;
   - IS: caminho da imagem quantizada a ser salva;
   - ME: método de quantização (_simple_, _uniform_, ou _mediancut_);
   - ND: múmero de cores que a imagem será reduzida;