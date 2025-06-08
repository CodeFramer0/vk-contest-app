import re
import time
from celery import shared_task
from django.conf import settings
from .models import User, Ticket
import vk_api


ACCESS_TOKEN = settings.ACCESS_TOKEN
GROUP_MAIN_ID = 130199528
GROUP_EXTRA_ID = 179939345
POST_ID = 25
OWNER_ID = -GROUP_MAIN_ID

KEYWORDS = {"участвую", "учавствую", "участие"}
SUBSCRIPTIONS = {
    GROUP_MAIN_ID: "СД «Спринтер» ДНР доставка озон, вб, СДЭК",
    GROUP_EXTRA_ID: "Отдых в Севастополе",
}


def get_vk():
    return vk_api.VkApi(token=ACCESS_TOKEN).get_api()


def get_existing_tickets():
    return set(Ticket.objects.values_list("number", flat=True))


def extract_number(text):
    match = re.search(r"(?:номер[^\d]*|№\s*)(\d+)", text.lower())
    return int(match.group(1)) if match else None


def build_reminder(unsubscribed):
    lines = "\n".join(f"• {name}" for name in unsubscribed)
    return (
        f"Чтобы участвовать в розыгрыше, нужно подписаться на:\n{lines}\n"
        "После подписки — повторно писать ничего не нужно 🙂")


def fetch_user_name(vk, user_id):
    try:
        data = vk.users.get(user_ids=user_id)[0]
        return f"{data['first_name']} {data['last_name']}"
    except:
        return "Имя не найдено"


def send_reply(vk, comment_id, message):
    try:
        vk.wall.createComment(
            owner_id=OWNER_ID,
            post_id=POST_ID,
            from_group=GROUP_MAIN_ID,
            reply_to_comment=comment_id,
            message=message,
        )
    except:
        pass


def check_subscriptions(vk, user_id):
    result = {}
    is_all = True
    for group_id, label in SUBSCRIPTIONS.items():
        try:
            member = vk.groups.isMember(group_id=group_id, user_id=user_id)
        except:
            member = False
        result[label] = member
        if not member:
            is_all = False
    return result, is_all


def should_skip_existing(comment, user_id):
    has_ticket = Ticket.objects.filter(user__vk_id=user_id).exists()
    if not has_ticket:
        return False

    replies = comment.get("thread", {}).get("items", [])
    already_answered = any(
        re.search(r"(номер|№)\s*\d+", r.get("text", "").lower()) for r in replies
    )
    return already_answered


def build_participant_set(vk):
    participants = {}
    offset = 0
    count = 100

    while True:
        response = vk.wall.getComments(
            owner_id=OWNER_ID,
            post_id=POST_ID,
            count=count,
            offset=offset,
            extended=1,
            thread_items_count=10,
        )

        comments = response.get("items", [])
        if not comments:
            break

        for comment in comments:
            user_id = comment.get("from_id")
            comment_id = comment["id"]
            text = comment.get("text", "").lower()

            if user_id <= 0 or not any(k in text for k in KEYWORDS):
                continue

            if should_skip_existing(comment, user_id):
                continue


            participants[comment_id] = {
                "user_id": user_id,
                "comment": text,
                "number": None,
                "reminder_sent": any(
                    "подпишись" in r.get("text", "").lower()
                    or "нужно подписаться" in r.get("text", "").lower()
                    for r in comment.get("thread", {}).get("items", [])
                ),
                "replies": comment.get("thread", {}).get("items", []),
            }

            for reply in comment.get("thread", {}).get("items", []):
                num = extract_number(reply.get("text", ""))
                if num:
                    participants[comment_id]["number"] = num

        offset += count
        time.sleep(0.34)

    return participants


@shared_task
def sync_vk_participants():
    vk = get_vk()
    used_numbers = get_existing_tickets()
    participants = build_participant_set(vk)

    for comment_id, entry in participants.items():
        user_id = entry["user_id"]
        user, _ = User.objects.get_or_create(
            vk_id=user_id, defaults={"full_name": fetch_user_name(vk, user_id)}
        )

        if entry["number"]:
            Ticket.objects.get_or_create(user=user, number=entry["number"])
            continue

        subs, is_subscribed = check_subscriptions(vk, user_id)

        if is_subscribed and not Ticket.objects.filter(user=user).exists():
            number = 1
            while number in used_numbers:
                number += 1
            Ticket.objects.create(user=user, number=number)
            used_numbers.add(number)
            send_reply(
                vk, comment_id, f"Приветствуем! Номер для участия в розыгрыше: {number}"
            )

        elif not is_subscribed and not entry["reminder_sent"]:
            unsubscribed = [name for name, ok in subs.items() if not ok]
            send_reply(vk, comment_id, build_reminder(unsubscribed))
