import replicate


def query(model_params):
    try:
        replicate_ = replicate.Client(api_token='r8_PKF16BOJySVj5Qmhn6PvWKkqv6tW47J2kiCO1')
        output = replicate_.run(
            "nateraw/mistral-7b-openorca:7afe21847d582f7811327c903433e29334c31fe861a7cf23c62882b181bacb88",
            model_kwargs=model_params)

        answer = ""
        for item in output:
            answer += item
        return answer
    except:
        return ""
