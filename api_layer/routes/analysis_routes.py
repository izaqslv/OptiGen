from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import subprocess
import os
import base64
import sys

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


@router.get("/plots")
def generate_and_get_plots():
    """
    Executa run_analysis.py como script externo
    e retorna os gráficos gerados.

     NÃO altera código existente
     Usa pipeline atual validado
     Estrutura robusta (produção)
    """

    try:
        #  1. Executa script existente (SEM alterar nada)
        # OBS: para ver os gráficos com matplotlib: ative abaixo (até a linha indicada)
        # subprocess.run(
        #   ["python", "-m", "model_layer.analysis.run_analysis"],
        #   [sys.executable, "-m", "model_layer.analysis.run_analysis"],
        # Ou, para rodar sem ver os gráficos (idela para quando estiver no frontend), ativar anaixo:
        # cria ambiente isolado para execução:
        env=os.environ.copy()
        # força o matplotlib a rodar sem interface gráfica (HEADLESS)
        env["MPLBACKEND"] = "Agg"
        # executa o script sem abrir janelas de gráfico
        subprocess.run(
            [sys.executable, "-m", "model_layer.analysis.run_analysis"],
            check=True,
            env=env,
            # cwd=os.getcwd()
        )

        #  2. Diretório onde os gráficos são salvos
        output_dir = "model_layer/analysis/outputs/plots"

        if not os.path.exists(output_dir):
            raise Exception("Diretório de saída não encontrado.")

        plots = []

        #  3. Lê imagens geradas
        for file in os.listdir(output_dir):
            if file.endswith(".png"):
                file_path = os.path.join(output_dir, file)

                with open(file_path, "rb") as f:
                    img_base64 = base64.b64encode(f.read()).decode("utf-8")

                plots.append({
                    "filename": file,
                    "image": img_base64
                })

        if not plots:
            raise Exception("Nenhum gráfico foi gerado.")

        return JSONResponse(content={"plots": plots})

    except subprocess.CalledProcessError:
        raise HTTPException(
            status_code=500,
            detail="Erro ao executar run_analysis.py"
        )

    # except Exception as e:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=str(e)
    #     )

    except Exception as e:
        import traceback
        print(traceback.format_exc())  # 🔥 mostra erro real no terminal

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
