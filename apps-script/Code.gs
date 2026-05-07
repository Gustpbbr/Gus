/**
 * Gus Sync (GitHub <-> Drive) — entry points e orquestração.
 *
 * Fonte da verdade roda no Apps Script. Cópia de referência em
 * apps-script/ no repo Gustpbbr/Gus. Pra editar: muda aqui no repo,
 * cola no Editor do Apps Script (ctrl+A, ctrl+V), salva.
 *
 * Triggers:
 *   safeSyncGitHubToDrive — time-driven, every 15 minutes
 *   safeSyncDriveToGitHub — time-driven, every 15 minutes
 */

const TIME_BUDGET_MS = 4 * 60 * 1000; // 4 min de 6 max — folga pra cleanup


// ============================================================================
// Wrappers seguros (chamados pelos triggers)
// ============================================================================

function safeSyncGitHubToDrive() {
  try {
    const stats = syncGitHubToDrive();
    Logger.log('GH→Drive OK: ' + JSON.stringify(stats));
  } catch (e) {
    sendTelegramAlert('❌ Apps Script GH→Drive falhou\n' + e.message);
    throw e;
  }
}

function safeSyncDriveToGitHub() {
  try {
    const stats = syncDriveToGitHub();
    Logger.log('Drive→GH OK: ' + JSON.stringify(stats));
  } catch (e) {
    sendTelegramAlert('❌ Apps Script Drive→GH falhou\n' + e.message);
    throw e;
  }
}


// ============================================================================
// GitHub → Drive
// ============================================================================

function syncGitHubToDrive() {
  const startMs = Date.now();
  const props = PropertiesService.getScriptProperties();

  // Pode haver fila pendente de execução anterior estourada
  let pending = JSON.parse(props.getProperty('GH_PENDING_FILES') || '[]');

  if (pending.length === 0) {
    const lastSha = props.getProperty('LAST_SYNCED_SHA') || '';
    const head = ghGetHeadSha();

    if (!lastSha) {
      // Bootstrap: sincroniza tudo do repo
      pending = ghListAllRepoFiles().filter(p => !isExcluded(p));
      Logger.log('Bootstrap: ' + pending.length + ' arquivos a sincronizar');
    } else if (lastSha === head) {
      return { changed: 0, head: head.slice(0, 7) };
    } else {
      pending = ghGetChangedFiles(lastSha, head).filter(p => !isExcluded(p));
      Logger.log(pending.length + ' arquivos mudados ' + lastSha.slice(0,7) + '..' + head.slice(0,7));
    }
    props.setProperty('TARGET_HEAD', head);
  } else {
    Logger.log('Retomando fila pendente: ' + pending.length + ' arquivos');
  }

  const stats = { created: 0, updated: 0, unchanged: 0, error: 0 };
  const errors = [];

  while (pending.length > 0 && (Date.now() - startMs) < TIME_BUDGET_MS) {
    const path = pending.shift();
    try {
      const content = ghFetchFileContent(path);
      const result = driveUpsert(path, content);
      stats[result] = (stats[result] || 0) + 1;
    } catch (e) {
      stats.error += 1;
      errors.push(path + ': ' + e.message);
      Logger.log('ERRO ' + path + ': ' + e.message);
    }
  }

  // Salva progresso
  props.setProperty('GH_PENDING_FILES', JSON.stringify(pending));
  if (pending.length === 0) {
    const target = props.getProperty('TARGET_HEAD');
    if (target) {
      props.setProperty('LAST_SYNCED_SHA', target);
      props.deleteProperty('TARGET_HEAD');
    }
  }

  if (errors.length > 0 && errors.length >= stats.created + stats.updated) {
    // Mais erros que sucessos — alerta
    sendTelegramAlert('⚠️ GH→Drive: ' + errors.length + ' erros\n' + errors.slice(0, 3).join('\n'));
  }

  return Object.assign(stats, { remaining: pending.length });
}


// ============================================================================
// Drive → GitHub
// ============================================================================

