HEAD = """
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"><link type="text/css" rel="stylesheet" href="resources/sheet.css">
    <style type="text/css">.ritz .waffle a { color: inherit; }.ritz .waffle .s0{background-color:#ffffff;text-align:left;color:#000000;font-family:'Arial';font-size:10pt;vertical-align:bottom;white-space:nowrap;direction:ltr;padding:2px 3px 2px 3px;}
    </style>
  </head>"""

SCRIPT = """
<script type="text/javascript" nonce="v09iOen6bNHXwr037zaRjg">
function posObj(sheet, id, row, col, x, y) {
  var rtl = false;
  var sheetElement = document.getElementById(sheet);
  if (!sheetElement) {
    sheetElement = document.getElementById(sheet + '-grid-container');
  }
  if (sheetElement) {
    rtl = sheetElement.getAttribute('dir') == 'rtl';
  }
  var r = document.getElementById(sheet+'R'+row);
  var c = document.getElementById(sheet+'C'+col);
  if (r && c) {
    var objElement = document.getElementById(id);
    var s = objElement.style;
    var t = y;
    while (r && r != sheetElement) {
      t += r.offsetTop;
      r = r.offsetParent;
    }
    var offsetX = x;
    while (c && c != sheetElement) {
      offsetX += c.offsetLeft;
      c = c.offsetParent;
    }
    if (rtl) {
      offsetX -= objElement.offsetWidth;
    }
    s.left = offsetX + 'px';
    s.top = t + 'px';
    s.display = 'block';
    s.border = '1px solid #000000';
  }
};
function posObjs() {
};
posObjs();
</script>
"""


class Th:
    def __init__(self, text, size):
        self.html = """
            <th id="0C0" style="width:{}px" class="column-headers-background">{}</th>
        """.format(size, text)

    def get_html(self):
        return self.html


class Tr:
    def __init__(self):
        self.tds = ""
        self.html = """
            <tr style="height:20px;">
              <th id="0R0" style="height: 20px;" class="row-headers-background">
                <div class="row-header-wrapper" style="line-height: 20px;"></div>
              </th>
              {}
            </tr>
        """
        pass

    def add_td(self, text):
        self.tds += '<td class="s0" dir="ltr">{}</td>'.format(text)

    def get_html(self):
        return self.html.format(self.tds)


class Table:

    def __init__(self):
        self.ths = ""
        self.trs = ""
        self.html = """
            <div>
                <table class="waffle" cellspacing="0" cellpadding="0">
                  <thead>
                    <tr>
                      <th class="row-header freezebar-origin-ltr"></th>
                      {th}
                    </tr>
                  </thead>
                  <tbody>
                    {tr}
                  </tbody>
                </table>
              </div>
        """
        pass

    def add_th(self, text, size=100):
        self.ths += Th(text, size).get_html()

    def add_tr(self, tr: Tr):
        self.trs += tr.get_html()

    def get_html(self):
        return self.html.format(th=self.ths, tr=self.trs)


class HtmlFile:

    def __init__(self):
        self.html = "<html>{head}<body>{body}{script}</body></html>"
        self.body = ""
        pass

    def title(self, title):
        self.body += '<font size="5" face="verdana, sans-serif"><i>{}</i></font><br><br><br>'.format(title)

    def paragraphTitle(self, title):
        self.body += '<b><font size="4" face="verdana, sans-serif"><i>{}</i></font></b><br><br>'.format(title)

    def seccionTitle(self, title):
        self.body += '<font size="4" face="verdana, sans-serif"><i>{}</i></font><br><br>'.format(title)

    def add_br(self, count=1):
        self.body += ('<br>' * count)

    def add_table(self, table: Table):
        self.body += table.get_html()+"<br>"

    def get_html(self):
        return self.html.format(head=HEAD, body=self.body, script=SCRIPT)