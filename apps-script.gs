/**
 * 피켓 이벤트 집계용 Google Apps Script
 *
 * 설정 방법
 * 1. 새 구글 시트 생성 → 확장 프로그램 > Apps Script
 * 2. 이 파일 내용을 통째로 붙여넣고 저장
 * 3. 함수 선택에서 setup 실행 (권한 허용) → "log", "집계" 시트가 만들어짐
 * 4. 배포 > 새 배포 > 유형: 웹 앱
 *    - 실행 사용자: 나 / 액세스 권한: 모든 사용자
 * 5. 나온 웹 앱 URL(…/exec)을 index.html 의 LOG_URL 에 넣기
 */

const HEADERS = ["시간", "이벤트", "문구", "QR", "채널", "수정여부"];

function doPost(e) {
  const p = (e && e.parameter) || {};
  const sheet = SpreadsheetApp.getActive().getSheetByName("log");
  sheet.appendRow([
    new Date(),
    String(p.event || "").slice(0, 20),
    String(p.m || "").slice(0, 3),
    String(p.qr || "").slice(0, 3),
    String(p.ch || "").slice(0, 10),
    String(p.edited || "").slice(0, 1),
  ]);
  return ContentService.createTextOutput("ok");
}

function setup() {
  const ss = SpreadsheetApp.getActive();
  const log = ss.getSheetByName("log") || ss.insertSheet("log");
  if (log.getLastRow() === 0) log.appendRow(HEADERS);
  log.setFrozenRows(1);

  const sum = ss.getSheetByName("집계") || ss.insertSheet("집계");
  sum.clear();
  sum.getRange("A1").setValue("QR 접속 수 (QR별)");
  sum.getRange("A2").setFormula(
    "=QUERY(log!A:F, \"select D, count(A) where B = 'visit' and D is not null group by D label D '접속 QR', count(A) '접속 수'\", 1)");
  sum.getRange("D1").setValue("보내기 (문구 × 채널)");
  sum.getRange("D2").setFormula(
    "=QUERY(log!A:F, \"select C, count(A) where B = 'send' group by C pivot E label C '문구'\", 1)");
  sum.getRange("A10").setValue("탭 변경 (바꾼 뒤 문구)");
  sum.getRange("A11").setFormula(
    "=QUERY(log!A:F, \"select C, count(A) where B = 'tab' group by C label C '문구', count(A) '횟수'\", 1)");
  sum.getRange("D10").setValue("보내기 중 문구 수정 비율");
  sum.getRange("D11").setFormula(
    "=QUERY(log!A:F, \"select F, count(A) where B = 'send' group by F label F '수정', count(A) '건수'\", 1)");
}
