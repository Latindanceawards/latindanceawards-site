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
