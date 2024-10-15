# 環境變數設定

在運行應用程式之前，您可以選擇性地設置以下環境變數：

- `BATCH_SIZE`: 設定影片生成時(frame)的批次大小，預設值為 `4`。
- `SERVER_PORT`: 設定伺服器運行的端口，預設值為 `7860`。

您可以在命令行中使用以下命令設置環境變數：

```bash
export BATCH_SIZE=4
export SERVER_PORT=7860
```

## 如何運行

### 使用 Python

確保您已經安裝了所有必要的依賴項，然後在命令行中運行以下命令來啟動應用程式：

```bash
python app.py
```

這將啟動 Gradio 應用程式，並在指定的端口上運行。

### 使用 Docker

您可以直接從 Docker Hub 拉取並運行映像：

1. 拉取 Docker 映像：

   ```bash
   docker pull royyang1203/sadtalker
   ```

2. 運行 Docker 容器：

   ```bash
   docker run -it --gpus all -p 7860:7860 -e BATCH_SIZE=4 -e SERVER_PORT=7860 royyang1203/sadtalker
   ```

這將在 Docker 容器中啟動 Gradio 應用程式，並在指定的端口上運行。
