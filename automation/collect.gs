/**
 * Latin Dance Awards: receives applications from the website form and writes them to this Google Sheet.
 * Setup (once): open the Sheet > Extensions > Apps Script > paste this file > Deploy > New deployment
 * > type "Web app" > Execute as: Me > Who has access: Anyone > Deploy > copy the web-app URL
 * and paste it into FORM_ENDPOINT in tools/build.py (then run build.py and push).
 * Column headers match automation/emails.gs, so the confirmation e-mails keep working.
 */
var SHEET_NAME = 'Applications';
var COLUMNS = [  // [sheet header, form field]
  ['Submitted at', null],
  ['Name der Schule / School name', 'school'],
  ['Stadt / City', 'city'],
  ['Dein Name / Your name', 'contact'],
  ['E-Mail / Email', 'email'],
  ['Website', 'website'],
  ['Google Maps', 'maps'],
  ['Instagram', 'instagram'],
  ['TikTok', 'tiktok'],
  ['Gründungsjahr / Year founded', 'year'],
  ['Probestunde / Trial class', 'trial'],
  ['Levels', 'levels'],
  ['Kursplan / Schedule link', 'schedule'],
  ['Festivals', 'festivals'],
  ['Events (Häufigkeit / frequency)', 'social'],
  ['Gastlehrer / Guest teachers', 'guests'],
  ['Wettbewerbe / Competitions', 'competitions'],
  ['Sprache / Language', 'language'],
  ['Status', null]
];

function doPost(e) {
  if (e && e.parameter && e.parameter.action === 'vote') return handleVote_(e.parameter);
  return handleApplication_(e);
}

function handleApplication_(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var p = (e && e.parameter) || {};
    if (!p.school || !p.email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(p.email)) {
      return ContentService.createTextOutput('invalid');
    }
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    if (sh.getLastRow() === 0) {
      sh.appendRow(COLUMNS.map(function (c) { return c[0]; }));
      sh.setFrozenRows(1);
      sh.getRange(1, 1, 1, COLUMNS.length).setFontWeight('bold');
    }
    var row = COLUMNS.map(function (c) {
      if (c[0] === 'Submitted at') return new Date();
      if (c[0] === 'Status') return 'New';
      var v = String(p[c[1]] || '').substring(0, 1500);
      return /^[=+\-@]/.test(v) ? "'" + v : v;   // stop spreadsheet formula injection
    });
    sh.appendRow(row);
    return ContentService.createTextOutput('ok');
  } finally {
    lock.releaseLock();
  }
}


/* ================= Publikumspreis / Audience Award voting =================
 * One vote per person (e-mail). Flow: POST action=vote -> row "Pending" + confirmation e-mail
 * -> person clicks the link (doGet ?vote=TOKEN) -> row "Confirmed". Counted only when confirmed.
 * Results are NOT shown on the website before 20 Dec 2026.
 * Sheet "Votes" is created automatically. */
var VOTE_SHEET = 'Votes';
var VOTE_HEAD = ['Submitted at', 'School', 'City', 'Email (normalized)', 'Token', 'Status', 'Confirmed at', 'Language'];
var MAX_MAILS_PER_DAY = 90;   // safety margin below Google's daily mail quota

function normEmail_(e) {
  e = String(e || '').trim().toLowerCase();
  var m = e.match(/^([^@\s]+)@([^@\s]+\.[^@\s]+)$/);
  if (!m) return '';
  var u = m[1], d = m[2];
  if (d === 'googlemail.com') d = 'gmail.com';
  u = u.split('+')[0];
  if (d === 'gmail.com') u = u.replace(/\./g, '');
  return u + '@' + d;
}

function voteSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(VOTE_SHEET) || ss.insertSheet(VOTE_SHEET);
  if (sh.getLastRow() === 0) {
    sh.appendRow(VOTE_HEAD);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, VOTE_HEAD.length).setFontWeight('bold');
  }
  return sh;
}

