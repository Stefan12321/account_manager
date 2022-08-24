import user_agent

from user_agent import generate_user_agent

CHROME_BUILDS = """89.0.4389.23
90.0.4430.24
91.0.4472.19
104.0.5112.20
103.0.5060.134
103.0.5060.53
103.0.5060.24
102.0.5005.61
102.0.5005.27
101.0.4951.41
101.0.4951.15
100.0.4896.60
100.0.4896.20
99.0.4844.51
99.0.4844.35
99.0.4844.17
98.0.4758.102
98.0.4758.80
98.0.4758.48
97.0.4692.71
97.0.4692.36
97.0.4692.20
96.0.4664.45
96.0.4664.35
96.0.4664.18
95.0.4638.69
95.0.4638.54
95.0.4638.17
95.0.4638.10
94.0.4606.113
94.0.4606.61
94.0.4606.41
93.0.4577.63
93.0.4577.15
92.0.4515.107
92.0.4515.43
91.0.4472.101
""".strip().splitlines()


def get_user_agent(os=None, navigator=None, platform=None,
                        device_type=None):
    """
    Generates HTTP User-Agent header

    :param os: limit list of os for generation
    :type os: string or list/tuple or None
    :param navigator: limit list of browser engines for generation
    :type navigator: string or list/tuple or None
    :param device_type: limit possible oses by device type
    :type device_type: list/tuple or None, possible values:
        "desktop", "smartphone", "tablet", "all"
    :return: User-Agent string
    :rtype: string
    :raises InvalidOption: if could not generate user-agent for
        any combination of allowed oses and navigators
    :raise InvalidOption: if any of passed options is invalid
    """
    user_agent.base.CHROME_BUILD += CHROME_BUILDS
    return generate_user_agent(os=os, navigator=navigator, platform=platform,
                        device_type=device_type)


if __name__ == '__main__':
    print(get_user_agent(os=("win"), navigator=("chrome"), device_type=("desktop")))
