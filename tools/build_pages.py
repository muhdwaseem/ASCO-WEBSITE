"""Build /services/ and /contact/ from the homepage shell, and point both homepages at them.
Content is taken from the live ascoaudit.com /services/ and /contact/ pages (scraped 2026-10-12)."""
import os, re, sys
os.chdir(sys.argv[1])

SERVICES = [
    ("accounting", "Accounting &amp; Bookkeeping", "SAcc.jpg",
     "Professional management of your daily financial transactions, ensuring accurate ledgers, up-to-date reporting, and clear visibility into your business cash flow.",
     ["Daily ledger management", "Monthly financial reporting", "Bank reconciliations", "Accounts payable/receivable"]),
    ("vat-corporate-tax", "VAT &amp; Corporate Tax", "SCoTax.jpg",
     "Comprehensive FTA compliance, strategic tax planning, correct business registration, and highly accurate filing mechanisms to prevent any regulatory penalties.",
     ["VAT Registration &amp; Filing", "Tax Assessment &amp; Strategy", "Corporate Tax Registration", "FTA Audit Assistance"]),
    ("internal-audit", "Internal Audit", "SAudit.jpg",
     "Independent and objective evaluations designed to add value and improve your organization’s operations, risk management processes, and internal controls.",
     ["Risk Assessment", "Fraud Detection", "Process Optimization", "Governance Review"]),
    ("inventory", "Inventory Management", "Sinve.jpg",
     "Accurate stock valuation, physical counts, and the implementation of robust control systems to optimize your supply chain finances and prevent shrinkage.",
     ["Inventory Analysis", "Inventory Reconciliation", "Cost Analysis", "Inventory Reporting"]),
    ("valuation", "Valuation &amp; Due Diligence", "SValue.jpg",
     "Thorough financial assessments and accurate business valuations essential for mergers, acquisitions, partner buyouts, or seeking external investment.",
     ["Business Valuation", "Financial Due Diligence", "Investment Reviews", "Financial Analysis"]),
    ("e-invoicing", "Accounting Systems &amp; E-Invoicing", "SInvoice.jpg",
     "Seamless implementation of modern ERPs (Xero, Zoho, QuickBooks) and ensuring full compliance with the UAE’s upcoming e-invoicing mandates.",
     ["Accounting Software Setup", "System Migration", "Process Automation", "E-Invoicing Support"]),
    ("consultancy", "Management Consultancy", "SQ-Cube.jpg",
     "Strategic advice designed to help you restructure operations, reduce unnecessary overhead costs, and significantly improve long-term profitability.",
     ["Business Process Improvement", "Performance Evaluation", "Strategic Planning", "Operational Advisory"]),
    ("cfo", "Fractional CFO Services", "SCFO.jpg",
     "Executive-level financial strategy, forecasting, and guidance on a flexible, fractional basis. Get the expertise of a Chief Financial Officer without the full-time overhead.",
     ["Financial Modeling &amp; Forecasting", "Investor &amp; Board Reporting", "Cash Flow Optimization", "Strategic Scaling Advice"]),
]
# homepage card title -> slug
HOME_CARDS = {
    "Accounting &amp; Bookkeeping": "accounting", "VAT &amp; Corporate Tax": "vat-corporate-tax",
    "Internal Audit": "internal-audit", "Inventory Management": "inventory",
    "Accounting Systems &amp; E-Invoicing": "e-invoicing", "Valuation &amp; Due Diligence": "valuation",
    "Management Consultancy": "consultancy", "CFO Services": "cfo",
}
ADDRESS = "Burj Nahar Mall - B1-08, M2 Floor - Al Muteena, Deira, Dubai, UAE"

def R(s, a, b, n=1):
    assert a in s, "MISSING: " + a[:90]
    return s.replace(a, b, n)