function syncDriveToGitHub() {
  const startMs = Date.now();
  const props = PropertiesService.getScriptProperties();
  const lastScanAt = parseInt(props.getProperty('LAST_DRIVE_SCAN_AT') || '0', 10);
  const scanStartedMs = Date.now();

  const rootId = props.getProperty('DRIVE_ROOT_FOLDER_ID');
  if (!rootId) throw new Error('DRIVE_ROOT_FOLDER_ID ausente');

  const dialogosId = driveFindFolderByPath(rootId, 'dialogos');
  if (!dialogosId) {
    Logger.log('Pasta dialogos/ não existe no Drive — nada a fazer');
    props.setProperty('LAST_DRIVE_SCAN_AT', scanStartedMs.toString());
    return { changed: 0 };
  }

  const stats = { imported: 0, mirror_created: 0, mirror_updated: 0, mirror_unchanged: 0, invalid: 0, error: 0 };

  driveWalkRecursive(dialogosId, '', lastScanAt, function (file, prefix) {
    if (Date.now() - startMs > TIME_BUDGET_MS) return false; // stop walk

    const name = file.getName();
    try {
      const inboxName = isInboxTopLevel(prefix, name);
      if (inboxName) {
        const r = processarDemandaInbox(file, inboxName);
        stats[r] = (stats[r] || 0) + 1;
      } else {
        const r = processarMirror(file, prefix);
        stats['mirror_' + r] = (stats['mirror_' + r] || 0) + 1;
      }
    } catch (e) {
      stats.error += 1;
      Logger.log('ERRO ' + prefix + name + ': ' + e.message);
    }
    return true;
  });

  // Avança ponteiro só se completou a varredura sem estourar tempo
  if (Date.now() - startMs <= TIME_BUDGET_MS) {
    props.setProperty('LAST_DRIVE_SCAN_AT', scanStartedMs.toString());
  } else {
    Logger.log('Time budget estourou — não avança LAST_DRIVE_SCAN_AT pra retomar próxima exec');
  }

  return stats;
}


// ============================================================================
// Setup helpers (rodar manual no Editor)
// ============================================================================

/**
 * Roda manualmente no Editor pra validar Properties + auth + APIs.
 * Use quando: primeira vez, ou após mudar Properties.
 */
function setupCheck() {
  const required = ['GITHUB_TOKEN', 'GITHUB_OWNER', 'GITHUB_REPO', 'GITHUB_BRANCH', 'DRIVE_ROOT_FOLDER_ID'];
  const props = PropertiesService.getScriptProperties();
  const missing = required.filter(k => !props.getProperty(k));
  if (missing.length > 0) {
    throw new Error('Properties faltando: ' + missing.join(', '));
  }

  // Testa GitHub
  const head = ghGetHeadSha();
  Logger.log('GitHub OK. HEAD = ' + head);

  // Testa Drive
  const rootId = props.getProperty('DRIVE_ROOT_FOLDER_ID');
  const folder = DriveApp.getFolderById(rootId);
  Logger.log('Drive OK. Pasta = ' + folder.getName());

  // Testa Telegram (opcional)
  if (props.getProperty('TELEGRAM_BOT_TOKEN')) {
    sendTelegramAlert('🔧 Apps Script setup check OK');
    Logger.log('Telegram OK (mensagem enviada)');
  } else {
    Logger.log('Telegram não configurado (opcional)');
  }

  Logger.log('✅ Setup check passou');
}

/**
 * Reset state — força re-bootstrap na próxima exec.
 * Use quando: quer redo full sync GitHub→Drive, ou após mudar repo.
 */
function resetState() {
  const props = PropertiesService.getScriptProperties();
  props.deleteProperty('LAST_SYNCED_SHA');
  props.deleteProperty('GH_PENDING_FILES');
  props.deleteProperty('TARGET_HEAD');
  props.deleteProperty('LAST_DRIVE_SCAN_AT');
  Logger.log('State resetado. Próxima exec faz bootstrap.');
}
