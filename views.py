import requests

def verify_turnstile(token):
    res = requests.post(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data={
            "secret": "0x4AAAAAADHRPsz7BGrK-U0Sd2ConCficI8",
            "response": token
        }
    )
    return res.json()["success"]  # 返回True就是验证成功
