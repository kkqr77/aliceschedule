import datetime

# Schedule for each day of the week
schedule = {
    "Monday": [
        "",
        "",
    ],
    "Tuesday": [
        "",
        "",
        "",
        "",
    ],
    "Wednesday": [
        "",
    ],
    "Thursday": [
        "",
    ],
    "Friday": [
        "",
        "",
        "",
        "",
    ],
    "Saturday": [
        "",
        "",
    ],
    "Sunday": [
        "Выходной, ура!"
    ]
}
# Helper to get the schedule for a specific day
def get_schedule(day):
    if day in schedule:
        if day == "Monday":
            return f"Расписание на понедельник:\n" + "\n".join(schedule[day])
        elif day == "Tuesday":
            return f"Расписание на вторник:\n" + "\n".join(schedule[day])
        elif day == "Wednesday":
            return f"Расписание на среду:\n" + "\n".join(schedule[day])
        elif day == "Thursday":
            return f"Расписание на четверг:\n" + "\n".join(schedule[day])
        elif day == "Friday":
            return f"Расписание на пятницу:\n" + "\n".join(schedule[day])
        elif day == "Saturday":
            return f"Расписание на субботу:\n" + "\n".join(schedule[day])
        elif day == "Sunday":
            return f"Расписание на выходной:\n" + "\n".join(schedule[day])
        else:
            return f"Расписание на {day}:\n" + "\n".join(schedule[day])
    else:
        return "Нет расписания."

# Function to map user input to a specific day
def get_requested_day(user_input):
    days = {
        "на понедельник": "Monday",
        "на вторник": "Tuesday",
        "на среду": "Wednesday",
        "на четверг": "Thursday",
        "на пятницу": "Friday",
        "на субботу": "Saturday",
        "на воскресенье": "Sunday",
        "на завтра": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%A"),
        "на послезавтра": (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%A"),
        "на сегодня": (datetime.datetime.now().strftime("%A"))
    }
    
    # Normalize user input to lowercase and check if it's in the dictionary
    user_input = user_input.strip().lower()
    if user_input in days:
        return days[user_input]
    else:
        return None
        
# Main handler
def handler(event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """

    # Get current day of the week
    current_day = datetime.datetime.now().strftime("%A")
    user_input = None
    
    # Session state check (if the session is new or ongoing)
    if 'session' in event and event['session']['new']:
        # First interaction: give today's schedule
        text = get_schedule(current_day)
        follow_up_question = "На какой день сказать расписание?"
        text += f"\n\n{follow_up_question}"
    else:
        # Follow-up interaction: check user input
        if 'request' in event and 'original_utterance' in event['request']:
            user_input = event['request']['original_utterance'].strip().lower()
        
        day_requested = get_requested_day(user_input)
        
        if day_requested:
            text = get_schedule(day_requested)
        else:
            text = "Я не панимаю"

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false'
        },
    }
