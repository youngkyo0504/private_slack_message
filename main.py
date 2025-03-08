from bull_market import bull_market
from kimp import get_tether_premium
from slack import post_block_message
from risk import get_risk_info
import os

access_token = os.environ["MY_GITHUB_TOKEN"]
slack_token = os.environ["SLACK_TOKEN"]

# 각 함수에서 Block Kit 형식의 블록 리스트를 받아옴
btc_blocks = bull_market("KRW-BTC")
tether_blocks = get_tether_premium()
risk_info = get_risk_info("BTC")

risk_blocks = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "📊 비트코인 리스크 분석",
            "emoji": True
        }
    },
    {
        "type": "section",
        "fields": [
            {
                "type": "mrkdwn",
                "text": f"*현재 리스크 레벨:*\n{risk_info['current_risk']}"
            }
        ]
    },
    {
        "type": "divider"
    }
]

# 모든 블록 합치기
all_blocks = btc_blocks + tether_blocks + risk_blocks

# Slack에 Block Kit 형식으로 메시지 보내기
# post_message 함수가 blocks 인자를 받을 수 있도록 수정 필요
post_block_message(
    slack_token,
    "#알람",
    all_blocks
)
