import os
import functools
import anthropic
from pathlib import Path
from gus.tools import TOOLS, executar_tool

# Preços por família de modelo (USD por token)
MODEL_PRICING = {
    "opus":   {"input": 15.0 / 1_000_000, "output": 75.0 / 1_000_000},
    "sonnet": {"input":  3.0 / 1_000_000, "output": 15.0 / 1_000_000},
    "haiku":  {"input":  0.8 / 1_000_000, "output":  4.0 / 1_000_000},
}
FALLBACK_PRICING = MODEL_PRICING["sonnet"]


def _get_pricing(model: str) -> dict:
    """Retorna pricing baseado no nome do modelo."""
    model_lower = model.lower()
    for family, pricing in MODEL_PRICING.items():
        if family in model_lower:
            return pricing
    return FALLBACK_PRICING

client = anthropic.AsyncAnthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    timeout=120.0,  # 2 minutos — evita ficar pendurado se a API travar
)


@functools.lru_cache(maxsize=1)
def _load_system_prompt() -> str:
    path = Path(__file__).parent / "system_prompt.md"
    return path.read_text(encoding="utf-8")


async def gerar_resposta(messages: list[dict], memory_context: str = "") -> tuple[str, dict]:
    model = os.getenv("MODEL_DEFAULT", "claude-sonnet-4-6")
    max_tokens = int(os.getenv("MAX_TOKENS_RESPONSE", "2048"))

    system_prompt = _load_system_prompt()
    if memory_context:
        system_prompt += f"\n\n## Memórias relevantes\n{memory_context}"

    total_in = 0
    total_out = 0
    current_messages = list(messages)
    max_tool_rounds = 10

    # Loop de tool calling — continua até Claude retornar texto final
    for _ in range(max_tool_rounds):
        response = await client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=current_messages,
            tools=TOOLS
        )

        total_in += response.usage.input_tokens
        total_out += response.usage.output_tokens

        if response.stop_reason == "tool_use":
            # Executa as tools e continua o loop
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = await executar_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            current_messages = current_messages + [
                {"role": "assistant", "content": response.content},
                {"role": "user", "content": tool_results}
            ]
        else:
            # Resposta final em texto
            text = next(
                (b.text for b in response.content if hasattr(b, "text")),
                ""
            )
            pricing = _get_pricing(model)
            cost_usd = round((total_in * pricing["input"]) + (total_out * pricing["output"]), 6)
            metadata = {
                "model": model,
                "tokens_in": total_in,
                "tokens_out": total_out,
                "cost_usd": cost_usd
            }
            return text, metadata

    # Saída de segurança se o loop de tools esgotar
    pricing = _get_pricing(model)
    cost_usd = round((total_in * pricing["input"]) + (total_out * pricing["output"]), 6)
    return "Desculpa, entrei em loop interno. Tenta reformular.", {
        "model": model, "tokens_in": total_in,
        "tokens_out": total_out, "cost_usd": cost_usd
    }
