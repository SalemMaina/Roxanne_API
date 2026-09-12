from django.utils import timezone


def generate_receipt_text(order):
    """
    Builds the immutable receipt snapshot text for an order.
    Called once, at order-creation time, in the view.
    """
    lines = [f"Receipt — {order.store.name}", f"Order #{order.id}", ""]
    for item in order.items.all():
        lines.append(f"{item.quantity} x {item.name} @ {item.unit_price} = {item.line_total}")
    lines.append("")
    lines.append(f"Total: {order.total_amount}")
    return "\n".join(lines)


def send_receipt_sms(receipt):
    """
    Sends the receipt via SMS. Stubbed for now — will call Africa's
    Talking's API once that integration is wired up. Kept as its own
    function so it can be mocked in tests without touching view logic.
    """
    order = receipt.order
    try:
        # TODO: replace with real Africa's Talking API call
        print(f"[STUB SMS] To {order.customer_phone}:\n{receipt.receipt_text}")
        receipt.sms_status = receipt.SmsStatus.SENT
        receipt.sent_at = timezone.now()
    except Exception:
        receipt.sms_status = receipt.SmsStatus.FAILED
    receipt.save()
    return receipt