import os
import json
from foundation_node import FoundationNode

#cluster_name = raw_input("enter cluster name: ")
if os.path.exists('node_config.json'):
  fp = open('node_config.json', "r")
  node_config = fp.read()
  fp.close()
  #print node_config
  node_config = json.loads(node_config)
  

node_name = node_config["node_name"]
#cluster = "curl -k https://jarvis.eng.nutanix.com/api/v1/clusters/" + cluster_name
#result_code = os.system(cluster + ' > cluster_data.txt')

nodes_metadata = []
for i in range(len(node_config["node_name"].split(","))):
    node = "curl -k https://jarvis.eng.nutanix.com/api/v1/nodes/" + node_config["node_name"].split(",")[i]
    node_data = os.system(node + ' > node_data.txt')
    if os.path.exists('node_data.txt'):
        fp = open('node_data.txt', "r")
        output = fp.read()
        output = json.loads(output)
        nodes_metadata.append(output)
        fp.close()
        os.remove('node_data.txt')
    #print(output)


#print output
#print type(output)
#print output["data"]
config_dict = {}

def setup_block_and_node_information(nodes, cvm_memory=12):
    blocks_config = {}
    node = None
    for node in nodes:
        #print node
        block_id = node.block_id
        #print block_id
        if block_id not in blocks_config:
            blocks_config[node.block_id] = {}
            blocks_config[node.block_id]["block_id"] = node.block_id
            blocks_config[node.block_id]["nodes"] = []
        #block_config = blocks_config[node.block_id]
        block_config = blocks_config[node.block_id]
        nodes_config = block_config["nodes"]
	node_config = {
	    "image_now": node.image_now,
	    "ipmi_ip": node.ipmi_ip,
	    "hypervisor_ip": node.host_ip,
	    "hypervisor": node.hypervisor_type,
	    "ipmi_mac": node.ipmi_mac,
	    "ipmi_password": node.ipmi_password,
	    "ipmi_user": node.ipmi_user,
	    "node_position": node.position,
	    "node_serial": node.serial,
	    "cvm_ip": node.cvm_ip,
	    "hypervisor_hostname": node.hostname,
	    "cvm_gb_ram": cvm_memory
	  }
	nodes_config.append(node_config)
    blocks = blocks_config.values()
    #print blocks_config

    config_dict.update({
      "blocks": blocks,
      "clusters": [],
      "hypervisor_netmask": nodes[0].netmask,
      "hypervisor_gateway": nodes[0].gateway,
      "ipmi_user": nodes[0].ipmi_user,
      "ipmi_password": nodes[0].ipmi_password,
      "ipmi_gateway": nodes[0].ipmi_gateway,
      "ipmi_netmask": nodes[0].ipmi_netmask,
      "cvm_netmask": nodes[0].netmask,
      "cvm_gateway": nodes[0].gateway
    })

def setup_cluster_creation(cluster_members, cluster_name, redundancy_factor=2,
                           cvm_ntp="", cvm_dns="",hypervisor_ntp_servers="", timezone="Africa/Addis_Ababa"):
    """

    Args:
      cluster_init(bool): True or False
      redundancy_factor(int): Redundancy Factor for a cluster - 2 or 3
      cvm_ntp(str): IP address for CVM NTP
      cvm_dns(str): IP address for CVM DNS
      hypervisor_ntp_servers(str): IP address for Hypervisor NTP
      timezone(str): Timezone to be configured on CVM

    Returns:
      None

    """
    clusters_to_create = []
    cluster_config = {"cluster_name":cluster_name ,
                "redundancy_factor": redundancy_factor,
                "cluster_members": cluster_members,
                "cluster_init_now": True,
                "cluster_external_ip": None,
                "cluster_init_successful": None,
                "timezone": timezone,
                "cvm_ntp_servers": cvm_ntp,
                "cvm_dns_servers": cvm_dns}
    clusters_to_create.append(cluster_config)

    config_dict.update({"clusters": clusters_to_create,
                        "hypervisor_ntp_servers": hypervisor_ntp_servers})

def setup_nos_hyp(nos_name, hyp_iso):
  """
  setup NOS and hypervisir
  """
  config_dict["nos_package"] = nos_name
  config_dict["hypervisor_iso"] = {}

def setup_hypervisor_type(hypervisor_type):
    """

    Args:
      hypervisor_type (str): esx, kvm etc

    Returns:
      None

    """
    for block in config_dict["blocks"]:
      for node in block["nodes"]:
        if not node["hypervisor"]:
          node["hypervisor"] = hypervisor_type
nodes = [FoundationNode(metadata = node_data) for node_data in nodes_metadata]
#print nodes
#print dir(nodes[0])
#print nodes[0].block_id

setup_block_and_node_information(nodes)
cluster_members = [config_dict["blocks"][0]["nodes"][i]["cvm_ip"] for i in range(len(config_dict["blocks"][0]["nodes"]))]
cluster_name = node_config.get("cluster_name", node_config.get("node_name").split(",")[0])
setup_cluster_creation(cluster_members=cluster_members, cluster_name=cluster_name)
nos_name = "nutanix_installer_package-release-euphrates-5.11-stable-db5047ecc43c99e3396e0f115818ad3bf307cc01-x86_64.tar.gz"
setup_nos_hyp(nos_name=nos_name, hyp_iso="")
setup_hypervisor_type("kvm")
#print config_dict
config_dict = json.dumps(config_dict)
print json.dumps(config_dict)

image_nodes_curl = 'curl -X POST --header "Content-Type: application/json" --header "Accept: application/json" -d' \
   + json.dumps(config_dict) + ' "http://10.47.99.231:8000/foundation/image_nodes"'

print image_nodes_curl
os.system(image_nodes_curl + ' > session_id.log')

