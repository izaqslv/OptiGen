 OptiGen Backend

Motor de inteligência para análise e predição de sedimentação em fluidos de perfuração.

 Visão Geral

O OptiGen Backend é responsável por executar os modelos preditivos, processar dados experimentais e gerar análises estruturais completas com base em inteligência artificial.

Este serviço expõe uma API REST construída com FastAPI, sendo o núcleo computacional da plataforma OptiGen.

---

 Funcionalidades

-  Predição de perfis de concentração ao longo do tempo e altura
-  Geração automática de gráficos comparando dados experimentais vs preditos
-  Exportação de resultados em formato de imagem
-  Execução de pipeline científico completo
-  Autenticação via token (JWT)
-  Endpoint de análise avançada ("/analysis/plots")

---

 Arquitetura

API (FastAPI)
    ↓
Pipeline de dados
    ↓
Modelos neurais (PyTorch)
    ↓
Geração de gráficos (Matplotlib - headless)

---

 Principais Endpoints

Endpoint                            | Descrição
"/auth/login"                       | Autenticação
"/profiles/available_fluids"        | Lista de fluidos
"/profiles/available_heights"       | Alturas disponíveis
"/profiles/{fluid_id}/height/plot"  | Gráfico por altura
"/profiles/{fluid_id}/plot_all"     | Todas as alturas
"/analysis/plots"                   | Análise completa com IA

---

 Tecnologias

- FastAPI
- PyTorch
- Pandas / NumPy
- Matplotlib (modo headless)
- Joblib

---

 Execução Local

uvicorn api_layer.main:app --reload

Acesse:

http://127.0.0.1:8000/docs

---

 Deploy

- Backend hospedado no Render
- Pronto para migração futura para AWS

---

 Status do Projeto

 MVP funcional
 Pipeline validado com dados reais
 Integração com frontend concluída

---

 Roadmap

- [ ] Persistência de análises
- [ ] Execução assíncrona
- [ ] Versionamento de resultados
- [ ] Escalabilidade em cloud (AWS)

---

 Sobre

Desenvolvido pela NewGen Intelligent Engineering Solutions
Incubada na UNICAMP (INCAMP)

--- 
