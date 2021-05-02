# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import YoutubeItem
from scrapy_splash import SplashRequest
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError




class Channel(Spider):
    name = 'channel'
    allowed_domains = ['www.youtube.com']

    def __init__(self, domain='', *args, **kwargs):
        super(Channel, self).__init__(*args, **kwargs)
        self.start_urls = [domain]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                meta={'handle_httpstatus_all': True},
                endpoint='render.html',
                args={'wait': 0.5},
            )


    def parse(self, response):
        
        htx = Selector(response)
        videos = htx.xpath("//ol[contains(@id,'playlist-autoscroll-list')]" \
        "//li[contains(@class,'yt-uix-scroller-scroll-unit')]")
        for video in videos:
            video_item = YoutubeItem()
            video_item['thumbnail_url'] = video.xpath("a//img/@src").extract_first()
            url = video.xpath("a/@href").extract_first()
            video_item['url'] = "https://www.youtube.com" + url
            video_item['title'] = video.xpath("a/div[contains(@class,'playlist-video-description')]/h4/text()").extract_first()
            request = SplashRequest(video_item['url'], self.parse_video,
                endpoint='render.html',
                args={'wait': 1})
            request.meta['item'] = video_item
            yield request

    def parse_video(self, response):
        video_resonse = Selector(response)
        video_item = response.meta['item']        
        views_txt = video_resonse.xpath("//div[contains(@class,'watch-view-count')]/text()").extract_first()
        video_item['views'] = re.findall('\d+', views_txt.replace(",", ""))[0]
        yield video_item

    def errback(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)