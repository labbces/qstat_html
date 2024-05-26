import xml.etree.ElementTree as ET

tree = ET.parse('/home/riano/qstat_html/qstatCluster.xml')
root = tree.getroot()

# Extract queue information
queues = {}
for queue in root.findall('.//Queue-List'):
    queue_name = queue.find('name').text
    queue_info = {
        'slots_total': queue.find('slots_total').text,
        'slots_used': queue.find('slots_used').text,
        'load_avg': queue.find('load_avg').text,
        'jobs': []
    }

    for job in queue.findall('.//job_list'):
        job_info = {
            'JB_job_number': job.find('JB_job_number').text,
            'JB_name': job.find('JB_name').text,
            'JB_owner': job.find('JB_owner').text,
            'state': job.attrib['state'],
            'slots': job.find('slots').text,
        }
        if job.find('JAT_start_time') is not None:
            job_info['JAT_start_time'] = job.find('JAT_start_time').text
        if job.find('JB_submission_time') is not None:
            job_info['JB_submission_time'] = job.find('JB_submission_time').text
        
        queue_info['jobs'].append(job_info)
    
    queues[queue_name] = queue_info

# Extract pending job information
pending_jobs = []
for job in root.findall('.//job_info/job_list'):
    if job.attrib['state'] == 'pending':
        job_info = {
            'JB_job_number': job.find('JB_job_number').text,
            'JB_name': job.find('JB_name').text,
            'JB_owner': job.find('JB_owner').text,
            'state': job.attrib['state'],
            'slots': job.find('slots').text,
        }
        if job.find('JB_submission_time') is not None:
            job_info['JB_submission_time'] = job.find('JB_submission_time').text
        pending_jobs.append(job_info)

# Generate HTML
html_output = "<html><body>"
html_output = '''
<!doctype html>
<html lang=en-us>
 <head>
  <meta charset=utf-8>
  <meta name=viewport content="width=device-width,initial-scale=1">
  <meta http-equiv=x-ua-compatible content="IE=edge">
  <meta name=generator content="Wowchemy 5.2.0 for Hugo">
  <meta name=author content="Diego Mauricio Riaño-Pachón">
  <meta name=description content="Cluster reservations">
  <link rel=alternate hreflang=en-us href=http://labbces.cena.usp.br/infra/clusterReservations/>
  <meta name=theme-color content="rgb(0, 136, 204)">
  <link rel=stylesheet href=https://cdnjs.cloudflare.com/ajax/libs/academicons/1.9.0/css/academicons.min.css integrity="sha512-W4yqoT1+8NLkinBLBZko+dFB2ZbHsYLDdr50VElllRcNt2Q4/GSs6u71UHKxB7S6JEMCp5Ve4xjh3eGQl/HRvg==" crossorigin=anonymous>
  <link rel=stylesheet href=https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css integrity="sha256-FMvZuGapsJLjouA6k7Eo2lusoAX9i0ShlWFG6qt7SLc=" crossorigin=anonymous>
  <link rel=stylesheet href=https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.min.css integrity="sha512-1xoFisiGdy9nvho8EgXuXvnpR5GAMSjFwp40gSRE3NwdUdIMIKuPa7bqoUhLD0O/5tPNhteAsE5XyyMi5reQVA==" crossorigin=anonymous media=print onload="this.media='all'">
  <link rel=stylesheet href=/css/wowchemy.663f760f057c24e84dba1f1fb41072b6.css>
  <link rel=manifest href=/index.webmanifest>
  <link rel=icon type=image/png href=/media/icon_huce0f58322822551670f82da3d360b308_88239_32x32_fill_lanczos_center_2.png>
  <link rel=apple-touch-icon type=image/png href=/media/icon_huce0f58322822551670f82da3d360b308_88239_180x180_fill_lanczos_center_2.png>
  <link rel=canonical href=http://labbces.cena.usp.br/infra/clusterReservations/>
  <meta property="twitter:card" content="summary"><meta property="og:site_name" content="LabBCES">
  <meta property="og:url" content="http://labbces.cena.usp.br/infra/clusterReservations/">
  <meta property="og:title" content="clusterReservations/ | LabBCES">
  <meta property="og:description" content="Cluster reservations">
  <meta property="og:image" content="http://labbces.cena.usp.br/media/logo_hu4bdaa9ee68286360853798cab7d37789_78789_300x300_fit_lanczos_2.png">
  <meta property="twitter:image" content="http://labbces.cena.usp.br/media/logo_hu4bdaa9ee68286360853798cab7d37789_78789_300x300_fit_lanczos_2.png">
  <meta property="og:locale" content="en-us"><meta property="article:published_time" content="2024-03-12T23:04:24-02:00">
  <meta property="article:modified_time" content="2024-03-12T23:04:24-02:00">
  <title>Cluster Reservations | LabBCES</title>
 </head>
 <body id=top data-spy=scroll data-offset=70 data-target=#TableOfContents class="page-wrapper dark" data-wc-page-id=322dbaccf72a6d71f827fdb2866be935>
 <script src=/js/wowchemy-init.min.b986d8d769373f1d4df43d168c348bd4.js></script>
 <aside class=search-modal id=search>
 <div class=container>
 <section class=search-header><div class="row no-gutters justify-content-between mb-3">
 <div class=col-6><h1>Search</h1></div>
 <div class="col-6 col-search-close"><a class=js-search href=# aria-label=Close><i class="fas fa-times-circle text-muted" aria-hidden=true></i></a></div></div><div id=search-box><input name=q id=search-query placeholder=Search... autocapitalize=off autocomplete=off autocorrect=off spellcheck=false type=search class=form-control aria-label=Search...></div></section><section class=section-search-results><div id=search-hits></div></section></div></aside><div class=page-header><nav class="navbar navbar-expand-lg navbar-light compensate-for-scrollbar" id=navbar-main><div class=container-xl><div class="d-none d-lg-inline-flex"><a class=navbar-brand href=/><img src=/media/logo_hu4bdaa9ee68286360853798cab7d37789_78789_0x70_resize_lanczos_2.png alt=LabBCES></a></div><button type=button class=navbar-toggler data-toggle=collapse data-target=#navbar-content aria-controls=navbar-content aria-expanded=false aria-label="Toggle navigation">
<span>
<i class="fas fa-bars"></i>
</span>
</button>
<div class="navbar-brand-mobile-wrapper d-inline-flex d-lg-none">
<a class=navbar-brand href=/><img src=/media/logo_hu4bdaa9ee68286360853798cab7d37789_78789_0x70_resize_lanczos_2.png alt=LabBCES></a>
</div>
<div class="navbar-collapse main-menu-item collapse justify-content-end" id=navbar-content>
 <ul class="navbar-nav d-md-inline-flex">
  <li class=nav-item><a class=nav-link href=/post><span>News</span></a></li>
  <li class=nav-item><a class=nav-link href=/people><span>People</span></a></li>
  <li class=nav-item><a class=nav-link href=/project><span>Projects</span></a></li>
  <li class=nav-item><a class=nav-link href=/pictures><span>Pictures</span></a></li>
  <li class=nav-item><a class=nav-link href=/publication><span>Publications</span></a></li>
  <li class=nav-item><a class=nav-link href=/event><span>Events</span></a></li>
  <li class=nav-item><a class=nav-link href=/tools><span>Tools</span></a></li>
  <li class=nav-item><a class=nav-link href=/teaching><span>Teaching</span></a></li>
  <li class=nav-item><a class=nav-link href=/infra><span>Infraestructure</span></a></li>
  <li class=nav-item><a class=nav-link href=/contact><span>Contact</span></a></li>
 </ul>
</div>
<ul class="nav-icons navbar-nav flex-row ml-auto d-flex pl-md-2"><li class=nav-item><a class="nav-link js-search" href=# aria-label=Search><i class="fas fa-search" aria-hidden=true></i></a></li></ul></div></nav></div><div class=page-body><article class=article><div class="article-container pt-3">
'''

