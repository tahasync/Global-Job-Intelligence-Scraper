import scrapy
import csv
import os

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['rozee.pk']

    def start_requests(self):
        # The spider is run from the scrapy_project directory
        file_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../../data/raw/job_links.csv'))
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return
            
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row['job_url']
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        from w3lib.html import remove_tags
        import json
        
        item = {
            'Job URL': response.url,
            'Job title': '', 'Company name': '', 'Location': '',
            'Job description': '', 'Required skills': '',
            'Employment type': 'N/A', 'Department / team': 'N/A', 'Posted date': 'N/A'
        }
        
        # Try JSON-LD first
        ld_scripts = response.css('script[type="application/ld+json"]::text').getall()
        for script in ld_scripts:
            try:
                data = json.loads(script.strip())
                if data.get('@type') == 'JobPosting':
                    item['Job title'] = data.get('title', item['Job title'])
                    item['Company name'] = data.get('hiringOrganization', {}).get('name', item['Company name'])
                    # Location might be complex object
                    loc = data.get('jobLocation', {})
                    if isinstance(loc, dict):
                        item['Location'] = loc.get('address', {}).get('addressLocality', item['Location'])
                    elif isinstance(loc, list) and loc:
                        item['Location'] = loc[0].get('address', {}).get('addressLocality', item['Location'])
                    
                    item['Job description'] = remove_tags(data.get('description', '')).strip()
                    item['Employment type'] = data.get('employmentType', item['Employment type'])
                    item['Posted date'] = data.get('datePosted', item['Posted date'])
                    item['Required skills'] = data.get('skills', item['Required skills'])
            except Exception:
                pass
                
        # Fallbacks for missing data
        if not item['Job title']:
            item['Job title'] = response.css('h1::text').get() or response.css('.jbtitle::text').get() or ''
        if not item['Company name']:
            item['Company name'] = response.css('.cname::text').get() or response.xpath('//h2//text()').get() or ''
        if not item['Job description']:
            texts = response.css('.job-description ::text').getall() or response.css('.jdisc ::text').getall()
            item['Job description'] = ' '.join(t.strip() for t in texts if t.strip())

        yield item
