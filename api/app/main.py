from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API do Pipeline de Dados")

class BatchData(BaseModel):
    records: List[Dict[str, Any]]
    batch_id: str

@app.post("/api/v1/batch")
async def process_batch(batch: BatchData):
    """
    Processa um lote de registros (máximo de 500 registros por lote)
    """
    if len(batch.records) > 500:
        raise HTTPException(status_code=400, detail="O tamanho do lote não pode exceder 500 registros")
    
    try:
        # Registra o processamento do lote
        logger.info(f"Processando lote {batch.batch_id} com {len(batch.records)} registros")
        
        # TODO: Implementar lógica de processamento de dados aqui
        
        return {
            "status": "sucesso",
            "batch_id": batch.batch_id,
            "registros_processados": len(batch.records),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao processar lote {batch.batch_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Endpoint de verificação de saúde
    """
    return {"status": "saudável", "timestamp": datetime.utcnow().isoformat()} 