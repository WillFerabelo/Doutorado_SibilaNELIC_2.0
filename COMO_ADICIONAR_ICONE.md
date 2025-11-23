# Como Adicionar um Ícone Personalizado ao Sistema NELIC

## Passo 1: Preparar a Imagem do Ícone

1. Escolha uma imagem (PNG, JPG, etc.) que represente o sistema
2. A imagem deve ter pelo menos 1024x1024 pixels para melhor qualidade
3. Idealmente, use uma imagem quadrada com fundo transparente (PNG)

## Passo 2: Converter a Imagem para .icns (formato de ícone do macOS)

### Opção A: Usando o Preview (Visualização) - Mais Simples

1. Abra a imagem no Preview
2. Redimensione para 1024x1024 pixels (Ferramentas → Ajustar Tamanho)
3. Copie a imagem (Cmd+A, depois Cmd+C)
4. Abra o Finder e vá até: `/Users/williamfernandes/Documents/Doutorado/Doutorado_SibilaNELIC_2.0/Sistema NELIC.app`
5. Clique com botão direito → "Obter Informações"
6. Clique no ícone pequeno no canto superior esquerdo da janela de informações
7. Cole a imagem copiada (Cmd+V)
8. Pronto! O ícone foi atualizado

### Opção B: Criar arquivo .icns profissional

Execute estes comandos no Terminal (substitua `/caminho/para/sua/imagem.png` pelo caminho real):

```bash
# 1. Criar pasta temporária para ícones
mkdir /tmp/icone.iconset

# 2. Criar várias resoluções (substitua o caminho da imagem)
sips -z 16 16     /caminho/para/sua/imagem.png --out /tmp/icone.iconset/icon_16x16.png
sips -z 32 32     /caminho/para/sua/imagem.png --out /tmp/icone.iconset/icon_16x16@2x.png
sips -z 32 32     /caminho/para/sua/imagem.png --out /tmp/icone.iconset/icon_32x32.png
sips -z 64 64     /caminho/para/sua/imagem.png --out /tmp/icone.iconset/icon_32x32@2x.png
sips -z 128 128   /caminho/para/sua/imagem.png --out /tmp/icone.iconset/icon_128x128.png
sips -z 256 256   /caminho/para/sua/imagem.png --out /tmp/icone.iconset/icon_128x128@2x.png
sips -z 256 256   /caminho/para/sua/imagem.png --out /tmp/icone.iconset/icon_256x256.png
sips -z 512 512   /caminho/para/sua/imagem.png --out /tmp/icone.iconset/icon_256x256@2x.png
sips -z 512 512   /caminho/para/sua/imagem.png --out /tmp/icone.iconset/icon_512x512.png
sips -z 1024 1024 /caminho/para/sua/imagem.png --out /tmp/icone.iconset/icon_512x512@2x.png

# 3. Converter para .icns
iconutil -c icns /tmp/icone.iconset -o "/Users/williamfernandes/Documents/Doutorado/Doutorado_SibilaNELIC_2.0/Sistema NELIC.app/Contents/Resources/AppIcon.icns"

# 4. Limpar arquivos temporários
rm -rf /tmp/icone.iconset
```

## Passo 3: Atualizar o Sistema

Depois de adicionar o ícone, execute:

```bash
# Atualizar cache de ícones do macOS
touch "/Users/williamfernandes/Documents/Doutorado/Doutorado_SibilaNELIC_2.0/Sistema NELIC.app"
killall Dock
killall Finder
```

## Sugestões de Ícones

Você pode:
- Usar o logo do NELIC (se houver)
- Criar um ícone com as letras "NELIC"
- Usar símbolos relacionados a biblioteca/arquivo/livros
- Buscar ícones gratuitos em sites como:
  - https://www.flaticon.com
  - https://iconarchive.com
  - https://www.iconfinder.com

## Onde Está o Aplicativo?

O aplicativo foi criado em:
`/Users/williamfernandes/Documents/Doutorado/Doutorado_SibilaNELIC_2.0/Sistema NELIC.app`

Você pode:
- Arrastar para o Dock
- Copiar para a pasta Aplicativos (/Applications)
- Copiar para a Área de Trabalho
- Criar um atalho em qualquer lugar