def update_home(path):
    s = open(path, encoding="utf-8").read()
    if "svc__more" in s:
        print("already updated:", path); return
    css = "../assets/css/" if "../assets/css/styles.css" in s else "assets/css/"
    s = R(s, f'<link rel="stylesheet" href="{css}styles.css">', f'<link rel="stylesheet" href="{css}styles.css">\n<link rel="stylesheet" href="{css}pages.css">')
    s = R(s, 'href="https://ascoaudit.com/services/"', 'href="/services/"')
    s = R(s, 'href="https://ascoaudit.com/contact"', 'href="/contact/"')
    # blog post is empty on the live site -> stop linking out
    s, k = re.subn(r'<a class="post" href="https://ascoaudit\.com/do-small[^"]*">(.*?)</a>',
                   lambda m: '<div class="post post--soon">' + m.group(1).replace('Read more <svg class="ic"><use href="#i-arrow"/></svg>', 'Article coming soon') + '</div>',
                   s, flags=re.S)
    assert k == 1, "blog card not found"
    for title, slug in HOME_CARDS.items():
        i = s.index(f"<h3>{title}</h3>", s.index('class="bento"'))
        j = s.index("</article>", i)
        s = s[:j] + f'<a class="svc__more" href="/services/#{slug}">Learn more <svg class="ic"><use href="#i-arrow"/></svg></a>' + s[j:]
    s = R(s, '<div><h4>Services</h4><a href="#services">Accounting &amp; Bookkeeping</a><a href="#services">VAT &amp; Corporate Tax</a><a href="#services">Internal Audit</a><a href="#services">CFO Services</a></div>',
          '<div><h4>Services</h4><a href="/services/#accounting">Accounting &amp; Bookkeeping</a><a href="/services/#vat-corporate-tax">VAT &amp; Corporate Tax</a><a href="/services/#internal-audit">Internal Audit</a><a href="/services/#cfo">CFO Services</a><a href="/services/">All services →</a></div>')
    s = R(s, '<div><h4>Contact</h4><a href="tel:+971508216634">+971 50 821 6634</a><a href="https://wa.me/971508216634" target="_blank" rel="noopener">WhatsApp</a><span>Dubai, United Arab Emirates</span></div>',
          f'<div><h4>Contact</h4><a href="tel:+971508216634">+971 50 821 6634</a><a href="tel:+97143999143">+971 4 399 9143</a><a href="mailto:hello@ascoaudit.com">hello@ascoaudit.com</a><a href="https://wa.me/971508216634" target="_blank" rel="noopener">WhatsApp</a><span>{ADDRESS}</span><span>Sun–Thu, 9:00 AM – 6:00 PM (GST)</span><a href="/contact/">Contact page →</a></div>')
    s = R(s, '"address":{"@type":"PostalAddress","addressLocality":"Dubai","addressCountry":"AE"}',
          '"email":"hello@ascoaudit.com","address":{"@type":"PostalAddress","streetAddress":"Burj Nahar Mall - B1-08, M2 Floor, Al Muteena, Deira","addressLocality":"Dubai","addressCountry":"AE"},"openingHours":"Su-Th 09:00-18:00"')
    open(path, "w", encoding="utf-8").write(s)
    print("updated:", path)

update_home("index.html")
update_home("v2/index.html")

# ---------- shared shell taken from the (updated) v1 homepage ----------
home = open("index.html", encoding="utf-8").read()
def rootify(chunk):
    chunk = chunk.replace('"assets/', '"/assets/')
    chunk = chunk.replace('href="#contact"', 'href="/contact/"').replace('href="#top"', 'href="/"')
    return re.sub(r'href="#([a-z]+)"', r'href="/#\1"', chunk)
sprite = home[home.index("<!-- Icon sprite -->"):home.index('<a class="skip"')]
nav = rootify(home[home.index("<!-- ============ NAV ============ -->"):home.index('<main id="main">')])
foot = rootify(home[home.index('<footer class="footer">'):home.index("</body>")])
fonts = home[home.index('<link rel="preconnect" href="https://fonts.googleapis.com">'):home.index('<link rel="stylesheet" href="assets/css/styles.css">')]

def page(title, desc, body, canonical):
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="/assets/img/Reliable-1024x1024.jpg">
<meta name="theme-color" content="#0A1A2F">
<link rel="icon" href="/assets/img/cropped-SQ-LOGO-270x270.png">
{fonts}<link rel="stylesheet" href="/assets/css/styles.css">
<link rel="stylesheet" href="/assets/css/pages.css">
</head>
<body>

{sprite}<a class="skip" href="#main">Skip to content</a>

{nav}<main id="main">
{body}
</main>

