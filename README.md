# YouTube Downloader

O **YouTube Downloader** é uma aplicação simples e intuitiva desenvolvida em Python, utilizando a biblioteca Tkinter para a interface gráfica. Este aplicativo permite aos usuários baixar vídeos do YouTube em formatos de vídeo (.mp4) e áudio (.mp3), com diferentes opções de qualidade.

## Funcionalidades

- **Download de Vídeos e Áudios**: Permite baixar vídeos do YouTube em formato .mp4 e extrair o áudio em formato .mp3.
- **Escolha de Qualidade**: Oferece várias opções de qualidade de vídeo, incluindo 360p, 480p, 720p, 1080p e a melhor qualidade disponível.
- **Gerenciamento de Downloads**: Salva os arquivos baixados em uma pasta específica e exibe os downloads recentes com miniaturas.
- **Configuração de Pasta de Destino**: Possibilidade de escolher a pasta de destino para os downloads ou usar uma pasta padrão dentro do diretório do aplicativo.
- **Barra de Progresso**: Exibe o progresso do download em tempo real.

## Requisitos

- Python 3.x
- Bibliotecas: pytube, pillow, pydub, requests

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/m1ttes1/YTB-Video-downloader.git
    cd YTB-Video-downloader
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`

    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Execute o script principal:
    ```bash
    python video_downloader.py
    ```

2. Insira a URL do vídeo do YouTube que deseja baixar.
3. Escolha o formato (vídeo ou áudio) e a qualidade desejada.
4. Clique em "Baixar" e aguarde a conclusão do download.


