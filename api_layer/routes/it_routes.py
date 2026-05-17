from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
import shutil
from module_it_alumar.it_orchestrator import ITOrchestrator

router = APIRouter(
    prefix="/it",
    tags=["Work Instructions (IT)"]
)

# Inicialização do Orquestrador com diretório de saída padronizado
orchestrator = ITOrchestrator(output_dir="data/generated_its")
TEMP_UPLOAD_DIR = "data/temp_uploads"
os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)


@router.post("/generate")
async def generate_from_file(
        file: UploadFile = File(...),
        filename_prefix: str = Form("IT_Alumar")
):
    """
    Endpoint Profissional: Recebe qualquer arquivo (Áudio, Vídeo, PDF, Word)
    e retorna a IT estruturada + PDF oficial + Word editável.
    """
    temp_path = os.path.join(TEMP_UPLOAD_DIR, file.filename)

    try:
        # Salva o arquivo temporariamente para processamento
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Detecta o tipo de entrada para orientar a IA
        ext = file.filename.split(".")[-1].lower()
        input_type = "document" if ext in ["pdf", "docx"] else "media"

        # Orquestra o processamento completo (Geração de Dados, PDF e Word)
        result = orchestrator.process_and_generate(
            file_path=temp_path,
            input_type=input_type,
            filename_prefix=filename_prefix
        )

        return {
            "message": "Processamento concluído com sucesso",
            "data": result["data"],
            "pdf_url": result["pdf_url"],
            "word_url": result["word_url"]  # <-- Suporte ao Word adicionado
        }

    except Exception as e:
        print(f"ERRO CRÍTICO NO MÓDULO IT: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Falha no processamento: {str(e)}")

    finally:
        # Limpa o arquivo temporário para manter a saúde do servidor
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.get("/download/{filename}")
async def download_it_file(filename: str):
    """
    Endpoint de Download: Suporta tanto PDF quanto DOCX (Word).
    """
    file_path = os.path.join("data/generated_its", filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    # Define o media_type dinamicamente com base na extensão
    ext = filename.split(".")[-1].lower()
    media_type = 'application/pdf' if ext == 'pdf' else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=media_type
    )