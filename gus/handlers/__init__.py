"""Pacote de handlers do bot Telegram.

Cada handler em seu próprio módulo (text, photo, document, voice, commands)
pra modularidade. Lógica compartilhada entre eles em `gus.handlers.responder`.

Re-exportado em `gus.bot` pra preservar API antiga
(`from gus.bot import handle_message, handle_photo, ...`).
"""
