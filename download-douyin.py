import re
from urllib import parse
from pprint import pprint
from datetime import datetime

import requests

# 注意Referer 和 user-agent都要正确，从浏览器取
headers = {
    'cookie': 'store-region=cn-fj; store-region-src=uid; LOGIN_STATUS=1; ttwid=1%7CSsOuAJK0k_yfZYwl9U47vzAn_eFUjpZto6ZgJMatP8o%7C1699938321%7C071e8c5c124046cec19bfcf83c1e24219d7dc5b5474a27fb8003f8e10d6790a4; douyin.com; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; webcast_local_quality=null; passport_csrf_token=50338423ab50f05a26f6108255ed0fc6; passport_csrf_token_default=50338423ab50f05a26f6108255ed0fc6; strategyABtestKey=%221699938324.215%22; s_v_web_id=verify_loxvdxt7_4WllqSSX_vxAb_4v0Q_8OJQ_lpodS8pZi4PU; n_mh=avpyv7AbG_zZx80bAhGEtbIxXeOSVET3QDnzOKWZUb4; publish_badge_show_info=%220%2C0%2C0%2C1699938390091%22; _bd_ticket_crypt_doamin=2; __security_server_data_status=1; csrf_session_id=7dcca4cde7c7edb47712a6cc6bc913ae; my_rd=2; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1700557413524%2C%22type%22%3A1%7D; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.6%7D; __ac_signature=_02B4Z6wo00f01eu5DKAAAIDAYPKXQHdgmhXrmQgAAB-.xnNfrA7ROGRoOoAirMu2NnwCryMkfiSR.qxPNgOMhmiO.p3P1fOV0pms4YrsAmmyMAO7vwBpMjAAXkIa8IjtEYkqy3TB4mhsGgRFa8; download_guide=%223%2F20231114%2F1%22; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; passport_assist_user=Cj1QmcI2S4BWBCBVRRr6lwcESzXoAZnDXXxg2bbGUHOgxpPMkW-uGuwxzjGeFkHE4Y3XfUW7Nj3iKA1HHShTGkoKPJF1wRDwBLhn0od47AaVymvhhAYYPblkTzTrYnlzgb07ErKERW-rGDjFqQfpyyRWkL4NV7c6D0I5NmZbMxDdpsENGImv1lQgASIBAzlhTwo%3D; sso_uid_tt=5f3bbd6830d09e3e2a6dcb2d872f211d; sso_uid_tt_ss=5f3bbd6830d09e3e2a6dcb2d872f211d; toutiao_sso_user=994a0ea379777c42682cf3b8794ba613; toutiao_sso_user_ss=994a0ea379777c42682cf3b8794ba613; sid_ucp_sso_v1=1.0.0-KGZhMTQ5ZjEzZjc5MDViMDdhOTA4MDAxYzMyMzBkMmEyOWIwMjZhNDAKHQjJnLKh_wIQl57OqgYY7zEgDDD60rvbBTgGQPQHGgJsZiIgOTk0YTBlYTM3OTc3N2M0MjY4MmNmM2I4Nzk0YmE2MTM; ssid_ucp_sso_v1=1.0.0-KGZhMTQ5ZjEzZjc5MDViMDdhOTA4MDAxYzMyMzBkMmEyOWIwMjZhNDAKHQjJnLKh_wIQl57OqgYY7zEgDDD60rvbBTgGQPQHGgJsZiIgOTk0YTBlYTM3OTc3N2M0MjY4MmNmM2I4Nzk0YmE2MTM; odin_tt=3963ae23e72fdd1f550b1a4e67e25ee9c9b687d962156735b692786b3525f7cbec192eedaef286d7332527f02b4e616618ef5d7443fad0960af25ff041290203; passport_auth_status=8d98339b985038d5d54ad2d17b2c41e1%2C2844fb4da0b85659139f94216b57e0b2; passport_auth_status_ss=8d98339b985038d5d54ad2d17b2c41e1%2C2844fb4da0b85659139f94216b57e0b2; uid_tt=5372dc660863bac1109e0c4465fee5a4; uid_tt_ss=5372dc660863bac1109e0c4465fee5a4; sid_tt=a35b90faad51bf89cf1bf7077b178664; sessionid=a35b90faad51bf89cf1bf7077b178664; sessionid_ss=a35b90faad51bf89cf1bf7077b178664; __ac_nonce=065538f190061989dbfa4; _bd_ticket_crypt_cookie=64320e5400da91e12d3dfe00a4d48dbd; sid_guard=a35b90faad51bf89cf1bf7077b178664%7C1699974939%7C5183999%7CSat%2C+13-Jan-2024+15%3A15%3A38+GMT; sid_ucp_v1=1.0.0-KGI5YzQ0MDk1OTBhMWMyNmQ2MzI2MWRhZDFlZjkzOTY3MWY4MDM3ZDIKGQjJnLKh_wIQm57OqgYY7zEgDDgGQPQHSAQaAmxxIiBhMzViOTBmYWFkNTFiZjg5Y2YxYmY3MDc3YjE3ODY2NA; ssid_ucp_v1=1.0.0-KGI5YzQ0MDk1OTBhMWMyNmQ2MzI2MWRhZDFlZjkzOTY3MWY4MDM3ZDIKGQjJnLKh_wIQm57OqgYY7zEgDDgGQPQHSAQaAmxxIiBhMzViOTBmYWFkNTFiZjg5Y2YxYmY3MDc3YjE3ODY2NA; passport_fe_beating_status=true; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A2195%2C%5C%22screen_height%5C%22%3A1235%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAH15TwGvaycDpNFJWiyiKIuTDWEkuKzcTqli_H2h8I70%2F1699977600000%2F0%2F0%2F1699977046382%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAH15TwGvaycDpNFJWiyiKIuTDWEkuKzcTqli_H2h8I70%2F1699977600000%2F0%2F1699976446383%2F0%22; msToken=w4-NtRzm2ET2vdQ6r69tfkyEl1VXA9ohxDUyCGXcNPnzwuItaTKPQ5fNtEfBYuKvOYAmCgoqux15Jt38k7k6Q9tEXfTqM38J4lvPtup62Nx66UwBp7yGAI89XC16tKA=; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTHFKTTcvWHllTGJWU1ZsTlhQL2VMaTk5YmtDYm1hcS9CQXV4aXI0dnRrUlZaTzNuNmt4OS94ZzNMcUhueHFrVEJMZ1hUNy9uMTQ0anFzUE1kRlF3bDA9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; tt_scid=jpsdmXYHWd6-sxlRMWLmf2yGGvlYmMJc-tSRsIPTMCt9ozfvpfLkJH5B62clJSjdb0c3; msToken=o29nIAyIxAmM19_TCXAAatFilyqcj3FfiQzDP188FvsKiFIu6sDxNG_y5jnuDcc5pwdgJIvacGRE1aFUoNcwBIMPag7bTxmoYqj5TD1-av6_-zMZwbD40pN7c1XUUXzf; pwa2=%223%7C0%7C3%7C1%22; home_can_add_dy_2_desktop=%220%22; IsDouyinActive=true',
    'Referer': 'https://www.douyin.com/user/MS4wLjABAAAA2e2u-pYCsUB85UcOB5hxaMe9Wi0Tv2eoaHxwjz7VSaE?vid=7284619915955375415',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}



