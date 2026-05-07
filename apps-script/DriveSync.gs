/**
 * Helpers DriveApp + lógica de inbox/mirror equivalente ao
 * .github/scripts/import_from_drive.py + sync_to_drive.py.
 *
 * Apps Script roda como o owner do projeto (Gustavo) → quota = sua,
 * sem fricção de Service Account.
 */


// ============================================================================
// Exclusions (paridade com sync_to_drive.py)
// ============================================================================

const EXCLUDE_PATHS = {
  'CLAUDE.md': true,
  'README.md': true,
  'gus/system_prompt.md': true,
  // Auditoria gigante (90k+ linhas), gerada por workflow. Não faz sentido
  // espelhar pro Drive — só inflou tempo de sync e quebrava em arquivos
  // > 1MB do GitHub Contents API.
  '_indices/_limpeza-hub-candidatos.md': true,
};

const EXCLUDE_PREFIXES = [
  'historico/',
  'gus/',
  '.github/',
  'sensivel/',
  'apps-script/',  // o próprio código não vai pro Drive
];

const INCLUDE_OVERRIDES = {
  'gus/gus-bootstrap.md': true,
  'gus/gus-identity.md': true,
};


// ============================================================================
// Constantes (paridade com import_from_drive.py)
// ============================================================================

const INBOXES = ['inbox-tiogu', 'inbox-claude-code', 'inbox-claude-chat', 'inbox-custom-gpt'];
const PROCESSADOS_FOLDER = 'processados';
const PROCESSADOS_ERRO_FOLDER = 'processados-erro';
const PORTAS_VALIDAS = {
  'claude-chat': true, 'tiogu': true, 'claude-code': true,
  'custom-gpt': true, 'gustavo': true,
};


// ============================================================================
// Path filtering
// ============================================================================

function isExcluded(path) {
  if (typeof path !== 'string') {
    Logger.log('isExcluded: path inválido (tipo ' + typeof path + '): ' + JSON.stringify(path));
    return true;  // Skip itens sem path válido em vez de quebrar
  }
  if (INCLUDE_OVERRIDES[path]) return false;
  if (EXCLUDE_PATHS[path]) return true;
  for (let i = 0; i < EXCLUDE_PREFIXES.length; i++) {
    if (path.indexOf(EXCLUDE_PREFIXES[i]) === 0) return true;
  }
  return false;
}


// ============================================================================
// Drive helpers
// ============================================================================

function driveGetRootId_() {
  const id = PropertiesService.getScriptProperties().getProperty('DRIVE_ROOT_FOLDER_ID');
  if (!id) throw new Error('DRIVE_ROOT_FOLDER_ID ausente');
  return id;
}


/**
 * Cria estrutura de pastas se necessário, retorna ID da pasta folha.
 * Idempotente — reusa pastas existentes.
 */
function driveEnsureFolderPath(rootId, relPath) {
  let parent = DriveApp.getFolderById(rootId);
  if (!relPath) return parent.getId();

  const parts = relPath.split('/').filter(Boolean);
  for (let i = 0; i < parts.length; i++) {
    const it = parent.getFoldersByName(parts[i]);
    if (it.hasNext()) {
      parent = it.next();
    } else {
      parent = parent.createFolder(parts[i]);
    }
  }
  return parent.getId();
}


/**
 * Resolve path tipo 'dialogos/inbox-tiogu' relativo a rootId. Retorna null se não existe.
 */
function driveFindFolderByPath(rootId, relPath) {
  let parent = DriveApp.getFolderById(rootId);
  const parts = relPath.split('/').filter(Boolean);
  for (let i = 0; i < parts.length; i++) {
    const it = parent.getFoldersByName(parts[i]);
    if (!it.hasNext()) return null;
    parent = it.next();
  }
  return parent.getId();
}


function driveFindFile(parentId, name) {
  const parent = DriveApp.getFolderById(parentId);
  const it = parent.getFilesByName(name);
  return it.hasNext() ? it.next() : null;
}


/**
 * Lê texto do arquivo. Pra Google Doc nativo, exporta como markdown.
 */