{foot}</body>
</html>
'''

def hero(crumb, h1, lead, extra=""):
    return f'''
<section class="page-hero">
  <div class="hero__grid" aria-hidden="true"></div>
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span>{crumb}</span></nav>
    <h1>{h1}</h1>
    <p>{lead}</p>{extra}
  </div>
</section>'''

# ---------- /services/ ----------
jump = '\n    <div class="jump">' + "".join(f'<a href="#{slug}">{t.replace("Fractional ", "")}</a>' for slug, t, *_ in SERVICES) + "</div>"
rows = []
for n, (slug, title, img, desc, items) in enumerate(SERVICES, 1):
    lis = "".join(f"<li>{x}</li>" for x in items)
    rows.append(f'''    <article class="svc-row reveal" id="{slug}">
      <div class="svc-row__media"><img src="/assets/img/{img}" alt="{title} illustration" width="600" height="600" loading="lazy"></div>
      <div>
        <span class="svc-row__num">{n:02d} / 08</span>
        <h2>{title}</h2>
        <p>{desc}</p>
        <ul class="checklist">{lis}</ul>
        <div class="svc-row__actions">
          <a href="/contact/?service={slug}#enquiry" class="btn btn--primary">Enquire about this service <svg class="ic"><use href="#i-arrow"/></svg></a>
          <a href="https://wa.me/971508216634" class="btn btn--ghost" target="_blank" rel="noopener"><svg class="ic ic--fill"><use href="#i-whatsapp"/></svg>WhatsApp us</a>
        </div>
      </div>
    </article>''')
services_body = hero("Services", "Expert financial services <em>for businesses across the UAE</em>",
    "Accounting, taxation, auditing, and advisory services that help businesses stay compliant, organized, and financially informed.", jump) + f'''

<section class="section">
  <div class="container intro">
    <div class="reveal">
      <span class="eyebrow">Built around you</span>
      <h2 class="h2">Financial services designed around <em>your business needs</em></h2>
      <p>At ASCO, we provide accounting, taxation, auditing, and advisory services that help businesses stay compliant, organized, and financially informed.</p>
      <p>Whether you’re a startup, SME, or established company, our team delivers practical support tailored to your business requirements.</p>
    </div>
    <div class="intro__card reveal">
      <span class="eyebrow">We support it</span>
      <h2>How we support businesses</h2>
      <p>Every business has different financial priorities.</p>
      <p>From bookkeeping and tax compliance to auditing and strategic advisory, we provide the expertise and support needed to help businesses operate with confidence.</p>
    </div>
  </div>
</section>

<section class="section section--tint" id="list">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Our services</span>
      <h2 class="h2">Our expert <em>services</em></h2>
    </div>
{chr(10).join(rows)}
  </div>
</section>

<section class="cta">
  <div class="container cta__inner reveal">
    <div>
      <span class="eyebrow eyebrow--light">Get started</span>
      <h2 class="h2">Ready to optimize <em>your finances?</em></h2>
      <p>Take the guesswork out of your accounting and tax compliance. Partner with ASCO for reliable, long-term financial guidance.</p>
    </div>
    <div class="cta__actions">
      <a href="/contact/#enquiry" class="btn btn--light btn--lg">Book a Free Consultation <svg class="ic"><use href="#i-arrow"/></svg></a>
      <a href="https://wa.me/971508216634" class="btn btn--ghost btn--lg" target="_blank" rel="noopener"><svg class="ic ic--fill"><use href="#i-whatsapp"/></svg>Get in Touch</a>
    </div>
  </div>
</section>'''
os.makedirs("services", exist_ok=True)
open("services/index.html", "w", encoding="utf-8").write(page(
    "Services — ASCO | Accounting, VAT, Audit &amp; CFO Services in the UAE",
    "Accounting & bookkeeping, VAT & Corporate Tax, internal audit, inventory, valuation, e-invoicing, consultancy and fractional CFO services for UAE businesses.",
    services_body, "/services/"))

# ---------- /contact/ ----------
opts = "".join(f'<option value="{slug}">{t}</option>' for slug, t, *_ in SERVICES) + '<option value="not-sure">Not sure yet</option>'
contact_body = hero("Contact", "Let’s discuss your <em>business requirements</em>",
    "Whether you’re looking for accounting support, tax guidance, audit services, or simply need professional advice, our team is here to help.") + f'''