# 博主的作品
# url = 'https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAA2e2u-pYCsUB85UcOB5hxaMe9Wi0Tv2eoaHxwjz7VSaE&max_cursor=0&locate_item_id=7284619915955375415&locate_query=false&show_live_replay_strategy=1&need_time_list=1&time_list_query=0&whale_cut_token=&cut_version=1&count=18&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2195&screen_height=1235&browser_language=en-US&browser_platform=Win32&browser_name=Chrome&browser_version=119.0.0.0&browser_online=true&engine_name=Blink&engine_version=119.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7301179433061533199&msToken=o29nIAyIxAmM19_TCXAAatFilyqcj3FfiQzDP188FvsKiFIu6sDxNG_y5jnuDcc5pwdgJIvacGRE1aFUoNcwBIMPag7bTxmoYqj5TD1-av6_-zMZwbD40pN7c1XUUXzf&X-Bogus=DFSzswVY1BhANCMrtmUvHPt/pL31'
# 我的喜欢列表
# url = 'https://www.douyin.com/aweme/v1/web/aweme/favorite/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAAH15TwGvaycDpNFJWiyiKIuTDWEkuKzcTqli_H2h8I70&max_cursor=0&min_cursor=0&whale_cut_token=&cut_version=1&count=18&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2195&screen_height=1235&browser_language=en-US&browser_platform=Win32&browser_name=Chrome&browser_version=119.0.0.0&browser_online=true&engine_name=Blink&engine_version=119.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7301179433061533199&msToken=TcJaEFqQh4-Ll_dia5FMOWj5YiGlt4sldQmghhXk5eXy64p3BCCQ5ZwlaXkd6s4_aMEtTgvCi2d4FPuFTbMUI3cPWHVLg12ciw5Z22g7-m_XCSvMd-Uz4v9O37vUwfVT&X-Bogus=DFSzswVO/9bANtOstmUyT-t/pLvH'
# url = 'https://www.douyin.com/aweme/v1/web/aweme/favorite/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAAH15TwGvaycDpNFJWiyiKIuTDWEkuKzcTqli_H2h8I70&max_cursor=1698608213000&min_cursor=0&whale_cut_token=&cut_version=1&count=18&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2195&screen_height=1235&browser_language=en-US&browser_platform=Win32&browser_name=Chrome&browser_version=119.0.0.0&browser_online=true&engine_name=Blink&engine_version=119.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7301179433061533199&msToken=vJIge_1ulukuXsQ1lWMIwN8dx74b1bRKqokX4OCL0QErbqQzFS1yuzhIdZo4od84gZpYq906QJN5bOX_EM26swdw7WBnEcEt6ntw-gBw-tX4TjwvmaES5sCX6n-9oQst&X-Bogus=DFSzswVYFyJANCMrtmUayat/pL3m'
url = 'https://www.douyin.com/aweme/v1/web/aweme/favorite/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAAH15TwGvaycDpNFJWiyiKIuTDWEkuKzcTqli_H2h8I70&max_cursor=1697568460000&min_cursor=0&whale_cut_token=&cut_version=1&count=18&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2195&screen_height=1235&browser_language=en-US&browser_platform=Win32&browser_name=Chrome&browser_version=119.0.0.0&browser_online=true&engine_name=Blink&engine_version=119.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7301179433061533199&msToken=TermagFmAn7PBcxOqD5VShj5AK3gX0_UfOkWW_Q4M3mpzT2buqTT1H0jijgjlFUP4nfrty7Dm53CUlqkuiPNR5KvyvEevvI_6TQ0J_GmWnqz9iIxNemNwoQmv3Mz2EvI&X-Bogus=DFSzswVYOKhANCMrtmWDP-t/pLfJ'
# url = 'https://www.douyin.com/aweme/v1/web/aweme/favorite/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAAH15TwGvaycDpNFJWiyiKIuTDWEkuKzcTqli_H2h8I70&max_cursor=1696336357000&min_cursor=0&whale_cut_token=&cut_version=1&count=18&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2195&screen_height=1235&browser_language=en-US&browser_platform=Win32&browser_name=Chrome&browser_version=119.0.0.0&browser_online=true&engine_name=Blink&engine_version=119.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7301179433061533199&msToken=kmP_0Okz0P-R_R58yoYO5Ybfy7RAVWAiE-1ZrMcDvjMew2MQNzV-RbZvdRyXckuegpY4kSUnGH4FNQksr84XOZYjmHQ2-dCK_1QZk1NcGn1Sl5jNHpWxSdfjj1r2XogO&X-Bogus=DFSzswVYy/GANCMrtmWd-Pt/pL3q'