function handleVote_(p) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var email = normEmail_(p.email), school = String(p.school || '').substring(0, 120), city = String(p.city || '').substring(0, 40);
    if (!email || !school || p.hp) return ContentService.createTextOutput('invalid');
    var en = p.language === 'EN';
    var sh = voteSheet_(), data = sh.getDataRange().getValues();
    var pendingRow = -1;
    for (var r = 1; r < data.length; r++) {
      if (data[r][3] === email) {
        if (data[r][5] === 'Confirmed') return ContentService.createTextOutput('ok');   // already voted: silently ignore
        pendingRow = r + 1;
      }
    }
    var sent = 0, today = new Date().toDateString();
    for (var i = 1; i < data.length; i++) if (new Date(data[i][0]).toDateString() === today) sent++;
    if (sent >= MAX_MAILS_PER_DAY) return ContentService.createTextOutput('busy');
    var token = Utilities.getUuid();
    var row = [new Date(), school, city, email, token, 'Pending', '', en ? 'EN' : 'DE'];
    if (pendingRow > 0) sh.getRange(pendingRow, 1, 1, row.length).setValues([row]); else sh.appendRow(row);
    var link = ScriptApp.getService().getUrl() + '?vote=' + token;
    var subj = en ? 'Please confirm your vote: ' + school : 'Bitte bestätige deine Stimme: ' + school;
    var body = en
      ? 'Hi!\n\nYou voted for ' + school + ' (' + city + ') in the Latin Dance Awards Audience Award.\n\nPlease confirm your vote with this link (one vote per person):\n' + link + '\n\nIf this was not you, just ignore this e-mail.\n\nLatin Dance Awards\nhttps://latindanceawards.com'
      : 'Hallo!\n\nDu hast beim Publikumspreis der Latin Dance Awards für ' + school + ' (' + city + ') abgestimmt.\n\nBitte bestätige deine Stimme mit diesem Link (eine Stimme pro Person):\n' + link + '\n\nWenn du das nicht warst, ignoriere diese E-Mail einfach.\n\nLatin Dance Awards\nhttps://latindanceawards.com';
    MailApp.sendEmail({ to: p.email, subject: subj, body: body, name: 'Latin Dance Awards', replyTo: 'hello@latindanceawards.com' });
    return ContentService.createTextOutput('ok');
  } finally {
    lock.releaseLock();
  }
}

function doGet(e) {
  var t = e && e.parameter && e.parameter.vote;
  var msg = ['Link ungültig oder abgelaufen.', 'Link invalid or expired.'];
  var school = '';
  if (t) {
    var lock = LockService.getScriptLock();
    lock.waitLock(20000);
    try {
      var sh = voteSheet_(), data = sh.getDataRange().getValues();
      for (var r = 1; r < data.length; r++) {
        if (data[r][4] === t) {
          school = data[r][1];
          var already = false;
          for (var k = 1; k < data.length; k++) if (data[k][3] === data[r][3] && data[k][5] === 'Confirmed') already = true;
          if (data[r][5] === 'Confirmed' || already) { msg = ['Deine Stimme wurde schon gezählt. Danke!', 'Your vote was already counted. Thank you!']; }
          else {
            sh.getRange(r + 1, 6).setValue('Confirmed');
            sh.getRange(r + 1, 7).setValue(new Date());
            msg = ['Danke! Deine Stimme für ' + school + ' ist bestätigt.', 'Thank you! Your vote for ' + school + ' is confirmed.'];
          }
          break;
        }
      }
    } finally { lock.releaseLock(); }
  }
  var esc = function (x) { return String(x).replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); };
  var html = '<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0;background:#120e0d;color:#f6e7d3;font-family:Georgia,serif;display:flex;min-height:100vh;align-items:center;justify-content:center;text-align:center"><div style="max-width:440px;padding:24px"><h1 style="color:#e4b95b;font-weight:400">Latin Dance Awards</h1><p style="font-size:20px">' + esc(msg[0]) + '</p><p style="color:#bfae98">' + esc(msg[1]) + '</p><p><a style="color:#e4b95b" href="https://latindanceawards.com/rankings.html" target="_top">latindanceawards.com</a></p></div></body></html>';
  return HtmlService.createHtmlOutput(html).setTitle('Latin Dance Awards').addMetaTag('viewport', 'width=device-width, initial-scale=1');
}
