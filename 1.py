'''
@Time : 2024-07-01 13:39
@Author : laolao
@FileName: 1.py

查找基因的url=https://www.ncbi.nlm.nih.gov/search/all/?term=GCA_001991095.1
信息基因的url=https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_001991095.1/?utm_source=gquery&utm_medium=referral&utm_campaign=KnownItemSensor:gb_assembly_id
'''
from time import sleep
import pandas  as pd
import requests
from lxml import html


def Send_Revision_History(asn):
    url = 'https://www.ncbi.nlm.nih.gov/datasets/api/datasets/v2alpha/genome/revision_history'
    sleep(0.3)
    headers = {
        'Host': 'www.ncbi.nlm.nih.gov',
        'Cookie': 'gdh-data-hub-csrftoken=VjdMkSGOTEeaxkdGd21QXojsIW27cBxI; ncbi_sid=E470006867D6E143_20133SID; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgJwGZsBCAYgQIIDCAIgEwDsAHAKK4CMArAAxce7lu2VSuWgDZsIogDoWkgLZxaIAL5A=; _gid=GA1.2.707638761.1719818457; _gat_dap=1; _ga_DP2X732JSX=GS1.1.1719818461.1.0.1719818461.0.0.0; _ga=GA1.1.1597956621.1719818457',
        'Content-Length': '31',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
        'Accept-Language': 'zh-CN',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Api-Key': '27cc0625ebd9931baf17439668edbef05c09',
        'X-Csrftoken': 'VjdMkSGOTEeaxkdGd21QXojsIW27cBxI',
        'Ncbi-Phid': '939BFBACD278E31500003C57DA37696F.1.m_7.09',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Origin': 'https://www.ncbi.nlm.nih.gov',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_001653455.1/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Priority': 'u=4, i'
    }
    data = {"accession": asn}
    response = requests.post(url, headers=headers, proxies={"http": None, "https": None}, json=data)
    sleep(0.3)
    GenomeStatus = 'WGS'
    try:
        if response.status_code == 200:
            parsed_data = response.json()
            if parsed_data['assembly_revisions'][0]['assembly_level'] == 'complete_genome':
                GenomeStatus = 'Complete'
        else:
            print(f'请求失败，状态码: {response.status_code}')
    except:
        pass
    return GenomeStatus


def Send_Chromosomes(asn):
    header = {'Host': 'www.ncbi.nlm.nih.gov',
              'Cookie': 'gdh-data-hub-csrftoken=VjdMkSGOTEeaxkdGd21QXojsIW27cBxI; ncbi_sid=E470006867D6E143_20133SID; '
                        'ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgJwGZsBCAYgQIIDCAIgEwDsAHAKK4CMArAAxce7lu2VSuWgDZsIogDoWkgLZxaIAL5A=; '
                        '_ga=GA1.2.1597956621.1719818457; _gid=GA1.2.707638761.1719818457; _gat_dap=1',
              'Content-Length': '133',
              'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
              'Accept-Language': 'zh-CN',
              'Sec-Ch-Ua-Mobile': '?0',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36',
              'Content-Type': 'application/json',
              'Accept': 'application/json, text/plain, */*',
              'Api-Key': '27cc0625ebd9931baf17439668edbef05c09',
              'X-Csrftoken': 'VjdMkSGOTEeaxkdGd21QXojsIW27cBxI',
              'Ncbi-Phid': '939BFBACD278E31500003C57DA37696F.1.m_7.08',
              'Sec-Ch-Ua-Platform': '"Windows"',
              'Origin': 'https://www.ncbi.nlm.nih.gov',
              'Sec-Fetch-Site': 'same-origin',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Dest': 'empty',
              'Referer': 'https://www.ncbi.nlm.nih.gov/datasets/genome/{}/'.format(asn),
              'Accept-Encoding': 'gzip, deflate, br',
              'Priority': 'u=4, i',
              }
    sleep(0.3)
    data = {"accession": asn, "role_filters": ["assembled-molecule"], "page_size": 1000,
            "count_assembly_unplaced": True, "page_token": ""}
    response = requests.post('https://www.ncbi.nlm.nih.gov/datasets/api/datasets/v2alpha/genome/sequence_reports',
                             headers=header, proxies={"http": None, "https": None}, json=data)
    sleep(0.3)
    GenomeStatus = ''
    Genbank_Accessions = []
    try:
        if response.status_code == 200:
            parsed_data = response.json()
            Genbank_Accessions = [report['genbank_accession'] for report in parsed_data['reports']]
            for report in parsed_data['reports']:
                if report['chr_name'].startswith('p'):
                    GenomeStatus = 'Plasmid'
        else:
            print(f'请求失败，状态码: {response.status_code}')
    except:
        # print("Chromosomes出错：{}".format(asn))
        # GenomeStatus = 'Error'
        pass

    return GenomeStatus, Genbank_Accessions


