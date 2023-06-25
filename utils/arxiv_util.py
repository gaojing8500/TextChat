#!/usr/bin/python3
# -*- coding:utf-8 -*-
# TextChat
# PyCharm
# @Author:gaojing
# @Time: 2023/6/25 22:35
import arxiv
from loguru import logger
import requests


class ArxivUtils(object):
    def __init__(self):
        self.description = "ArxivUtils description"
        self.arxiv_url = "http://arxiv.org/"
        self.base_url = "https://arxiv.paperswithcode.com/api/v0/papers/"
        ##设置科研领域，作为订阅方式
        self.reaserch_domain_list = ["Artificial Intelligence", "Computation and Language",
                                     "Computer Vision and Pattern Recognition"]

    def get_search_domain_keys(self):
        EXCAPE = '\"'
        QUOTA = ''  # NO-USE
        OR = 'OR'  # TODO
        ret = ''
        for idx in range(0, len(self.reaserch_domain_list)):
            filter = self.reaserch_domain_list[idx]
            if len(filter.split()) > 1:
                ret += (EXCAPE + filter + EXCAPE)
            else:
                ret += (QUOTA + filter + QUOTA)
            if idx != len(self.reaserch_domain_list) - 1:
                ret += OR
        return ret

    def get_authors(self,authors, first_author=False):
        output = str()
        if first_author == False:
            output = ", ".join(str(author) for author in authors)
        else:
            output = authors[0]
        return output

    def get_domain_similarity_paper(self,domain_description,domain):
        pass

    def get_submit_time_papers(self, topic, query, max_results=2):
        # output 根据提交时间来获取paper
        content = dict()
        content_to_web = dict()
        ##根据提交在时间来搜索
        search_engine = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        for result in search_engine.results():

            paper_id = result.get_short_id()
            paper_title = result.title
            paper_url = result.entry_id
            code_url = self.base_url + paper_id  # TODO
            paper_abstract = result.summary.replace("\n", " ")
            paper_authors = self.get_authors(result.authors)
            paper_first_author = self.get_authors(result.authors, first_author=True)
            primary_category = result.primary_category
            publish_time = result.published.date()
            update_time = result.updated.date()
            comments = result.comment

            logger.info(f"Time = {update_time} title = {paper_title} author = {paper_first_author}")

            # eg: 2108.09112v1 -> 2108.09112
            ver_pos = paper_id.find('v')
            if ver_pos == -1:
                paper_key = paper_id
            else:
                paper_key = paper_id[0:ver_pos]
            paper_url = self.arxiv_url + 'abs/' + paper_key

            try:
                # source code link
                r = requests.get(code_url).json()
                repo_url = None
                if "official" in r and r["official"]:
                    repo_url = r["official"]["url"]
                # TODO: not found, two more chances
                # else:
                #    repo_url = get_code_link(paper_title)
                #    if repo_url is None:
                #        repo_url = get_code_link(paper_key)
                if repo_url is not None:
                    content[paper_key] = "|**{}**|**{}**|{} et.al.|[{}]({})|**[link]({})**|\n".format(
                        update_time, paper_title, paper_first_author, paper_key, paper_url, repo_url)
                    content_to_web[paper_key] = "- {}, **{}**, {} et.al., Paper: [{}]({}), Code: **[{}]({})**".format(
                        update_time, paper_title, paper_first_author, paper_url, paper_url, repo_url, repo_url)

                else:
                    content[paper_key] = "|**{}**|**{}**|{} et.al.|[{}]({})|null|\n".format(
                        update_time, paper_title, paper_first_author, paper_key, paper_url)
                    content_to_web[paper_key] = "- {}, **{}**, {} et.al., Paper: [{}]({})".format(
                        update_time, paper_title, paper_first_author, paper_url, paper_url)

                # TODO: select useful comments
                comments = None
                if comments != None:
                    content_to_web[paper_key] += f", {comments}\n"
                else:
                    content_to_web[paper_key] += f"\n"

            except Exception as e:
                logger.error(f"exception: {e} with id: {paper_key}")

        data = {topic: content}
        data_web = {topic: content_to_web}
        return data, data_web

    def get_daily_paper(self):
        topic = "Artificial Intelligence"
        keywords = self.get_search_domain_keys()
        self.get_papers(topic, keywords)
