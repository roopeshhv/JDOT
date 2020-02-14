import os
import paramiko
import json
import requests

from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient

from build_check import get_build_url

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_client = SlackClient(slack_bot_token)

#REST call constants
JARVIS_URL = "https://jarvis.eng.nutanix.com"

def get_fvm():
  fp = open('fvm_pool.json', "r")
  fvm = fp.read()
  fp.close()
  fvm = json.loads(fvm)
  return fvm.get("foundation_ip")[0]

def download_build_to_fvm(fvm_ip, build_url):
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(fvm_ip, username='nutanix', password='nutanix/4u')
  stdin, stdout, stderr = client.exec_command('cd /home/nutanix/foundation/nos; wget %s' %build_url)
  client.close()

def get_available_images(fvm_ip):
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(fvm_ip, username='nutanix', password='nutanix/4u')
  stdin, stdout, stderr = client.exec_command('ls /home/nutanix/foundation/nos')
  available_images = stdout.read().split('\n')
  client.close()
  return available_images

def check_nos_availability(available_images, nos_name):
  """
  This routine checks if NOS already present in FVM.
  """
  print 'available_images', available_images
  print 'nos_name', nos_name
  return nos_name in available_images

# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    # If the incoming message contains "hi", then respond with a "Hello" message
    message_text = message.get('text')
    print "message_text:", message_text
    if message.get("subtype") is None and 'get cluster' in message_text:
          channel = message["channel"]
          cluster_name = message_text.split()[3]
          request_url = JARVIS_URL + '/api/v1/nodes/' + cluster_name
          resp = requests.get(request_url, verify=False).json()
          response = "SVM_IP: " + resp['data']['svm_ip'] +"\n" + "SVM_VERSION: " + resp['data']['svm_version']
          slack_client.api_call("chat.postMessage", channel=channel, text=response)

    elif message.get("subtype") is None and 'image nodes' in message_text and '--help' in message_text:
              print "message_text:", message_text
              print len(message_text)
              channel = message["channel"]
              command = "image nodes <node1> <node2> cluster_name=<CLUSTER_NAME> nos=<NOS_VERSION> fvm=<FVM_IP>\n"
              example = 'Example:\n\t image nodes catania6-1 catania6-2 cluster_name=catania nos=master fvm=10.47.99.231'
              response = command + example 
              slack_client.api_call("chat.postMessage", channel=channel, text=response)

    elif message.get("subtype") is None and 'image nodes' in message_text and '--help' not in message_text:
              channel = message["channel"]
              arguments = message_text.split()[3:]
              args_list = []
              kwargs_dict = {}
              for arg in arguments:
                  if '=' not in arg:
                       args_list.append(arg)
                  else:
                       kwargs_dict[arg.split('=')[0]] = arg.split('=')[1]
              print args_list, kwargs_dict
              args_list = map(str, args_list)
              node_config = {}
              node_config['node_name'] = ','.join(args_list)
              if 'cluster_name' in kwargs_dict:
                  node_config['cluster_name'] = kwargs_dict['cluster_name']

              node_config['nos'] = kwargs_dict.get('nos', 'master')
              build_url = get_build_url(version=node_config['nos'])
              node_config['nos_name'] = build_url['nos_package']
              print node_config['nos_name']
 
              node_config['fvm'] = kwargs_dict.get('fvm', get_fvm())
              available_images = get_available_images(node_config['fvm'])
              if not check_nos_availability(available_images, node_config['nos_name']):
                  print 'Downloading...'
                  download_build_to_fvm(node_config['fvm'], build_url['tar_url'])

              with open('node_config.json', 'w') as f:
                  f.write(json.dumps(node_config))
              os.system('python build_config.py')
              fvm_link = 'http://%s:8000/gui/index.html' %node_config['fvm']
              response = 'Imaging started successfully on FVM: ' + fvm_link
              slack_client.api_call("chat.postMessage", channel=channel, text=response)
                
"""
    elif message.get("subtype") is None and 'create cluster' not in message_text:
              print "message_text:", message_text
              print len(message_text)
              channel = message["channel"]
              cluster_name = message_text.split()[3]
              jarvis_request_url = JARVIS_URL + '/api/v1/nodes/' + cluster_name
              print jarvis_request_url
              jarvis_response = requests.get(jarvis_request_url, verify=False)
              jarvis_response = jarvis_response.json()
              request_body = create_fvm_request_body(jarvis_response['data'])
              fvm_request_url = requests.post()
              slack_client.api_call("chat.postMessage", channel=channel, text=message)
"""

# Example reaction emoji echo
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    event = event_data["event"]
    emoji = event["reaction"]
    channel = event["item"]["channel"]
    text = ":%s:" % emoji
    slack_client.api_call("chat.postMessage", channel=channel, text=text)

# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3004)
