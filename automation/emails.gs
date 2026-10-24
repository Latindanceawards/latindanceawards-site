/**
 * Latin Dance Awards — automatic emails for school applications
 * ------------------------------------------------------------
 * What it does (runs by itself every hour):
 *   1. New application  -> sends a confirmation email right away.
 *   2. 3 days later     -> sends "application accepted, please send proofs" with a link to the proof form.
 *   3. 10 days after that, if no proofs arrived -> sends one friendly reminder.
 *
 * Setup (once):
 *   - Connect your Tally application form to Google Sheets (Tally: Integrations -> Google Sheets).
 *   - In that spreadsheet: Extensions -> Apps Script -> paste this whole file -> Save.
 *   - Fill in the CONFIG below.
 *   - Choose the function "setup" in the toolbar and click Run. Allow the permissions.
 *   That's it. To test first, set TEST_MODE to true (all emails go to TEST_EMAIL only).
 */

var CONFIG = {
  // Must match the question titles in your Tally form (the column headers in the sheet)
  COL_EMAIL:    'E-Mail / Email',
  COL_SCHOOL:   'Name der Schule / School name',
  COL_CONTACT:  'Dein Name / Your name',
  COL_LANGUAGE: 'Sprache / Language',      // answers: "Deutsch" or "English"
  COL_SUBMITTED:'Submitted at',            // Tally adds this column automatically

  // Link to your second Tally form (the proof form). The school name and email are filled in automatically.
  PROOF_FORM_URL: 'https://tally.so/r/XXXXXX',

  // Optional: name of the sheet where the proof form saves its answers (in this same spreadsheet).
  // If set, schools that already sent proofs won't get the reminder.
  PROOF_SHEET: '',
  PROOF_COL_EMAIL: 'email',               // the hidden field in the proof form

  INSTAGRAM_HANDLE: '@latindanceawards',
  SENDER_NAME: 'Latin Dance Awards',
  REPLY_TO: 'hello@latindanceawards.com',

  DAYS_UNTIL_PROOF_EMAIL: 3,
  DAYS_UNTIL_REMINDER: 10,
  PROOF_DEADLINE_DAYS: 10,

  TEST_MODE: false,
  TEST_EMAIL: 'your-own-email@gmail.com'
};

// Status columns this script adds to the sheet (don't rename them later)
var S_CONFIRM = 'Bestätigung gesendet';
var S_PROOF   = 'Nachweis-Mail gesendet';
var S_REMIND  = 'Erinnerung gesendet';

function setup() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'processApplications') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('processApplications').timeBased().everyHours(1).create();
  processApplications();
}

function processApplications() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) return;
  try {
    var sheet = findApplicationSheet_();
    var data = sheet.getDataRange().getValues();
    if (data.length < 2) return;
    var head = data[0].map(String);
    var col = function (name) { return head.indexOf(name); };

    [S_CONFIRM, S_PROOF, S_REMIND].forEach(function (name) {
      if (col(name) === -1) { sheet.getRange(1, head.length + 1).setValue(name); head.push(name); }
    });

    var cEmail = col(CONFIG.COL_EMAIL), cSchool = col(CONFIG.COL_SCHOOL), cContact = col(CONFIG.COL_CONTACT),
        cLang = col(CONFIG.COL_LANGUAGE), cDate = col(CONFIG.COL_SUBMITTED);
    if (cEmail === -1 || cSchool === -1) throw new Error('Email or school column not found. Check COL_EMAIL and COL_SCHOOL in CONFIG.');

    var proofsSent = proofEmails_();
    var now = new Date();

    for (var r = 1; r < data.length; r++) {
      var row = data[r];
      var email = String(row[cEmail] || '').trim();
      if (!email || email.indexOf('@') === -1) continue;
      var a = {
        email: email,
        school: String(row[cSchool] || '').trim(),
        contact: cContact > -1 ? String(row[cContact] || '').trim() : '',
        en: cLang > -1 && /engl/i.test(String(row[cLang])),
        submitted: cDate > -1 && row[cDate] ? new Date(row[cDate]) : now
      };
      var days = (now - a.submitted) / 86400000;

      if (!row[col(S_CONFIRM)]) {
        send_(a, confirmationEmail_(a));
        mark_(sheet, r, col(S_CONFIRM));
      }
      if (!row[col(S_PROOF)] && days >= CONFIG.DAYS_UNTIL_PROOF_EMAIL) {
        send_(a, proofEmail_(a));
        mark_(sheet, r, col(S_PROOF));
      }
      var proofDate = row[col(S_PROOF)] ? new Date(row[col(S_PROOF)]) : null;
      if (proofDate && !row[col(S_REMIND)] && !proofsSent[email.toLowerCase()] &&
          (now - proofDate) / 86400000 >= CONFIG.DAYS_UNTIL_REMINDER) {
        send_(a, reminderEmail_(a));
        mark_(sheet, r, col(S_REMIND));
      }
    }
  } finally {
    lock.releaseLock();
  }
}

