import os
import replicate


def query(model_params):
    try:
        replicate_ = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
        output = replicate_.run(
            "nateraw/mistral-7b-openorca:7afe21847d582f7811327c903433e29334c31fe861a7cf23c62882b181bacb88",
            input=model_params)

        answer = ""
        for item in output:
            answer += item
        return answer
    except:
        return ""