function driveReadAsText(file) {
  const mime = file.getMimeType();
  if (mime === MimeType.GOOGLE_DOCS) {
    const url = 'https://www.googleapis.com/drive/v3/files/' + file.getId() + '/export?mimeType=text/markdown';
    const resp = UrlFetchApp.fetch(url, {
      headers: { 'Authorization': 'Bearer ' + ScriptApp.getOAuthToken() },
      muteHttpExceptions: true,
    });
    if (resp.getResponseCode() < 200 || resp.getResponseCode() >= 300) {
      throw new Error('Export Google Doc falhou: ' + resp.getResponseCode());
    }
    return resp.getContentText('UTF-8');
  }
  return file.getBlob().getDataAsString('UTF-8');
}


/**
 * Cria ou atualiza arquivo no Drive. Idempotente.
 * Retorna: 'created' | 'updated' | 'unchanged'
 */
function driveUpsert(path, content) {
  const rootId = driveGetRootId_();
  const dirParts = path.split('/').slice(0, -1).join('/');
  const name = path.split('/').pop();
  const parentId = driveEnsureFolderPath(rootId, dirParts);

  const existing = driveFindFile(parentId, name);
  if (existing) {
    let current;
    try {
      current = driveReadAsText(existing);
    } catch (e) {
      Logger.log('driveReadAsText falhou (' + e.message + '), vai sobrescrever');
      current = null;
    }
    if (current === content) return 'unchanged';
    existing.setContent(content);
    return 'updated';
  }

  DriveApp.getFolderById(parentId).createFile(name, content, MimeType.PLAIN_TEXT);
  return 'created';
}


/**
 * Walk recursivo. Yield (file, prefix) pra cada file modificado depois de sinceMs.
 * Pula pastas processados/ e processados-erro/ no nível raiz.
 *
 * Callback retorna false → para a varredura.
 */
function driveWalkRecursive(folderId, prefix, sinceMs, callback) {
  const folder = DriveApp.getFolderById(folderId);

  // Files
  const files = folder.getFiles();
  while (files.hasNext()) {
    const f = files.next();
    if (sinceMs > 0 && f.getLastUpdated().getTime() < sinceMs) continue;
    if (callback(f, prefix) === false) return false;
  }

  // Subfolders
  const subs = folder.getFolders();
  while (subs.hasNext()) {
    const sub = subs.next();
    const subName = sub.getName();
    // Skip processados na raiz de dialogos/
    if (prefix === '' && (subName === PROCESSADOS_FOLDER || subName === PROCESSADOS_ERRO_FOLDER)) {
      continue;
    }
    const continueWalk = driveWalkRecursive(sub.getId(), prefix + subName + '/', sinceMs, callback);
    if (continueWalk === false) return false;
  }
  return true;
}


// ============================================================================
// Lógica de demanda vs mirror
// ============================================================================

/**
 * Retorna nome do inbox se o arquivo é uma demanda (direto em inbox-X/, sem _).
 * Retorna null pra mirror.
 */
function isInboxTopLevel(prefix, fileName) {
  const parts = prefix.split('/').filter(Boolean);
  if (parts.length !== 1) return null;
  if (INBOXES.indexOf(parts[0]) === -1) return null;
  if (fileName.charAt(0) === '_') return null;
  return parts[0];
}


function normalizarNome(name) {
  return name.endsWith('.md') ? name : name + '.md';
}


/**
 * Modo mirror: cópia raw idempotente pro GitHub.
 * Retorna: 'created' | 'updated' | 'unchanged' | 'skipped'
 */
function processarMirror(file, prefix) {
  const mime = file.getMimeType();
  // Pula binários
  if (mime !== MimeType.GOOGLE_DOCS && mime.indexOf('text/') !== 0 && mime !== 'application/octet-stream') {
    Logger.log('Mirror skip (mime ' + mime + '): ' + prefix + file.getName());
    return 'skipped';
  }

  let content;
  try {
    content = driveReadAsText(file);
  } catch (e) {
    Logger.log('Read falhou ' + prefix + file.getName() + ': ' + e.message);
    throw e;
  }

  const name = normalizarNome(file.getName());
  const path = 'dialogos/' + prefix + name;
  const msg = 'mirror: ' + name + ' de Drive dialogos/' + prefix;
  return ghPutFile(path, content, msg);
}