# https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request
resp = requests.get(url, headers=headers)
# pprint(resp.json())
json = resp.json()
aweme_list = json['aweme_list']
for i in aweme_list:
    ## 替换标题的特殊字符
    # pprint(i['desc'])
    video_title = re.findall('[\u4e00-\u9fa5|\d]',i['desc'])
    video_title2 = ''.join(str(x) for x in video_title)
    create_time = datetime.utcfromtimestamp(i['create_time']).strftime('%Y%m%d')
    video_title2 = create_time + '-' + i['author']['nickname'] + '-' + video_title2
    # pprint(video_title2)
    video_url = i['video']['play_addr']['url_list'][0]
    pprint(video_url)

    try:
        video_stream = requests.get(video_url, stream=True)
    except:
        pass
    file_size1 = int(video_stream.headers['Content-Length']) / 1024 / 1024  # 提取出来的是个数字str

    s = 0
    with open(f"抖音喜欢列表\{video_title2}.mp4", 'wb') as data:  # 打开文件
        for i in video_stream.iter_content(chunk_size=1024):  # 分批写入1MB=1024KB
            s += 1024
            value = float('%.2f' % (s / 1024 / 1024))
            ratio = value / file_size1 * 100  # 在总量的百分比
            # file_size是总大小 s是每次运行的大小
            print("\r{}MB/{}MB {:.2f}%[{}>{}]".format(int(file_size1), int(value), ratio, int(int(ratio) / 5) * '█',
                                                      int((100 - int(ratio)) / 5) * "."), end='')
            data.write(i)  # 写入
    print(f'{video_title2}写入完成')



