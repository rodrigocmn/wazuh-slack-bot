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

# wazuh bot help definition
def get_help():
    # initialise list and append commands
    helplist = ["/wazuh help       - Show this help message."]
    helplist.append("/wazuh install     - Automatically generates the wazuh agent install scripts.")
    helplist = '\n'.join(helplist)
    
    return f"These are the available commands for the wazuh bot: \n```\n{helplist}\n```"

# respond to slack within 3 seconds (required to handle actions, commands and views submissions from Slack)
def respond_to_slack_within_3_seconds(body, ack):
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
    command_text = body.get("text") 
    
    if command_text == "help":
        respond(get_help())
    elif command_text == "install":
        # retrieve user identification from sender
        user_id = body["user_id"]
        # define the greeting message
        greeting = f"Hi <@{user_id}>, please choose your platform to install the wazuh agent:"
        
        respond(
            blocks=MenuOptions().get_menu_options(greeting)
        )
    else:
        respond("Command not found. Please use '/wazuh help' to check the valid commands.")


# handle the option selection
@app.action("select_option")
def handle_option_selection(ack, body, respond):
    # Acknowledge the action
    ack()
    
    # retrieve user identification from sender
    user_id = body["user"]["id"]
    
    # get user real name and format for script (use "." instead of spaces)
    name_for_script = get_real_name(user_id).replace(' ','.').lower()
    
    # generate messages and scripts
    message_os = f"<@{user_id}>, below is the script you need to run on your laptop to install the wazuh agent in your"
    message_service = "after the installation, you will need to start the agent:"
    scripts = ScriptsGenerator().generate_scripts(body["actions"][0]["selected_option"]["value"],name_for_script)
    
    # respond to user
    respond(f"{message_os} {body["actions"][0]["selected_option"]["text"]["text"]}: \n ```{scripts[0]}``` \n {message_service} \n ```{scripts[1]}```")
    
# configure app for wazuh commands and use lazy listeners feature
app.command("/wazuh")(ack=respond_to_slack_within_3_seconds, lazy=[process_request])

SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)


