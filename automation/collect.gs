/**
 * Latin Dance Awards: receives applications from the website form and writes them to this Google Sheet.
 * Setup (once): open the Sheet > Extensions > Apps Script > paste this file > Deploy > New deployment
 * > type "Web app" > Execute as: Me > Who has access: Anyone > Deploy > copy the web-app URL
 * and paste it into FORM_ENDPOINT in tools/build.py (then run build.py and push).
 * Column headers match automation/emails.gs, so the confirmation e-mails keep working.
 */
var SHEET_ID = '12JuPTUjsvSyKjJT9MeUovPpNRDYRJMJEddRJZ616zDc';
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
  var a = e && e.parameter && e.parameter.action;
  if (a === 'vote') return handleVote_(e.parameter);
  if (a === 'review') return handleReview_(e.parameter);
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
    var ss = SpreadsheetApp.openById(SHEET_ID);
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


/* ===== Audience Award voting + school reviews (all confirmed by e-mail link) ===== */
var VOTE_SHEET = 'Votes';
var VOTE_HEAD = ['Submitted at', 'School', 'City', 'Email (normalized)', 'Token', 'Status', 'Confirmed at', 'Language'];
var REVIEW_SHEET = 'Reviews';
var REVIEW_HEAD = ['Submitted at', 'School', 'City', 'Name', 'Rating', 'Text', 'Email (normalized)', 'Token', 'Status', 'Confirmed at', 'Language'];
var MAX_MAILS_PER_DAY = 90;
// Reviews appear on the website once the e-mail link is clicked (Status "Confirmed").
// To approve each review by hand first, set this to true: only rows you change to "Approved" are shown.
// To hide a review at any time, set its Status to "Hidden".
var REQUIRE_APPROVAL = false;

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

function sheet_(name, head) {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = ss.getSheetByName(name) || ss.insertSheet(name);
  if (sh.getLastRow() === 0) {
    sh.appendRow(head);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, head.length).setFontWeight('bold');
  }
  return sh;
}

function mailsToday_() {
  var today = new Date().toDateString(), n = 0;
  [[VOTE_SHEET, VOTE_HEAD], [REVIEW_SHEET, REVIEW_HEAD]].forEach(function (s) {
    var d = sheet_(s[0], s[1]).getDataRange().getValues();
    for (var i = 1; i < d.length; i++) if (new Date(d[i][0]).toDateString() === today) n++;
  });
  return n;
}

function safe_(v) { v = String(v || ''); return /^[=+\-@]/.test(v) ? "'" + v : v; }

function sendConfirm_(to, en, kind, school, city, link) {
  var what = kind === 'review' ? (en ? 'review' : 'Bewertung') : (en ? 'vote' : 'Stimme');
  var subj = en ? 'Please confirm your ' + what + ': ' + school : 'Bitte bestätige deine ' + what + ': ' + school;
  var body = en
    ? 'Hi!\n\nYou left a ' + what + ' for ' + school + ' (' + city + ') on Latin Dance Awards.\n\nPlease confirm it with this link:\n' + link + '\n\nIf this was not you, just ignore this e-mail.\n\nLatin Dance Awards\nhttps://latindanceawards.com'
    : 'Hallo!\n\nDu hast bei den Latin Dance Awards eine ' + what + ' für ' + school + ' (' + city + ') abgegeben.\n\nBitte bestätige sie mit diesem Link:\n' + link + '\n\nWenn du das nicht warst, ignoriere diese E-Mail einfach.\n\nLatin Dance Awards\nhttps://latindanceawards.com';
  MailApp.sendEmail({ to: to, subject: subj, body: body, name: 'Latin Dance Awards', replyTo: 'hello@latindanceawards.com' });
}

function handleVote_(p) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var email = normEmail_(p.email), school = String(p.school || '').substring(0, 120), city = String(p.city || '').substring(0, 40);
    if (p.hp) return ContentService.createTextOutput('ok');
    if (!email || !school) return ContentService.createTextOutput('invalid');
    var sh = sheet_(VOTE_SHEET, VOTE_HEAD), data = sh.getDataRange().getValues(), pendingRow = -1;
    for (var r = 1; r < data.length; r++) {
      if (data[r][3] === email) {
        if (data[r][5] === 'Confirmed') return ContentService.createTextOutput('ok');
        pendingRow = r + 1;
      }
    }
    if (mailsToday_() >= MAX_MAILS_PER_DAY) return ContentService.createTextOutput('busy');
    var token = Utilities.getUuid();
    var row = [new Date(), school, city, email, token, 'Pending', '', p.language === 'EN' ? 'EN' : 'DE'];
    if (pendingRow > 0) sh.getRange(pendingRow, 1, 1, row.length).setValues([row]); else sh.appendRow(row);
    sendConfirm_(p.email, p.language === 'EN', 'vote', school, city, ScriptApp.getService().getUrl() + '?vote=' + token);
    return ContentService.createTextOutput('ok');
  } finally { lock.releaseLock(); }
}