def Send_Isolation_Country(asn):
    header = {'Host': 'www.ncbi.nlm.nih.gov',
              'Cookie': 'gdh-data-hub-csrftoken=VjdMkSGOTEeaxkdGd21QXojsIW27cBxI; ncbi_sid=E470006867D6E143_20133SID; '
                        'ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgJwGZsBCAYgQIIDCAIgEwDsAHAKK4CMArAAxce7lu2VSuWgDZsIogDoWkgLZxaIAL5A=; '
                        '_ga=GA1.2.1597956621.1719818457; _gid=GA1.2.707638761.1719818457; _gat_dap=1',
              'Content-Length': '112',
              'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
              'Accept-Language': 'zh-CN',
              'Sec-Ch-Ua-Mobile': '?0',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36',
              'Content-Type': 'application/json',
              'Accept': 'application/json, text/plain, */*',
              'Api-Key': '27cc0625ebd9931baf17439668edbef05c09',
              'X-Csrftoken': 'VjdMkSGOTEeaxkdGd21QXojsIW27cBxI',
              'Ncbi-Phid': '939BFBACD278E31500003C57DA37696F.1.m_7.07',
              'Sec-Ch-Ua-Platform': '"Windows"',
              'Origin': 'https://www.ncbi.nlm.nih.gov',
              'Sec-Fetch-Site': 'same-origin',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Dest': 'empty',
              'Referer': 'https://www.ncbi.nlm.nih.gov/datasets/genome/{}/'.format(asn),
              'Accept-Encoding': 'gzip, deflate, br',
              'Priority': 'u=4, i'}
    data = {"accessions": [asn], "returned_content": "COMPLETE", "filters": {"assembly_version": "all_assemblies"}}
    geo_loc_name = ''
    response = requests.post('https://www.ncbi.nlm.nih.gov/datasets/api/datasets/v2alpha/genome/dataset_report',
                             headers=header, proxies={"http": None, "https": None}, json=data)
    try:
        if response.status_code == 200:
            parsed_data = response.json()
            for report in parsed_data['reports']:
                geo_loc_name = report['assembly_info']['biosample']['geo_loc_name']
        else:
            print(f'请求失败，状态码: {response.status_code}')
    except:
        # print("Isolation_Country没有：{}".format(asn))
        pass
    return geo_loc_name

