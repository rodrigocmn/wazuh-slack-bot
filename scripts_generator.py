

class ScriptsGenerator:
    def generate_scripts(self, option: str, username: str):
        os_script = "not found!"
        os_service = "not found!"
        
        
        # Select the respective script
            
        match option:
            case "mac_silicom":
                os_script = f"""curl -so wazuh-agent.pkg https://packages.wazuh.com/4.x/macos/wazuh-agent-4.7.2-1.arm64.pkg && echo "WAZUH_MANAGER='agent.wazuh.codurance.com' && WAZUH_AGENT_GROUP='Laptop' && WAZUH_AGENT_NAME='{username}.laptop.mac'" > /tmp/wazuh_envs && sudo installer -pkg ./wazuh-agent.pkg -target /"""
                os_service = "sudo /Library/Ossec/bin/wazuh-control start"
            case "mac_intel":
                os_script = f"""curl -so wazuh-agent.pkg https://packages.wazuh.com/4.x/macos/wazuh-agent-4.7.2-1.intel64.pkg && echo "WAZUH_MANAGER='agent.wazuh.codurance.com' && WAZUH_AGENT_GROUP='Laptop' && WAZUH_AGENT_NAME='{username}.laptop.mac'" > /tmp/wazuh_envs && sudo installer -pkg ./wazuh-agent.pkg -target /"""
                os_service = "sudo /Library/Ossec/bin/wazuh-control start"
            case "win":
                os_script = f"""Invoke-WebRequest -Uri https://packages.wazuh.com/4.x/windows/wazuh-agent-4.7.2-1.msi -OutFile ${{env.tmp}}\wazuh-agent; msiexec.exe /i ${{env.tmp}}\wazuh-agent /q WAZUH_MANAGER='agent.wazuh.codurance.com' WAZUH_AGENT_GROUP='Laptop' WAZUH_AGENT_NAME='{username}.laptop.mac' WAZUH_REGISTRATION_SERVER='agent.wazuh.codurance.com' """
                os_service = "NET START WazuhSvc"
            case "lin_red":
                os_script = f"""curl -o wazuh-agent-4.7.2-1.x86_64.rpm https://packages.wazuh.com/4.x/yum/wazuh-agent-4.7.2-1.x86_64.rpm && sudo WAZUH_MANAGER='agent.wazuh.codurance.com' WAZUH_AGENT_GROUP='Laptop' WAZUH_AGENT_NAME='{username}.laptop.mac' rpm -ihv wazuh-agent-4.7.2-1.x86_64.rpm"""
                os_service = """sudo systemctl daemon-reload
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent"""    
            case "lin_deb":
                os_script = f"""wget https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.7.2-1_amd64.deb && sudo WAZUH_MANAGER='agent.wazuh.codurance.com' WAZUH_AGENT_GROUP='Laptop' WAZUH_AGENT_NAME='{username}.laptop.mac' dpkg -i ./wazuh-agent_4.7.2-1_amd64.deb"""
                os_service = """sudo systemctl daemon-reload
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent""" 

        return(os_script,os_service)