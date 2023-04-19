#!/usr/bin/python3
# -*- coding:utf-8 -*-
# TextChat
# PyCharm
# @Author:gaojing
# @Time: 2023/4/19 21:37

import argparse

from arxiv_daily import load_config, demo

def arxiv_daily_test():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path', type=str, default='config.yaml',
                        help='configuration file path')
    parser.add_argument('--update_paper_links', default=False,
                        action="store_true", help='whether to update paper links etc.')
    args = parser.parse_args()
    config = load_config(args.config_path)
    config = {**config, 'update_paper_links': args.update_paper_links}
    demo(**config)

if __name__ == '__main__':
    arxiv_daily_test()