import logging
from menu_options import MenuOptions
from scripts_generator import ScriptsGenerator

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

# process_before_response must be True when running on FaaS
app = App(process_before_response=True)


@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()

# global definiton for command
command = "/wazuh"


def respond_to_slack_within_3_seconds(body, ack):
    if body.get("text") == "help":
        ack(f":x: Usage: {command} (description here)")
    else:
        ack()

# retrieve user real name from slack
def get_real_name(user_id):
    try:
        result = app.client.users_info(user=user_id)
        if result['ok']:
            real_name = result['user']['profile']['real_name']
            return real_name
    except Exception as e:
        print(f"Error fetching user info: {e}")
        return None, None

# handle wazuh bot command
def process_request(respond, body):
    if body.get("text") == "install":
        # retrieve user identification from sender
        user_id = body["user_id"]
        # define the greeting message
        greeting = f"Hi <@{user_id}>, please choose your platform to install the wazuh agent:"
        # instanciate menu
        options = MenuOptions()
        
        respond(
            blocks=options.get_menu_options(greeting)
        )
    else:
        respond("I got nothing!")


# Handle the option selection
@app.action("select_option")
def handle_option_selection(ack, body, respond):
    # Acknowledge the action
    ack()
    
    real_name = get_real_name(body["user"]["id"])
    real_name_script = real_name.replace(' ','.').lower()
    
    message_os = f"{real_name}, below is the script you need to run on your laptop to install the wazuh agent in your"
    message_service = "after the installation, you will need to start the agent:"
    selected_option = body["actions"][0]["selected_option"]["text"]["text"]
    
    scripts = ScriptsGenerator().generate_scripts(selected_option,real_name_script)
    
    respond(f"{message_os} {selected_option}: \n ```{scripts[0]}``` \n {message_service} \n ```{scripts[1]}```")
    

app.command(command)(ack=respond_to_slack_within_3_seconds, lazy=[process_request])

SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)