# Section 1: Queues and basic information
html_output += "<h1>Queue Information</h1>"
html_output += "<ul>"
for queue_name, queue_info in queues.items():
    html_output += f"<li><strong>{queue_name}</strong>: Slots Total: {queue_info['slots_total']}, Slots Used: {queue_info['slots_used']}, Load Avg: {queue_info['load_avg']}</li>"
html_output += "</ul>"

# Section 2: Running Jobs table
html_output += "<h1>Running Jobs Information</h1>"
html_output += "<table border='1'>"
html_output += "<tr><th>Queue</th><th>Job Number</th><th>Job Name</th><th>Job Owner</th><th>State</th><th>Slots</th><th>Start Time</th><th>Submission Time</th></tr>"
for queue_name, queue_info in queues.items():
    for job in queue_info['jobs']:
        html_output += "<tr>"
        html_output += f"<td>{queue_name}</td>"
        html_output += f"<td>{job['JB_job_number']}</td>"
        html_output += f"<td>{job['JB_name']}</td>"
        html_output += f"<td>{job['JB_owner']}</td>"
        html_output += f"<td>{job['state']}</td>"
        html_output += f"<td>{job['slots']}</td>"
        html_output += f"<td>{job.get('JAT_start_time', '')}</td>"
        html_output += f"<td>{job.get('JB_submission_time', '')}</td>"
        html_output += "</tr>"
html_output += "</table>"

# Section 3: Pending Jobs table
html_output += "<h1>Pending Jobs Information</h1>"
html_output += "<table border='1'>"
html_output += "<tr><th>Job Number</th><th>Job Name</th><th>Job Owner</th><th>State</th><th>Slots</th><th>Submission Time</th></tr>"
for job in pending_jobs:
    html_output += "<tr>"
    html_output += f"<td>{job['JB_job_number']}</td>"
    html_output += f"<td>{job['JB_name']}</td>"
    html_output += f"<td>{job['JB_owner']}</td>"
    html_output += f"<td>{job['state']}</td>"
    html_output += f"<td>{job['slots']}</td>"
    html_output += f"<td>{job.get('JB_submission_time', '')}</td>"
    html_output += "</tr>"
html_output += "</table>"

html_output += "</body></html>"

# Print HTML output
print(html_output)