
/* eslint-disable */
let idTmr;
const getExplorer = () => {
  let explorer = window.navigator.userAgent;
  //ie
  if (explorer.indexOf("MSIE") >= 0) {
    return 'ie';
  }
  //firefox

  else if (explorer.indexOf("Firefox") >= 0) {
    return 'Firefox';
  }
  //Chrome
  else if (explorer.indexOf("Chrome") >= 0) {
    return 'Chrome';
  }
  //Opera
  else if (explorer.indexOf("Opera") >= 0) {
    return 'Opera';
  }
  //Safari
  else if (explorer.indexOf("Safari") >= 0) {
    return 'Safari';
  }
}
// �ж�������Ƿ�ΪIE
const exportToExcel = (data,name) => {

  // �ж��Ƿ�ΪIE
  if (getExplorer() == 'ie') {
    tableToIE(data, name)
  } else {
    tableToNotIE(data,name)
  }
}

const Cleanup = () => {
  window.clearInterval(idTmr);
}

// ie�������ִ��
const tableToIE = (data, name) => {
  let curTbl = data;
  let oXL = new ActiveXObject("Excel.Application");

  //����AX����excel
  let oWB = oXL.Workbooks.Add();
  //��ȡworkbook����
  let xlsheet = oWB.Worksheets(1);
  //���ǰsheet
  let sel = document.body.createTextRange();
  sel.moveToElementText(curTbl);
  //�ѱ���е������Ƶ�TextRange��
  sel.select;
  //ȫѡTextRange������
  sel.execCommand("Copy");
  //����TextRange������
  xlsheet.Paste();
  //ճ�������EXCEL��

  oXL.Visible = true;
  //����excel�ɼ�����

  try {
    let fname = oXL.Application.GetSaveAsFilename("Excel.xls", "Excel Spreadsheets (*.xls), *.xls");
  } catch (e) {
    print("Nested catch caught " + e);
  } finally {
    oWB.SaveAs(fname);

    oWB.Close(savechanges = false);
    //xls.visible = false;
    oXL.Quit();
    oXL = null;
    // ����excel���̣��˳����
    window.setInterval("Cleanup();", 1);
    idTmr = window.setInterval("Cleanup();", 1);
  }
}

// ��ie�������ִ��
const tableToNotIE = (function() {
  // ����Ҫ��utf-8��ȻĬ��gbk�������������
  let uri = 'data:application/vnd.ms-excel;base64,',
    template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><meta charset="UTF-8"><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>',
    base64 = function(s) {
      return window.btoa(unescape(encodeURIComponent(s)));

    },

    format = (s, c) => {
      return s.replace(/{(\w+)}/g,
        (m, p) => {
          return c[p];
        })
    }
  return (table, name) => {
    let ctx = {
      worksheet: name,
      table
    }

    //��������
    let link = document.createElement('a');
    link.setAttribute('href', uri + base64(format(template, ctx)));

    link.setAttribute('download', name);


    // window.location.href = uri + base64(format(template, ctx))
    link.click();
  }
})()