<section class="section">
  <div class="container contact-grid">
    <div class="reveal">
      <span class="eyebrow">Get in touch</span>
      <h2 class="h2">Reach out <em>any way you like</em></h2>
      <p class="lead">Reach out to us through any of the channels below. We typically respond within 24 hours during business days.</p>
      <div class="info-cards">
        <div class="info-card"><span class="pillars__ic"><svg class="ic"><use href="#i-target"/></svg></span><div><h3>Location</h3><p>{ADDRESS}</p></div></div>
        <div class="info-card"><span class="pillars__ic"><svg class="ic"><use href="#i-chat"/></svg></span><div><h3>Email</h3><a href="mailto:hello@ascoaudit.com">hello@ascoaudit.com</a></div></div>
        <div class="info-card"><span class="pillars__ic"><svg class="ic"><use href="#i-phone"/></svg></span><div><h3>Phone</h3><a href="tel:+971508216634">+971 50 821 6634</a><br><a href="tel:+97143999143">+971 4 399 9143</a></div></div>
        <div class="info-card"><span class="pillars__ic"><svg class="ic"><use href="#i-calendar"/></svg></span><div><h3>Business hours</h3><p>Sunday – Thursday, 9:00 AM – 6:00 PM (GST)</p></div></div>
      </div>
    </div>
    <div class="enquiry reveal" id="enquiry">
      <h2>Send us an enquiry</h2>
      <p>Fill in a few details and we’ll pick up the conversation on WhatsApp.</p>
      <form class="lead-form" id="leadForm">
        <label>Your name<input name="name" required autocomplete="name" placeholder="Full name"></label>
        <label>Company<input name="company" autocomplete="organization" placeholder="Company name"></label>
        <label>Phone<input name="phone" type="tel" autocomplete="tel" placeholder="+971 …"></label>
        <label>Email<input name="email" type="email" autocomplete="email" placeholder="you@company.com"></label>
        <label class="full">Service needed<select name="service">{opts}</select></label>
        <label class="full">Message<textarea name="message" placeholder="Tell us briefly what you need help with"></textarea></label>
        <button class="btn btn--light btn--lg full" type="submit"><svg class="ic ic--fill"><use href="#i-whatsapp"/></svg>Send enquiry</button>
        <small class="full">Opens WhatsApp with your details. Prefer email? Write to <a href="mailto:hello@ascoaudit.com" style="text-decoration:underline">hello@ascoaudit.com</a>.</small>
      </form>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Visit our office</span>
      <h2 class="h2">We’re conveniently <em>located in Dubai</em></h2>
      <p class="lead">Schedule an in-person meeting with our team to discuss your business requirements.</p>
    </div>
    <div class="map reveal"><iframe title="ASCO office location on Google Maps" src="https://www.google.com/maps?q=Burj+Nahar+Mall,+Al+Muteena,+Deira,+Dubai&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="notsure reveal">
      <div>
        <span class="eyebrow">Get started</span>
        <h2 class="h2">Not sure what <em>service you need?</em></h2>
        <p>That’s perfectly fine. Many business owners contact us before they know exactly what type of support they require. We’ll take the time to understand your situation, answer your questions, and help you identify the most suitable solution for your business.</p>
      </div>
      <div class="notsure__actions">
        <a href="https://wa.me/971508216634" class="btn btn--primary btn--lg" target="_blank" rel="noopener"><svg class="ic ic--fill"><use href="#i-whatsapp"/></svg>Schedule a consultation</a>
        <a href="tel:+971508216634" class="btn btn--ghost btn--lg"><svg class="ic"><use href="#i-phone"/></svg>Call ASCO</a>
      </div>
    </div>
  </div>
</section>'''
os.makedirs("contact", exist_ok=True)
open("contact/index.html", "w", encoding="utf-8").write(page(
    "Contact ASCO — Accounting &amp; Tax Advisors in Deira, Dubai",
    "Contact ASCO: Burj Nahar Mall, Al Muteena, Deira, Dubai. Call +971 50 821 6634 or email hello@ascoaudit.com. Sunday–Thursday, 9 AM – 6 PM.",
    contact_body, "/contact/"))
print("built services/ and contact/")
