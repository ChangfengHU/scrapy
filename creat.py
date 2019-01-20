from scrapy import cmdline
# cmdline.execute("scrapy jobbole jobbole.com".split())
cmdline.execute("scrapy genspider -t crawl jobbole  lagou.com ".split())