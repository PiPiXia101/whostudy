# -*- coding: utf-8 -*-
import json

import scrapy


class CourseSpider(scrapy.Spider):
    name = 'course'
    allowed_domains = ['www.genshuixue.com']

    # start_urls = ['http://www.genshuixue.com/']
    url = 'https://www.genshuixue.com/pc/courseCenter?{}course=all&subjectId=0'
    url2 = 'https://www.genshuixue.com/sapi/viewLogic/selectCourse/courses?course=all&size=30&subjectId=0&gradeId={}&categoryId={}'
    def start_requests(self):
        yield scrapy.Request(
            url=self.url
        )

        pass

    def parse(self, response):
        categoryId_list = response.xpath("//div[@class='type'][2]/div[@class='fliter-list']/span")
        for categoryId in categoryId_list:
            cate = categoryId.xpath("./@data-id").get()
            param1 = 'categoryId=' + str(cate) + '&'
            url = self.url.format(param1)
            yield scrapy.Request(
                url=url,
                meta={
                    'cate': cate
                },
                callback=self.parse_gradeId
            )

    def parse_gradeId(self, response):
        cate = response.meta['cate']
        gradeId_list = response.xpath("//main/div[@class='type'][3]/div[@class='fliter-list']/span")
        for gradeId in gradeId_list:
            grad = gradeId.xpath("./@data-id").get()
            url = self.url2.format(grad,cate)
            yield scrapy.Request(
                url=url,
                callback=self.parse_json
            )

    def parse_json(self,response):
        obj_j = json.loads(response.text)
        result = obj_j['data']['items']
        for item in result:
            print(item['clazzName'])


