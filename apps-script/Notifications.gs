/**
 * Alertas via Telegram. Usa o mesmo bot @Tiogubot.
 *
 * Properties opcionais:
 *   TELEGRAM_BOT_TOKEN — token do bot
 *   TELEGRAM_CHAT_ID — chat ID pessoal do Gustavo
 *
 * Se ausentes, alerts são silenciosos (loga e segue).
 */


function sendTelegramAlert(message) {
  const props = PropertiesService.getScriptProperties();
  const token = props.getProperty('TELEGRAM_BOT_TOKEN');
  const chatId = props.getProperty('TELEGRAM_CHAT_ID');
  if (!token || !chatId) {
    Logger.log('Telegram secrets ausentes — alerta pulado: ' + message.slice(0, 100));
    return;
  }

  const url = 'https://api.telegram.org/bot' + token + '/sendMessage';
  // Apps Script + JSON tem quirk com chars não-ASCII (emoji etc) que pode
  // resultar em "Bad Request: message text is empty" no Telegram. Form-encoded
  // funciona estável e Telegram aceita os dois formatos.
  const opts = {
    method: 'post',
    payload: {
      chat_id: chatId,
      text: message,
    },
    muteHttpExceptions: true,
  };

  try {
    const resp = UrlFetchApp.fetch(url, opts);
    const code = resp.getResponseCode();
    if (code !== 200) {
      Logger.log('Telegram falhou (' + code + '): ' + resp.getContentText().slice(0, 200));
    }
  } catch (e) {
    Logger.log('Telegram erro: ' + e.message);
  }
}
