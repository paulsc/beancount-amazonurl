from beancount.core.data import Transaction

__plugins__ = ['amazon_url']

# Regex pattern for Amazon order IDs (3-7-7 digit format)
RE_AMZN_ORDER = r"\b[D\d]\d{2}-\d{7}-\d{7}\b"

def amazon_url(entries, options_map):
    errors = []
    for entry in entries:
        if isinstance(entry, Transaction):
            payee = getattr(entry, 'payee', '')
            if payee and 'amazon' in payee.lower():
                import re
                match = re.search(RE_AMZN_ORDER, entry.narration)
                if match:
                    order_id = match.group(0)
                    url = f"https://www.amazon.de/gp/your-account/order-details?orderID={order_id}"
                    entry.meta["url"] = url
    return entries, errors
