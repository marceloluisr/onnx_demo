# onnx_demo

# Requerimentos
.
- JAVA OpenJDK 17 instalado e variável JAVA_HOME configurada apropridamente em gradle.properties
- Android SDK instalado e caminho de deretório no arquivo local.properties. Se não existir, então crie um local.properties na pasta do projeto
  
> Conectar USB com Depurador USB ativado no modo desenvolvedor

> Connectar adb device

adb devices

# Comandos de execução

> Instalar o apk debug no celular

./gradlew installDebug

> Copiar modelo para a pasta temporária do celular (dependendo do celular tudo será apagado depois da reinicialização)

adb push model.onnx /data/local/tmp/model.onnx

> Executar programa 

adb shell am start -W -S -n ai.onnxruntime.example.imageclassifier/.MainActivity


> Ver log

adb logcat SODBenchmark:D *:S

> Parar programa 

adb kill-server

> Ver erros

adb logcat AndroidRuntime:E *:S
adb logcat -v time -b crash > crash_log.txt

> Limpar ou visualizar logs 

adb logcat -c 
adb logcat YourAppTag:E *:S




# Problemas comuns  

### Se depois de fazer o reboot do celular, o modelos *.pte colocados na pasta temporária do Android não foram apagados, então faça

1) Listar arquivos da pasta /data/local/temp

adb shell ls -l /data/local/tmp/


2) Remover os arquivos com o seguinte comando, por exemplo

adb shell rm /data/local/tmp/YOUR_MODEL.onnx

ou para remover todos os modelos

adb shell rm /data/local/tmp/*.onnx

# Exemplo de conversão
Recomendação: **precisar carregar os pesos do modelo com `load_state_dict()` antes de exportar para ONNX**, caso contrário o modelo estará com pesos aleatórios (não treinado).
```python
import torch
import torch.onnx

# Cria o modelo
model = U2NET()

# Carrega os pesos treinados
model.load_state_dict(torch.load("u2net.pth", map_location='cpu'))  # ajuste o caminho se necessário

# Define o modo de avaliação
model.eval()

# Entrada dummy
dummy_input = torch.randn(1, 3, 224, 224)

# Exporta para ONNX
torch.onnx.export(
    model,
    dummy_input,
    "u2net.onnx",
    export_params=True,
    opset_version=11,
    do_constant_folding=True,
    input_names=['input'],
    output_names=['out1', 'out2', 'out3', 'out4', 'out5', 'out6'],
    dynamic_axes={
        'input': {0: 'batch_size'},
        'out1': {0: 'batch_size'},
        'out2': {0: 'batch_size'},
        'out3': {0: 'batch_size'},
        'out4': {0: 'batch_size'},
        'out5': {0: 'batch_size'},
        'out6': {0: 'batch_size'},
    }
)
print(" Modelo ONNX exportado com sucesso!")
```

# Reconhecimento

https://github.com/xuebinqin/U-2-Net