def Send_Article(asn):
    header = {'Host': 'www.ncbi.nlm.nih.gov',
              'Cookie': 'gdh-data-hub-csrftoken=VjdMkSGOTEeaxkdGd21QXojsIW27cBxI; ncbi_sid=E470006867D6E143_20133SID; _gid=GA1.2.707638761.1719818457; WebEnv=1ZMmxp9c3Uo1uddJeAWr-ZNk9DlczhFo886O1t2XEPYkW%40E470006867D6E143_20133SID; _ga_DP2X732JSX=GS1.1.1719832778.3.1.1719836020.0.0.0; _ga=GA1.1.1597956621.1719818457; _ga_CSLL4ZEK4L=GS1.1.1719832778.3.1.1719836020.0.0.0; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgMIFEAc+AIgIwCsAYgGz4BMA7NSSQAxvvsAstRLAzAE4yAOgC2cWpxAAaEAFcAdgBsA9gENUCqAA8ALplC1MIKAt3QAXjJB9jCuQGMHK6NalYA5qYBGahQGtrMmNrKmMvBV8A63pjRF1RJWt8Y1oWawFjVCgAMzU5JX1ZZmMSaxJbLDLi9xBoc2RYKHLgqpJOPnoWegEhcrCsNSUk4tisPKUAZ2bilPGh6es04zxCUkoaBiZWDg5uXkERcUklsqxTcygLDHsnFygMCKj/DAA5AHlX3CWjLAB3AHCBQObzIIFKURA5CIYQeFQwJaZKpkPhhWR8dJYfBUKTos4gcio6x8X4gfAkNE2SogCaLdG1cxyGY2OYgYlIkA9ElGWScTEEkgCKhsNzUljCPnCdK82qKVQaLR6NytEDSkAo0ooylkWr0DFBAaqoJjI2yKj4vkkfBSAC+NqAA==',
              'Cache-Control': 'max-age=0',
              'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
              'Sec-Ch-Ua-Mobile': '?0',
              'Sec-Ch-Ua-Platform': '"Windows"',
              'Accept-Language': 'zh-CN',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
              'Sec-Fetch-Site': 'none',
              'Sec-Fetch-Mode': 'navigate',
              'Sec-Fetch-User': '?1',
              'Sec-Fetch-Dest': 'document',
              'Accept-Encoding': 'gzip, deflate, br',
              'Priority': 'u=0, i'}
    title=""
    url = 'https://www.ncbi.nlm.nih.gov/nuccore/{}/'.format(asn)
    print(url)
    response = requests.get(url, headers=header, proxies={"http": None, "https": None})
    try:
        tree = html.fromstring(response.content)
        content_value = tree.xpath("//meta[@name='ncbi_uidlist']/@content")[0]
        value = tree.xpath( "//input[@name='EntrezSystem2.PEntrez.Nuccore.Sequence_ResultsPanel.Sequence_DisplayBar.ncbi_phid']/@value")[0]
        url = 'https://www.ncbi.nlm.nih.gov/portal/loader/pload.cgi?curl=http%3A%2F%2Fwww.ncbi.nlm.nih.gov%2Fsviewer%2Fviewer.cgi%3Fid%3D{}%26db%3Dnuccore%26report%3Dgenbank%26conwithfeat%3Don%26hide-sequence%3Don%26hide-cdd%3Don%26retmode%3Dhtml%26ncbi_phid%3D{}%26withmarkup%3Don%26tool%3Dportal%26log%24%3Dseqview'.format(content_value, value)
        print(url)
        sleep(0.3)
        response = requests.get(url, headers=header, proxies={"http": None, "https": None})
        import re
        html_content = response.text
        pattern = re.compile(r'TITLE\s+(.*?)\s+JOURNAL', re.DOTALL)
        matches = pattern.findall(html_content)
        title = re.sub(r'\s+', ' ', matches[0]).strip()
    except:
        pass

    return title


if __name__ == '__main__':
    df = pd.read_excel("./hp_metadata.xlsx", sheet_name='S5')  # 修改地方1
    assembly = df['Assembly']
    Genbank_Accessions = []
    for row_index in range(len(assembly)):
        IsolationCountry = Send_Isolation_Country(assembly[row_index])
        GenomeStatus = Send_Revision_History(assembly[row_index])
        GS2, Genbank_Accessions = Send_Chromosomes(assembly[row_index])

        if GenomeStatus != 'WGS' and len(GS2) > 1:
             GenomeStatus = GenomeStatus + ',' + GS2

        article = ''
        for GenBank in Genbank_Accessions:
            article += Send_Article(GenBank) + '\n'

        df['Isolation Country'] = df['Isolation Country'].astype(str)
        df['article'] = df['article'].astype(str)

        df.at[row_index, 'Genome Status'] = GenomeStatus
        df.at[row_index, 'Isolation Country'] = IsolationCountry
        df.at[row_index, 'article'] = article

        print("[{}]:{}\n{}".format(row_index, assembly[row_index], df.iloc[row_index]['article']))

    df.to_excel('S5.xlsx', index=False)  # 修改地方2
