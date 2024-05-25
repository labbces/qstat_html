import xml.etree.ElementTree as ET

tree = ET.parse('/home/riano/qstat_html/qstatClsuter.xml')
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