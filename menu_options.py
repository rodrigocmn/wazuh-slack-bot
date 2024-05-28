

class MenuOptions:
    greeting = ""
    
    def get_menu_options(self, greeting: str):

        
        # Respond with a menu of options
        options = [
            {
                "text": {
                    "type": "plain_text",
                    "text": "MacOS Apple Silicon"
                },
                "value": "mac_silicom"
            },
            {
                "text": {
                    "type": "plain_text",
                    "text": "MacOS Intel"
                },
                "value": "mac_intel"
            },
            {
                "text": {
                    "type": "plain_text",
                    "text": "Windows"
                },
                "value": "win"
            },
            {
                "text": {
                    "type": "plain_text",
                    "text": "Linux (Debian based)"
                },
                "value": "lin_deb"
            },
            {
                "text": {
                    "type": "plain_text",
                    "text": "Linux (RedHat based)"
                },
                "value": "lin_red"
            }
        ]
        
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": greeting
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an option"
                    },
                    "options": options,
                    "action_id": "select_option"
                }
            }
        ]
        return (blocks)