/**
 * Modo demanda: valida frontmatter, commita no GitHub, move pra processados/.
 * Retorna: 'imported' | 'invalid'
 */
function processarDemandaInbox(file, inbox) {
  const rootId = driveGetRootId_();
  const name = file.getName();
  const content = driveReadAsText(file);
  const parsed = parseFrontmatter(content);
  const fm = parsed[0];
  const body = parsed[1];

  function moverPraErro(motivo) {
    const erroId = driveEnsureFolderPath(rootId, 'dialogos/' + PROCESSADOS_ERRO_FOLDER + '/' + inbox);
    file.moveTo(DriveApp.getFolderById(erroId));
    Logger.log('Movido pra processados-erro/' + inbox + '/: ' + motivo);
  }

  if (!fm) {
    moverPraErro('frontmatter ausente/inválido');
    return 'invalid';
  }
  const erros = validateDemandaFrontmatter(fm);
  if (erros.length > 0) {
    moverPraErro('validação: ' + erros.join(', '));
    return 'invalid';
  }

  const githubName = normalizarNome(name);
  const githubPath = 'dialogos/' + inbox + '/' + githubName;
  const msg = 'import: ' + name + ' via ' + inbox + ' (origem: ' + fm.origem + ')';
  ghPutFile(githubPath, content, msg);

  // Move pra processados/<inbox>/
  const procId = driveEnsureFolderPath(rootId, 'dialogos/' + PROCESSADOS_FOLDER + '/' + inbox);
  file.moveTo(DriveApp.getFolderById(procId));

  // Notifica Telegram só pra inbox-tiogu (paridade com import_from_drive.py)
  if (inbox === 'inbox-tiogu') {
    const tituloMatch = body.match(/^#\s+(.+)$/m);
    const titulo = tituloMatch ? tituloMatch[1].trim() : name;
    sendTelegramAlert(
      '📥 Demanda nova em inbox-tiogu\n' +
      'Origem: ' + fm.origem + ' | Prioridade: ' + fm.prioridade + '\n' +
      '"' + titulo + '"'
    );
  }

  return 'imported';
}


// ============================================================================
// Frontmatter parsing (subset YAML — só o que o protocolo usa)
// ============================================================================

function parseFrontmatter(content) {
  if (content.indexOf('---') !== 0) return [null, content];
  const end = content.indexOf('\n---', 3);
  if (end === -1) return [null, content];

  const fmStr = content.slice(3, end).trim();
  let body = content.slice(end + 4);
  while (body.charAt(0) === '\n') body = body.slice(1);

  const fm = parseSimpleYaml_(fmStr);
  return [fm, body];
}


/**
 * Parse YAML simples linha-a-linha. Suporta string scalars com aspas opcionais.
 * NÃO suporta listas, blocos multi-linha, etc — não precisamos pras demandas.
 */
function parseSimpleYaml_(str) {
  const fm = {};
  const lines = str.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const m = line.match(/^([a-zA-Z_][\w\-]*)\s*:\s*(.*)$/);
    if (!m) continue;
    let val = m[2].trim();
    // Strip optional quotes
    if ((val.charAt(0) === '"' && val.charAt(val.length - 1) === '"') ||
        (val.charAt(0) === "'" && val.charAt(val.length - 1) === "'")) {
      val = val.slice(1, -1);
    }
    fm[m[1]] = val;
  }
  return fm;
}


function validateDemandaFrontmatter(fm) {
  const erros = [];
  const obrig = ['tipo', 'origem', 'destino', 'prioridade', 'status', 'criado_em'];
  for (let i = 0; i < obrig.length; i++) {
    if (!fm[obrig[i]]) erros.push('campo ausente: ' + obrig[i]);
  }
  if (erros.length > 0) return erros;

  if (fm.tipo !== 'demanda') erros.push("tipo deve ser 'demanda', recebeu '" + fm.tipo + "'");
  if (!PORTAS_VALIDAS[fm.origem]) erros.push('origem inválida: ' + fm.origem);
  if (!PORTAS_VALIDAS[fm.destino]) erros.push('destino inválido: ' + fm.destino);
  if (fm.origem === fm.destino) erros.push('origem == destino');
  return erros;
}