/* ---------------- emails ---------------- */

function confirmationEmail_(a) {
  if (a.en) return {
    subject: 'We received your application: ' + a.school,
    body: [
      hello_(a),
      'Thank you for entering <b>' + esc_(a.school) + '</b> for the Latin Dance Awards 2026, Bachata Edition. Your application has arrived.',
      'What happens next: within the next few days you\'ll get a second email with a short request to confirm some of your information. It only takes a few minutes, and you mostly just send links.',
      'Results will be published on <b>December 20, 2026</b>.',
      bye_(a)
    ]
  };
  return {
    subject: 'Deine Bewerbung ist angekommen: ' + a.school,
    body: [
      hallo_(a),
      'Danke, dass du <b>' + esc_(a.school) + '</b> für die Latin Dance Awards 2026, Bachata Edition, angemeldet hast. Deine Bewerbung ist bei uns angekommen.',
      'So geht es weiter: In den nächsten Tagen bekommst du eine zweite E-Mail mit einer kurzen Bitte, einige Angaben zu bestätigen. Das dauert nur ein paar Minuten, meistens schickst du einfach Links.',
      'Die Ergebnisse werden am <b>20. Dezember 2026</b> veröffentlicht.',
      tschuess_(a)
    ]
  };
}

function proofEmail_(a) {
  var link = proofLink_(a);
  var deadline = formatDate_(addDays_(new Date(), CONFIG.PROOF_DEADLINE_DAYS), a.en);
  if (a.en) return {
    subject: 'Application accepted, one last step: ' + a.school,
    body: [
      hello_(a),
      'Good news: the application for <b>' + esc_(a.school) + '</b> has been accepted for the Bachata Awards 2026.',
      'To make sure every ranking is fair, we confirm the information of every school. All we need are a few links that usually already exist:',
      list_([
        '<b>Festivals:</b> a link to the lineup or to the festival\'s post announcing your teachers',
        '<b>Years active:</b> your Impressum, an old article or your first Instagram post',
        '<b>Classes:</b> a link to your class schedule (a screenshot is fine too)',
        '<b>Events:</b> links to 2–3 recent posts about your socials, workshops or guest teachers',
        '<b>Competitions</b> (optional): a link to the published results'
      ]),
      '<b>One more thing:</b> please send a short message to ' + esc_(CONFIG.INSTAGRAM_HANDLE) + ' on Instagram from your school\'s official account, for example "Application ' + esc_(a.school) + '". This shows us the application really comes from you.',
      button_(link, 'Send proofs (5 minutes)'),
      'Please send them by <b>' + deadline + '</b>. Anything we can\'t confirm will simply score 0 points for that factor, but your school stays in the ranking.',
      bye_(a)
    ]
  };
  return {
    subject: 'Bewerbung angenommen, ein letzter Schritt: ' + a.school,
    body: [
      hallo_(a),
      'Gute Nachrichten: Die Bewerbung von <b>' + esc_(a.school) + '</b> wurde für die Bachata Awards 2026 angenommen.',
      'Damit jedes Ranking fair ist, bestätigen wir die Angaben aller Schulen. Dafür brauchen wir nur ein paar Links, die es meistens schon gibt:',
      list_([
        '<b>Festivals:</b> ein Link zum Lineup oder zum Post des Festivals, in dem eure Lehrer angekündigt werden',
        '<b>Jahre aktiv:</b> euer Impressum, ein alter Artikel oder euer erster Instagram-Post',
        '<b>Kurse:</b> ein Link zu eurem Kursplan (ein Screenshot geht auch)',
        '<b>Events:</b> Links zu 2–3 aktuellen Posts über eure Socials, Workshops oder Gastlehrer',
        '<b>Wettbewerbe</b> (optional): ein Link zu den veröffentlichten Ergebnissen'
      ]),
      '<b>Noch eine Kleinigkeit:</b> Schick bitte eine kurze Nachricht an ' + esc_(CONFIG.INSTAGRAM_HANDLE) + ' auf Instagram, und zwar vom offiziellen Account eurer Schule, zum Beispiel „Bewerbung ' + esc_(a.school) + '“. So wissen wir, dass die Bewerbung wirklich von euch kommt.',
      button_(link, 'Nachweise senden (5 Minuten)'),
      'Bitte schick sie bis zum <b>' + deadline + '</b>. Was wir nicht bestätigen können, zählt bei diesem Kriterium mit 0 Punkten, eure Schule bleibt aber im Ranking.',
      tschuess_(a)
    ]
  };
}

