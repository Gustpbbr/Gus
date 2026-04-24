// Google Apps Script — Gus: Drive Inbox → GitHub
// Deploy em: script.google.com → Novo projeto
// Trigger: processInbox a cada 5 minutos (time-based)
//
// Propriedades necessárias (Project Settings → Script Properties):
//   GITHUB_TOKEN    — Personal Access Token com Contents: read+write no repo Gus
//   INBOX_FOLDER_ID — ID da pasta Gus-Sync/Inbox/ no Drive (da URL do Drive)

const GITHUB_OWNER = 'Gustpbbr';
const GITHUB_REPO = 'Gus';
const GITHUB_BRANCH = 'main';
const DEFAULT_GITHUB_PATH = 'capturado/misc/';
const PROCESSED_FOLDER_NAME = 'Processado';

function processInbox() {
  const props = PropertiesService.getScriptProperties();
  const githubToken = props.getProperty('GITHUB_TOKEN');
  const inboxFolderId = props.getProperty('INBOX_FOLDER_ID');

  if (!githubToken || !inboxFolderId) {
    Logger.log('ERRO: Configure GITHUB_TOKEN e INBOX_FOLDER_ID nas propriedades do script.');
    return;
  }

  const inboxFolder = DriveApp.getFolderById(inboxFolderId);

  // Cria pasta Processado se não existir
  let processedFolder;
  const existing = inboxFolder.getFoldersByName(PROCESSED_FOLDER_NAME);
  processedFolder = existing.hasNext() ? existing.next() : inboxFolder.createFolder(PROCESSED_FOLDER_NAME);

  const files = inboxFolder.getFiles();
  let ok = 0;
  let erros = 0;

  while (files.hasNext()) {
    const file = files.next();
    const fileName = file.getName();

    if (!fileName.endsWith('.md')) continue;

    try {
      const content = file.getBlob().getDataAsString('utf-8');
      const githubPath = extractGithubPath(content, fileName);

      pushToGithub(githubToken, githubPath, content, fileName);

      processedFolder.addFile(file);
      inboxFolder.removeFile(file);

      Logger.log('✓ ' + fileName + ' → ' + githubPath);
      ok++;
    } catch (e) {
      Logger.log('✗ Erro em ' + fileName + ': ' + e.message);
      erros++;
    }
  }

  Logger.log('Concluído: ' + ok + ' arquivo(s) processados, ' + erros + ' erro(s).');
}

function extractGithubPath(content, fileName) {
  // Extrai github_path: do frontmatter YAML (entre --- e ---)
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (fmMatch) {
    const pathMatch = fmMatch[1].match(/^github_path:\s*(.+)$/m);
    if (pathMatch) return pathMatch[1].trim();
  }
  return DEFAULT_GITHUB_PATH + fileName;
}

function pushToGithub(token, path, content, fileName) {
  const encodedContent = Utilities.base64Encode(
    Utilities.newBlob(content, MimeType.PLAIN_TEXT).setEncoding('UTF-8').getBytes()
  );

  const apiUrl = 'https://api.github.com/repos/' + GITHUB_OWNER + '/' + GITHUB_REPO + '/contents/' + path;
  const headers = {
    'Authorization': 'token ' + token,
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json',
  };

  // Verifica se arquivo já existe (precisa do SHA pra atualizar)
  const checkResp = UrlFetchApp.fetch(apiUrl, {
    method: 'GET',
    headers: headers,
    muteHttpExceptions: true,
  });

  const body = {
    message: 'capture: ' + fileName + ' via Claude Projetos',
    content: encodedContent,
    branch: GITHUB_BRANCH,
  };

  if (checkResp.getResponseCode() === 200) {
    body.sha = JSON.parse(checkResp.getContentText()).sha;
  }

  const putResp = UrlFetchApp.fetch(apiUrl, {
    method: 'PUT',
    headers: headers,
    payload: JSON.stringify(body),
    muteHttpExceptions: true,
  });

  const code = putResp.getResponseCode();
  if (code < 200 || code >= 300) {
    throw new Error('GitHub API ' + code + ': ' + putResp.getContentText().substring(0, 300));
  }
}
