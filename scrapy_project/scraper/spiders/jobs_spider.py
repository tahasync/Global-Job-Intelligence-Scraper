import scrapy
import csv
import os

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    # Expanded to support common ATS platforms
    allowed_domains = ['rozee.pk', 'lever.co', 'greenhouse.io', 'ashbyhq.com']

    def start_requests(self):
        # Resolve the link file relative to the spider's location
        file_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../../data/raw/job_links.csv'))
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return
            
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row['job_url']
                yield scrapy.Request(url, callback=self.parse)

    def _get_source(self, url):
        if 'rozee.pk' in url: return 'Rozee.pk'
        if 'discord' in url: return 'Discord'
        if 'palantir' in url: return 'Palantir'
        if 'figma' in url: return 'Figma'
        if 'github' in url: return 'Github'
        if 'mustakbil' in url: return 'Mustakbil'
        if 'netflix' in url: return 'Netflix'
        if 'dropbox' in url: return 'Dropbox'
        return 'Other'

    def parse(self, response):
        from w3lib.html import remove_tags
        import json
        
        item = {
            'Job URL': response.url,
            'Source': self._get_source(response.url),
            'Job title': '', 'Company name': '', 'Location': '',
            'Job description': '', 'Required skills': '',
            'Employment type': 'N/A', 'Department / team': 'N/A', 'Posted date': 'N/A'
        }
        
        # 1. Try JSON-LD (Standard for Lever, Greenhouse, Ashby)
        ld_scripts = response.css('script[type="application/ld+json"]::text').getall()
        for script in ld_scripts:
            try:
                data = json.loads(script.strip())
                # Handle both single objects and lists of objects
                if isinstance(data, list):
                    data = data[0]
                    
                if data.get('@type') == 'JobPosting':
                    item['Job title'] = data.get('title', item['Job title'])
                    item['Company name'] = data.get('hiringOrganization', {}).get('name', item['Company name'])
                    
                    # Location parsing
                    loc = data.get('jobLocation', {})
                    if isinstance(loc, dict):
                        address = loc.get('address', {})
                        if isinstance(address, dict):
                            item['Location'] = address.get('addressLocality', item['Location'])
                        else:
                            item['Location'] = str(address)
                    
                    item['Job description'] = remove_tags(data.get('description', '')).strip()
                    item['Employment type'] = data.get('employmentType', item['Employment type'])
                    item['Posted date'] = data.get('datePosted', item['Posted date'])
                    item['Required skills'] = data.get('skills', item['Required skills'])
            except Exception:
                pass
                
        # 2. CSS Fallbacks for specific platforms
        if not item['Job title']:
            item['Job title'] = (
                response.css('h1.section-header::text').get() or
                response.css('h1::text').get() or 
                response.css('h2.posting-header::text').get() or 
                response.css('.app-title::text').get() or 
                response.css('title::text').get() or
                ''
            ).strip().split('|')[0].strip()

        if not item['Company name']:
            # Try logo alt text first (common in new Greenhouse)
            item['Company name'] = (
                response.css('.logo img::attr(alt)').get() or
                response.css('meta[property="og:site_name"]::attr(content)').get() or
                response.css('.company-name::text').get() or
                response.css('title::text').re_first(r'at (.*)') or
                ''
            ).strip()

        if not item['Location']:
            item['Location'] = (
                response.css('.job__location div::text').get() or
                response.css('.location::text').get() or
                response.css('.posting-categories .location::text').get() or
                ''
            ).strip()

        if not item['Job description']:
            # Common containers for descriptions
            desc_selectors = ['.job-description', '.description', '.posting-description', '#content', 'article', '.body']
            for sel in desc_selectors:
                texts = response.css(f'{sel} ::text').getall()
                if texts:
                    item['Job description'] = ' '.join(t.strip() for t in texts if t.strip())
                    break

        yield item
