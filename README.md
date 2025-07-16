# executorch_demo

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

adb shell rm /data/local/tmp/YOUR_MODEL.pte



