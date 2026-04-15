import os
import anthropic
from pathlib import Path
from gus.tools import TOOLS, executar_tool

# Preços Sonnet 4.6 (por token)
COST_INPUT = 3.0 / 1_000_000
COST_OUTPUT = 15.0 / 1_000_000

client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


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

    # Loop de tool calling — continua até Claude retornar texto final
    while True:
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
            cost_usd = round((total_in * COST_INPUT) + (total_out * COST_OUTPUT), 6)
            metadata = {
                "model": model,
                "tokens_in": total_in,
                "tokens_out": total_out,
                "cost_usd": cost_usd
            }
            return text, metadata