function handleReview_(p) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var email = normEmail_(p.email), school = String(p.school || '').substring(0, 120), city = String(p.city || '').substring(0, 40);
    var name = String(p.name || '').trim().substring(0, 40), text = String(p.text || '').trim().substring(0, 600), rating = parseInt(p.rating, 10);
    if (p.hp) return ContentService.createTextOutput('ok');
    if (!email || !school || !(rating >= 1 && rating <= 5) || text.length < 10 || /https?:|www\.|@/i.test(text + ' ' + name)) return ContentService.createTextOutput('invalid');
    var sh = sheet_(REVIEW_SHEET, REVIEW_HEAD), data = sh.getDataRange().getValues(), pendingRow = -1;
    for (var r = 1; r < data.length; r++) {
      if (data[r][6] === email && data[r][1] === school) {
        if (data[r][8] !== 'Pending') return ContentService.createTextOutput('ok');
        pendingRow = r + 1;
      }
    }
    if (mailsToday_() >= MAX_MAILS_PER_DAY) return ContentService.createTextOutput('busy');
    var token = Utilities.getUuid();
    var row = [new Date(), school, city, safe_(name), rating, safe_(text), email, token, 'Pending', '', p.language === 'EN' ? 'EN' : 'DE'];
    if (pendingRow > 0) sh.getRange(pendingRow, 1, 1, row.length).setValues([row]); else sh.appendRow(row);
    sendConfirm_(p.email, p.language === 'EN', 'review', school, city, ScriptApp.getService().getUrl() + '?review=' + token);
    return ContentService.createTextOutput('ok');
  } finally { lock.releaseLock(); }
}

function confirm_(sheetName, head, tokenCol, statusCol, token) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var sh = sheet_(sheetName, head), data = sh.getDataRange().getValues();
    for (var r = 1; r < data.length; r++) {
      if (data[r][tokenCol] === token) {
        var school = data[r][1];
        if (data[r][statusCol] !== 'Pending') return { school: school, again: true };
        if (sheetName === VOTE_SHEET) {
          for (var k = 1; k < data.length; k++) if (data[k][3] === data[r][3] && data[k][5] === 'Confirmed') return { school: school, again: true };
        }
        sh.getRange(r + 1, statusCol + 1).setValue('Confirmed');
        sh.getRange(r + 1, statusCol + 2).setValue(new Date());
        return { school: school, again: false };
      }
    }
    return null;
  } finally { lock.releaseLock(); }
}

function page_(msg) {
  var esc = function (x) { return String(x).replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); };
  var html = '<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0;background:#120e0d;color:#f6e7d3;font-family:Georgia,serif;display:flex;min-height:100vh;align-items:center;justify-content:center;text-align:center"><div style="max-width:440px;padding:24px"><h1 style="color:#e4b95b;font-weight:400">Latin Dance Awards</h1><p style="font-size:20px">' + esc(msg[0]) + '</p><p style="color:#bfae98">' + esc(msg[1]) + '</p><p><a style="color:#e4b95b" href="https://latindanceawards.com/rankings.html" target="_top">latindanceawards.com</a></p></div></body></html>';
  return HtmlService.createHtmlOutput(html).setTitle('Latin Dance Awards').addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function reviewsJson_(school) {
  var sh = sheet_(REVIEW_SHEET, REVIEW_HEAD), d = sh.getDataRange().getValues(), want = REQUIRE_APPROVAL ? 'Approved' : 'Confirmed', items = [], sum = 0, n = 0;
  for (var i = d.length - 1; i >= 1; i--) {
    if (d[i][1] === school && d[i][8] === want) {
      n++; sum += Number(d[i][4]) || 0;
      if (items.length < 30) items.push({ n: String(d[i][3] || ''), r: Number(d[i][4]) || 0, t: String(d[i][5] || ''), d: Utilities.formatDate(new Date(d[i][0]), 'UTC', 'yyyy-MM-dd') });
    }
  }
  return ContentService.createTextOutput(JSON.stringify({ count: n, avg: n ? Math.round(sum / n * 10) / 10 : 0, items: items })).setMimeType(ContentService.MimeType.JSON);
}

function doGet(e) {
  var p = (e && e.parameter) || {};
  if (p.action === 'reviews') return reviewsJson_(String(p.school || ''));
  var bad = ['Link ungültig oder abgelaufen.', 'Link invalid or expired.'];
  if (p.review) {
    var a = confirm_(REVIEW_SHEET, REVIEW_HEAD, 7, 8, p.review);
    if (!a) return page_(bad);
    return page_(a.again ? ['Deine Bewertung wurde schon bestätigt. Danke!', 'Your review was already confirmed. Thank you!']
      : ['Danke! Deine Bewertung für ' + a.school + ' ist bestätigt.', 'Thank you! Your review for ' + a.school + ' is confirmed.']);
  }
  if (p.vote) {
    var b = confirm_(VOTE_SHEET, VOTE_HEAD, 4, 5, p.vote);
    if (!b) return page_(bad);
    return page_(b.again ? ['Deine Stimme wurde schon gezählt. Danke!', 'Your vote was already counted. Thank you!']
      : ['Danke! Deine Stimme für ' + b.school + ' ist bestätigt.', 'Thank you! Your vote for ' + b.school + ' is confirmed.']);
  }
  return page_(['Latin Dance Awards läuft.', 'Latin Dance Awards is running.']);
}
