from openai import OpenAI
import requests

# ✅ Direct OpenAI API key
client = OpenAI(api_key="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")

# Function to fetch real-time gold and silver prices
def get_metal_prices():
    try:
        response = requests.get(
            "https://api.metals.live/v1/spot"  # Free public metals API
        )
        data = response.json()
        gold_price = None
        silver_price = None
        for item in data:
            if "gold" in item:
                gold_price = item["gold"]
            if "silver" in item:
                silver_price = item["silver"]
        return gold_price, silver_price
    except Exception as e:
        return None, None


def get_investment_advice(user_message):
    try:
        gold_price, silver_price = get_metal_prices()

        # Include real-time pricing data if available
        price_info = ""
        if gold_price and silver_price:
            price_info = f"Current gold price: ${gold_price}/oz, silver price: ${silver_price}/oz."
        else:
            price_info = "Real-time pricing data is currently unavailable."

        # Make Jarvis aware of current prices
        prompt = (
            f"You are Jarvis, an intelligent financial advisor. "
            f"{price_info} Respond conversationally to: {user_message}"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Jarvis, a friendly and knowledgeable AI financial advisor. "
                        "If the user says they want to invest, respond with something like: "
                        "'Great! We can begin your first investment journey on Jarvis!'"
                        "Then end your message with the keyword: [INVEST_NOW]"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=250,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Sorry, there was an error getting investment advice: {str(e)}"