function reminderEmail_(a) {
  var link = proofLink_(a);
  if (a.en) return {
    subject: 'Reminder: proofs for ' + a.school,
    body: [
      hello_(a),
      'Just a quick reminder: we haven\'t received the proofs for <b>' + esc_(a.school) + '</b> yet. Without them, we can only score the information we find ourselves, which often means fewer points.',
      button_(link, 'Send proofs now'),
      'Already sent them? Then please ignore this email.',
      bye_(a)
    ]
  };
  return {
    subject: 'Erinnerung: Nachweise für ' + a.school,
    body: [
      hallo_(a),
      'Nur eine kurze Erinnerung: Die Nachweise für <b>' + esc_(a.school) + '</b> haben wir noch nicht erhalten. Ohne sie können wir nur die Angaben bewerten, die wir selbst finden, und das bedeutet oft weniger Punkte.',
      button_(link, 'Jetzt Nachweise senden'),
      'Schon geschickt? Dann ignoriere diese E-Mail einfach.',
      tschuess_(a)
    ]
  };
}

/* ---------------- helpers ---------------- */

function hallo_(a)   { return a.contact ? 'Hallo ' + esc_(a.contact.split(' ')[0]) + ',' : 'Hallo,'; }
function hello_(a)   { return a.contact ? 'Hi ' + esc_(a.contact.split(' ')[0]) + ',' : 'Hi there,'; }
function tschuess_() { return 'Viele Grüße<br>Das Team der Latin Dance Awards'; }
function bye_()      { return 'Best regards,<br>The Latin Dance Awards team'; }

function proofLink_(a) {
  var sep = CONFIG.PROOF_FORM_URL.indexOf('?') > -1 ? '&' : '?';
  return CONFIG.PROOF_FORM_URL + sep + 'schule=' + encodeURIComponent(a.school) + '&email=' + encodeURIComponent(a.email);
}

function send_(a, mail) {
  var to = CONFIG.TEST_MODE ? CONFIG.TEST_EMAIL : a.email;
  MailApp.sendEmail({
    to: to,
    subject: (CONFIG.TEST_MODE ? '[TEST] ' : '') + mail.subject,
    htmlBody: layout_(mail.body),
    body: mail.body.join('\n\n').replace(/<br>/g, '\n').replace(/<[^>]+>/g, ''),
    name: CONFIG.SENDER_NAME,
    replyTo: CONFIG.REPLY_TO
  });
}

function layout_(paragraphs) {
  var p = paragraphs.map(function (x) {
    return /^<(ul|table)/.test(x) ? x : '<p style="margin:0 0 16px">' + x + '</p>';
  }).join('');
  return '<div style="background:#0A0808;padding:32px 12px;font-family:Helvetica,Arial,sans-serif">' +
    '<div style="max-width:560px;margin:0 auto;background:#131011;border:1px solid #3a2f1c;border-radius:18px;padding:34px 30px;color:#F6E7D3;font-size:15px;line-height:1.6">' +
    '<div style="font-family:Georgia,serif;font-size:21px;color:#F6E7D3;margin-bottom:2px">Latin Dance</div>' +
    '<div style="font-size:11px;letter-spacing:5px;color:#E4B95B;font-weight:bold;margin-bottom:26px">AWARDS</div>' +
    p + '</div>' +
    '<div style="max-width:560px;margin:16px auto 0;text-align:center;color:#8a7f7a;font-size:12px">latindanceawards.com · Bachata Edition 2026</div></div>';
}

function list_(items) {
  return '<ul style="margin:0 0 16px;padding-left:20px">' + items.map(function (i) {
    return '<li style="margin:0 0 8px">' + i + '</li>';
  }).join('') + '</ul>';
}

function button_(url, label) {
  return '<table role="presentation" cellspacing="0" cellpadding="0" style="margin:6px 0 22px"><tr><td style="border-radius:999px;background:#E4B95B">' +
    '<a href="' + url + '" style="display:inline-block;padding:13px 26px;color:#131011;font-weight:bold;text-decoration:none;border-radius:999px">' + label + '</a></td></tr></table>';
}

function esc_(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
function addDays_(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
function formatDate_(d, en) {
  var de = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'];
  var e = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  return en ? e[d.getMonth()] + ' ' + d.getDate() : d.getDate() + '. ' + de[d.getMonth()];
}
function mark_(sheet, r, c) { sheet.getRange(r + 1, c + 1).setValue(new Date()); }

function findApplicationSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheets = ss.getSheets();
  for (var i = 0; i < sheets.length; i++) {
    var h = sheets[i].getRange(1, 1, 1, Math.max(1, sheets[i].getLastColumn())).getValues()[0].map(String);
    if (h.indexOf(CONFIG.COL_EMAIL) > -1 && h.indexOf(CONFIG.COL_SCHOOL) > -1 && sheets[i].getName() !== CONFIG.PROOF_SHEET) return sheets[i];
  }
  return sheets[0];
}

function proofEmails_() {
  var out = {};
  if (!CONFIG.PROOF_SHEET) return out;
  var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.PROOF_SHEET);
  if (!sh) return out;
  var v = sh.getDataRange().getValues(), c = v[0].map(String).indexOf(CONFIG.PROOF_COL_EMAIL);
  if (c === -1) return out;
  for (var i = 1; i < v.length; i++) if (v[i][c]) out[String(v[i][c]).trim().toLowerCase()] = true;
  return out;
}
