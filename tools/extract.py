"""Turn a downloaded WordPress/Elementor page into readable text (headings, paragraphs, list items)."""
import sys, re
from html.parser import HTMLParser

SKIP = {"script", "style", "noscript", "svg", "header", "footer", "nav", "form"}
BLOCK = {"h1": "# ", "h2": "## ", "h3": "### ", "h4": "#### ", "h5": "##### ", "h6": "###### ", "p": "", "li": "- ", "a": ""}

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.stack = []
        self.out = []
        self.buf = ""

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        elif tag in BLOCK and tag != "a":
            self.flush()
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
        elif tag in BLOCK and tag != "a":
            self.flush()
            if self.stack:
                self.stack.pop()

    def handle_data(self, d):
        if not self.skip:
            self.buf += d

    def flush(self):
        t = re.sub(r"\s+", " ", self.buf).strip()
        if t:
            prefix = BLOCK.get(self.stack[-1], "") if self.stack else ""
            self.out.append(prefix + t)
        self.buf = ""

p = P()
p.feed(open(sys.argv[1], encoding="utf-8", errors="ignore").read())
p.flush()
seen, lines = set(), []
for line in p.out:
    if line not in seen:  # Elementor duplicates blocks for mobile/desktop
        seen.add(line)
        lines.append(line)
print("\n".join(lines))
