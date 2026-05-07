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
  const opts = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({
      chat_id: chatId,
      text: message,
    }),
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
