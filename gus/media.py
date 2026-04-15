import base64
import asyncio
import logging
import httpx
from pypdf import PdfReader
from pdf2image import convert_from_bytes
from io import BytesIO

logger = logging.getLogger(__name__)

# Limite de caracteres de texto: ~150k tokens de folga no contexto do Claude
PDF_TEXT_LIMIT = 500_000
# Número máximo de páginas a renderizar como imagem (PDFs visuais)
PDF_IMAGE_MAX_PAGES = 10


async def _download(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=60)
        response.raise_for_status()
        return response.content


async def processar_imagem(file_url: str, caption: str = "") -> list[dict]:
    """Retorna bloco de conteúdo multimodal para Claude Vision."""
    data = await _download(file_url)
    b64 = base64.standard_b64encode(data).decode("utf-8")
    content = [
        {
            "type": "image",
            "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}
        }
    ]
    if caption:
        content.append({"type": "text", "text": caption})
    else:
        content.append({"type": "text", "text": "O que está nessa imagem? Descreva e comente o que for relevante."})
    return content


def _pdf_para_imagens(data: bytes, max_pages: int) -> list[str]:
    """Converte páginas do PDF em base64 JPEG via poppler."""
    images = convert_from_bytes(data, dpi=150, first_page=1, last_page=max_pages)
    result = []
    for img in images:
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=85)
        result.append(base64.standard_b64encode(buf.getvalue()).decode("utf-8"))
    return result


async def processar_pdf(file_url: str, caption: str = "") -> list[dict]:
    """
    Extrai texto do PDF. Se o texto for insuficiente (PDF visual/escaneado),
    renderiza as páginas como imagens e usa Claude Vision.
    """
    data = await _download(file_url)
    reader = PdfReader(BytesIO(data))
    total_pages = len(reader.pages)

    # Tenta extração de texto
    pages_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text.strip())
    texto_extraido = "\n\n---\n\n".join(pages_text)

    prompt = caption or "Analise este documento."

    # PDF com texto suficiente
    if len(texto_extraido) > 200:
        truncado = len(texto_extraido) > PDF_TEXT_LIMIT
        texto_final = texto_extraido[:PDF_TEXT_LIMIT]
        aviso = (
            f"\n\n[Documento truncado: {len(texto_extraido):,} caracteres, "
            f"enviando os primeiros {PDF_TEXT_LIMIT:,}]"
        ) if truncado else f"\n\n[{total_pages} páginas, {len(texto_extraido):,} caracteres]"
        return [{"type": "text", "text": f"{prompt}\n\n---\n\n{texto_final}{aviso}"}]

    # PDF visual (planta baixa, topografia, escaneado) — renderiza como imagens
    logger.info("PDF sem texto suficiente, renderizando como imagens")
    pages_to_render = min(total_pages, PDF_IMAGE_MAX_PAGES)

    try:
        b64_images = await asyncio.to_thread(_pdf_para_imagens, data, pages_to_render)
    except Exception as e:
        logger.error(f"Falha ao renderizar PDF como imagem: {e}")
        return [{"type": "text", "text": f"{prompt}\n\n[PDF sem texto extraível e falha na renderização: {e}]"}]

    content: list[dict] = []
    for b64 in b64_images:
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}
        })

    aviso_pages = f" (mostrando {pages_to_render} de {total_pages} páginas)" if total_pages > PDF_IMAGE_MAX_PAGES else ""
    content.append({"type": "text", "text": f"{prompt}{aviso_pages}"})
    return content
