import torch
from modelscope import snapshot_download, AutoModel, AutoTokenizer
import os
model_dir = snapshot_download('Qwen/Qwen2.5-7B-Instruct', cache_dir='/path/to/your/cache/dir', revision='master')