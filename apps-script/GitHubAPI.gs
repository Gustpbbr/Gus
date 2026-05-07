/**
 * Wrappers da API REST do GitHub via UrlFetchApp.
 *
 * Auth: PAT clássico (sem expiração) salvo em Script Properties como
 * GITHUB_TOKEN. Scope necessário: repo.
 */


function ghGetProps_() {
  const p = PropertiesService.getScriptProperties();
  const token = p.getProperty('GITHUB_TOKEN');
  if (!token) throw new Error('GITHUB_TOKEN ausente em Script Properties');
  return {
    token: token,
    owner: p.getProperty('GITHUB_OWNER'),
    repo: p.getProperty('GITHUB_REPO'),
    branch: p.getProperty('GITHUB_BRANCH') || 'main',
  };
}


/**
 * Wrapper genérico. Retorna JSON parseado, null em 404, throw em outros erros.
 */
function ghApi(method, urlPath, body) {
  const cfg = ghGetProps_();
  const url = 'https://api.github.com' + urlPath;
  const opts = {
    method: method,
    headers: {
      'Authorization': 'token ' + cfg.token,
      'Accept': 'application/vnd.github.v3+json',
      'X-GitHub-Api-Version': '2022-11-28',
    },
    muteHttpExceptions: true,
  };
  if (body) {
    opts.contentType = 'application/json';
    opts.payload = JSON.stringify(body);
  }

  const resp = UrlFetchApp.fetch(url, opts);
  const code = resp.getResponseCode();
  const text = resp.getContentText();

  if (code === 404) return null;
  if (code < 200 || code >= 300) {
    throw new Error('GitHub ' + method + ' ' + urlPath + ' -> ' + code + ': ' + text.slice(0, 200));
  }
  return text ? JSON.parse(text) : null;
}


function ghGetHeadSha() {
  const cfg = ghGetProps_();
  const data = ghApi('GET', '/repos/' + cfg.owner + '/' + cfg.repo + '/branches/' + cfg.branch);
  if (!data) throw new Error('Branch ' + cfg.branch + ' não encontrada');
  return data.commit.sha;
}


/**
 * Lista todos os arquivos .md do repo via Git Tree API recursive=1.
 * Limit: 100k items / 7MB. Pra repo Gus está MUITO folgado.
 */
function ghListAllRepoFiles() {
  const cfg = ghGetProps_();
  const data = ghApi('GET', '/repos/' + cfg.owner + '/' + cfg.repo + '/git/trees/' + cfg.branch + '?recursive=1');
  if (!data) throw new Error('Trees API retornou null');
  if (data.truncated) {
    Logger.log('AVISO: tree truncated, pode ter arquivos faltando');
  }
  const files = [];
  for (let i = 0; i < data.tree.length; i++) {
    const item = data.tree[i];
    if (item.type === 'blob' && item.path.endsWith('.md')) {
      files.push(item.path);
    }
  }
  return files;
}


/**
 * Compara dois SHAs e retorna lista de arquivos .md modificados (added/modified).
 * Removidos são ignorados (Apps Script não deleta no Drive — política).
 *
 * Limit da Compare API: 250 commits / 300 files. Pra trafego do Gus é folgado.
 */
function ghGetChangedFiles(baseSha, headSha) {
  const cfg = ghGetProps_();
  const data = ghApi('GET', '/repos/' + cfg.owner + '/' + cfg.repo + '/compare/' + baseSha + '...' + headSha);
  if (!data || !data.files) return [];

  const out = [];
  for (let i = 0; i < data.files.length; i++) {
    const f = data.files[i];
    if (f.status !== 'removed' && f.filename.endsWith('.md')) {
      out.push(f.filename);
    }
  }
  return out;
}


/**
 * Lê conteúdo de um arquivo do GitHub (UTF-8 decoded).
 */
function ghFetchFileContent(path) {
  const cfg = ghGetProps_();
  const enc = encodeURIComponent(path).replace(/%2F/g, '/');
  const data = ghApi('GET', '/repos/' + cfg.owner + '/' + cfg.repo + '/contents/' + enc + '?ref=' + cfg.branch);
  if (!data) throw new Error('Arquivo não encontrado no GitHub: ' + path);
  if (data.encoding !== 'base64') throw new Error('Encoding inesperado: ' + data.encoding);
  const bytes = Utilities.base64Decode(data.content);
  return Utilities.newBlob(bytes).getDataAsString('utf-8');
}


/**
 * Cria ou atualiza arquivo no GitHub via Contents API.
 * Idempotente: GET antes pra checar se conteúdo já é byte-idêntico → skip.
 *
 * Retorna: 'created' | 'updated' | 'unchanged'
 */
function ghPutFile(path, content, commitMessage) {
  const cfg = ghGetProps_();
  const enc = encodeURIComponent(path).replace(/%2F/g, '/');

  // GET pra pegar SHA atual + comparar
  const existing = ghApi('GET', '/repos/' + cfg.owner + '/' + cfg.repo + '/contents/' + enc + '?ref=' + cfg.branch);
  if (existing && existing.encoding === 'base64') {
    try {
      const currentBytes = Utilities.base64Decode(existing.content);
      const currentStr = Utilities.newBlob(currentBytes).getDataAsString('utf-8');
      if (currentStr === content) return 'unchanged';
    } catch (e) {
      Logger.log('Compare falhou (' + e.message + '), prossegue com PUT');
    }
  }

  const body = {
    message: commitMessage,
    content: Utilities.base64Encode(content, Utilities.Charset.UTF_8),
    branch: cfg.branch,
  };
  if (existing) body.sha = existing.sha;

  ghApi('PUT', '/repos/' + cfg.owner + '/' + cfg.repo + '/contents/' + enc, body);
  return existing ? 'updated' : 'created';
}
